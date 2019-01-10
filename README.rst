Rebuild ceph with code coverage enabled

This script pulls the latest (already-released) build out of Brew and
scratch-builds it with code coverage enabled. It generates a Yum repository and
stores the artifacts on a remote server.

This allows QE to use these builds to get code coverage metrics.


Prerequisites
-------------

You will need the ``brewkoji`` package::

    (Add the RCMTOOLS repository to /etc/yum.repos.d)

    sudo yum -y install brewkoji

And the ``createrepo`` utility::

    sudo yum -y install createrepo_c

Getting the code
----------------

Clone this repository::

    git clone https://github.com/ktdreyer/build-ceph-coverage
    cd build-ceph-coverage

Running
-------

Ensure you have a Kerberos ticket::

   kinit kdreyer

Run the script::

   ./rebuild.py

Results
-------

This generates a new ``ceph-coverage`` RPM that you can download. This package
ships the ``.cc`` and ``.gcno`` files in ``/usr/src/coverage/ceph``.

To extract this RPM on an Ubuntu system (without installing it), you can run::

   rpm2cpio path/to/ceph-coverage-12.2.5-1.noarch.el7cp | cpio -dium

This ``rpm2cpio ... | cpio -dium`` command will extract all the RPM's files
into the current working directory.
