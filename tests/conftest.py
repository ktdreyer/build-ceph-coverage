import os
import py.path
import pytest

TESTS_DIR = os.path.dirname(os.path.abspath(__file__))
FIXTURES_DIR = os.path.join(TESTS_DIR, 'fixtures')


@pytest.fixture
def fixtures_dir(scope='session'):
    return py.path.local(FIXTURES_DIR)


@pytest.fixture
def tmp_spec_dir(tmpdir, fixtures_dir):
    """
    Temporary directory with a copy of our spec fixture.
    """
    ceph_spec = fixtures_dir.join('ceph.spec')
    ceph_spec.copy(tmpdir)
    return tmpdir
