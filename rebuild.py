#!/usr/bin/python

from glob import glob
import os
import posixpath
import subprocess
import re

import koji
from koji_cli.lib import activate_session
from koji_cli.lib import watch_tasks
from koji_cli.lib import list_task_output_all_volumes
from koji_cli.lib import download_file
# borrow some private pieces of the koji cli for scratch-building
from koji_cli.lib import _progress_callback
try:
    # Available in Koji v1.17, https://pagure.io/koji/issue/975
    from koji_cli.lib import unique_path
except ImportError:
    from koji_cli.lib import _unique_path as unique_path

"""
Rebuild the ceph package with code coverage enabled, and publish a
repository for QE to consume.
"""

PROFILE = 'brew'  # from /etc/koji.conf.d
PACKAGE = 'ceph'
KEY = 'fd431d51'  # Red Hat release key
TAGS = ('ceph-3.2-rhel-7',)


def get_koji_session():
    # Return an unauthenticated koji session
    try:
        conf = koji.read_config(PROFILE)
    except koji.ConfigurationError as e:
        if 'no configuration for profile name' in str(e):
            print('You are missing the brewkoji RPM. Please install it.')
            print('It is available in the RCMTOOLS composes.')
            print('http://download.devel.redhat.com/rel-eng/RCMTOOLS/')
        raise
    hub = conf['server']
    opts = {'krbservice': conf['krbservice']}
    session = koji.ClientSession(hub, opts)
    # KojiOptions = namedtuple('Options', ['authtype', 'debug'])
    # options = KojiOptions(authtype='')
    # Can I simply pass in the conf dict like this?
    activate_session(session, conf)
    return session


def get_koji_pathinfo():
    # Return a Koji PathInfo object for our profile.
    conf = koji.read_config(PROFILE)
    top = conf['topurl']  # or 'topdir' here for NFS access
    pathinfo = koji.PathInfo(topdir=top)
    return pathinfo


def latest_build(session, tag):
    # Find the latest build NVR for this package in this tag.
    builds = session.getLatestBuilds(tag, package=PACKAGE)
    return builds[0]


def srpm_url(session, build):
    # Return the URL to the signed SRPM for this build.
    pathinfo = get_koji_pathinfo()
    buildinfo = {
        'arch': 'src',
        'name': build['package_name'],
        'version': build['version'],
        'release': build['release'],
    }
    builddir = pathinfo.build(build)
    if KEY:
        rpmpath = pathinfo.signed(buildinfo, KEY)
    else:
        rpmpath = pathinfo.rpm(buildinfo)
    url = posixpath.join(builddir, rpmpath)
    return url


def verify_srpm(filename):
    # Verify that the package matches its checksums.
    # todo: verify gpg signature as well?
    ret = subprocess.call(('rpm', '-K', '--nosignature', filename))
    return ret == 0


def download_srpm(session, build, destination):
    # Download the SRPM from this Koji build into "destination" dir.
    url = srpm_url(session, build)
    filename = posixpath.basename(url)
    destfile = os.path.join(destination, filename)
    if os.path.exists(destfile):
        if verify_srpm(destfile):
            return destfile
        print('existing %s does not verify, re-downloading.' % destfile)
    print('downloading %s to %s' % (url, destination))
    download_file(url, destfile, size=1, num=1)
    verify_srpm(destfile)
    return destfile


def unpack_srpm(srpm):
    # Unpack the src.rpm file.
    # `rpm2cpio file.src.rpm | cpio -dium`
    dirname = os.path.dirname(srpm)
    filename = os.path.basename(srpm)
    ps = subprocess.Popen(('rpm2cpio', filename),
                          cwd=dirname,
                          stdout=subprocess.PIPE)
    subprocess.check_call(('cpio', '-dium'),
                          cwd=dirname,
                          stdin=ps.stdout)
    ps.wait()


def munge_spec(path, build):
    """
    Manipulate ceph.spec with the changes we need for a coverage build.

    1. Bump the release value
    2. Insert -DENABLE_COVERAGE=1 as a cmake option
    3. Copy processed source and gcno files to /usr/src/coverage/ceph
    4. Add new "ceph-coverage" subpackage

    :param path: directory where PACKAGE .spec file is located
    :param build: buildinfo data from Koji
    """
    spec = os.path.join(path, '%s.spec' % PACKAGE)
    m = re.match(r'\d+', build['release'])
    if not m:
        raise ValueError('unable to parse Release %s' % build['release'])
    releaseint = int(m.group())
    release = '%d.1.coverage%%{dist}' % releaseint
    with open(spec) as fileh:
        lines = fileh.readlines()
    print('rewriting %s with coverage changes' % spec)
    with open(spec, 'w') as fileh:
        for line in lines:
            if re.match(r'\s*Release:', line):
                fileh.write('Release: %s\n' % release)
            elif re.match(r'%prep', line):
                text = read_fragment('package')
                fileh.write(text)
                fileh.write(line)
            elif re.match(r'cmake ', line):
                fileh.write(line)
                text = read_fragment('cmake')
                fileh.write(text)
            elif re.match(r'%install', line):
                fileh.write(line)
                text = read_fragment('install')
                fileh.write(text)
            elif re.match(r'%files base', line):
                text = read_fragment('files')
                fileh.write(text)
                fileh.write(line)
            else:
                fileh.write(line)


def read_fragment(name):
    """
    Read a .txt file from the "fragments" directory, and return its contents.
    """
    app_dir = os.path.dirname(os.path.abspath(__file__))
    basename = '%s.txt' % name
    filename = os.path.join(app_dir, 'fragments', basename)
    with open(filename) as fh:
        return fh.read()


def pack_srpm(path):
    # Re-pack the new SRPM
    # todo: wipe any "new" dir here before proceeding...
    #       ...or not, because it won't matter with real tmpdirs.
    cmd = ('rpmbuild',
           '-bs',
           '%s.spec' % PACKAGE,
           '--define=_sourcedir .',
           '--define=_srcrpmdir ./new',
           '--define=dist .el7',
           )
    subprocess.check_call(cmd, cwd=path)
    pattern = os.path.join(path, 'new', '*.src.rpm')
    files = glob(pattern)
    return files[0]


def scratch_build(session, tag, srpm):
    """
    scratch-build the SRPM in Koji. Return the Koji task ID.

    :param session: koji.ClientSession
    :param str tag: koji tag name, eg  "ceph-3.2-rhel-7"
    :param str srpm: path to our temporary coverage .src.rpm file
    """
    target = tag + '-candidate'  # move to separate method?

    # Create a unique temporary directory path to use on the Koji hub server.
    # Conventionally Koji clients use a "cli-build" prefix here, so we'll do
    # the same.
    serverdir = unique_path('cli-build')
    callback = _progress_callback

    # Upload our srpm file to the Koji hub.
    session.uploadWrapper(srpm, serverdir, callback=callback)

    # Send the "build" RPC to the Koji hub. "source" is full (server-side)
    # path to our SRPM.
    source = "%s/%s" % (serverdir, os.path.basename(srpm))
    opts = {'scratch': 'true', 'arch_override': 'x86_64'}

    task_id = session.build(source, target, opts)
    return task_id


def watch_scratch_build(session, task_id):
    error = watch_tasks(session, [task_id], poll_interval=4)
    if error:
        raise RuntimeError('scratch build failed')


def store_binaries(session, task_id, path):
    """
    Store the resulting binaries from a Brew scratch build
    (really wish this was part of the official koji api...)
    """
    task = session.getTaskInfo(task_id)
    assert task['method'] == 'build'
    subtasks = session.getTaskChildren(task_id)
    # Assemble a list of tasks/files to download.
    downloads = []
    for task in subtasks:
        if task['method'] != 'buildArch':
            continue
        files = list_task_output_all_volumes(session, task['id'])
        for filename in files:
            if not filename.endswith('.rpm'):
                continue
            if filename.endswith('.src.rpm'):
                continue
            for volume in files[filename]:
                # I'm keeping it simple for now by only supporting the default
                # volume. I haven't found a buildArch task that blows up yet...
                assert volume == 'DEFAULT'
                downloads.append((task, filename))
    # Do the downloads.
    pathinfo = get_koji_pathinfo()
    number = 0
    for (task, filename) in downloads:
        number += 1
        work = pathinfo.work('DEFAULT')
        taskrelpath = pathinfo.taskrelpath(task['id'])
        url = '%s/%s/%s' % (work, taskrelpath, filename)
        filename = os.path.join(path, 'rpms', filename)
        download_file(url, filename, size=len(downloads), num=number)


def generate_repository(path):
    """ Generate a Yum repository with the binaries. """
    rpmdir = os.path.join(path, 'rpms')
    subprocess.check_call(('createrepo', '.'), cwd=rpmdir)


def publish_repository(path, tag):
    """ Publish the Yum repository somewhere persistent that QE can access. """
    src = os.path.join(path, 'rpms')
    src += '/'
    host = 'file.rdu.redhat.com'
    dest = host + ':/home/remote/kdreyer/public_html/coverage/' + tag + '/'
    #cmd = ('rsync', '-a', '-P', '--delete', src, dest)
    cmd = ('rsync', '-a', '-P', src, dest)
    subprocess.check_call(cmd)


def write_props(srpm, tag):
    """ Write a .props file for Jenkins to read into its environment. """
    pass


def main():
    session = get_koji_session()
    for tag in TAGS:
        build = latest_build(session, tag)
        # TODO: test if we've already built this NVR, to avoid rebuilding it
        # again.

        tempdir = '/tmp/rebuild'  # todo: use real tmpdir instead
        srpm = download_srpm(session, build, tempdir)
        unpack_srpm(srpm)

        # Update the packaging
        munge_spec(tempdir, build)
        srpm = pack_srpm(tempdir)

        # Build this new package
        task_id = scratch_build(session, tag, srpm)
        watch_scratch_build(session, task_id)
        store_binaries(session, task_id, tempdir)

        # Repository work
        generate_repository(tempdir)
        publish_repository(tempdir, tag)
        write_props(srpm, tag)


if __name__ == '__main__':
    main()
