from tests.utils import run_file_in_kernel


def test_lib_os_in_kernel():
    assert run_file_in_kernel('list_dir.py')