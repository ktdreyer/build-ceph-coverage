import pytest
import rebuild


@pytest.fixture
def munged_spec(tmp_spec_dir):
    """
    Return the contents of a munged spec file.
    """
    path = str(tmp_spec_dir)
    build = {'release': '59'}
    rebuild.munge_spec(path, build)
    spec = tmp_spec_dir.join('ceph.spec')
    text = spec.read_text('utf-8')
    return text


def test_release(munged_spec):
    expected = 'Release: 59.coverage%{dist}'
    assert expected in munged_spec


def test_package(munged_spec):
    expected = '%package coverage\n'
    assert expected in munged_spec


def test_enable_coverage(munged_spec):
    expected = '-DENABLE_COVERAGE=1 \\\n'
    assert expected in munged_spec


def test_install(munged_spec):
    expected = 'cp -r src %{buildroot}/usr/src/coverage/ceph/\n'
    assert expected in munged_spec


def test_files(munged_spec):
    expected = '%files coverage\n'
    assert expected in munged_spec
