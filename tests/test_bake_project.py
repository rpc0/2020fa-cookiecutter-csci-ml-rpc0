from contextlib import contextmanager

import os
import subprocess

from cookiecutter.utils import rmtree


@contextmanager
def inside_dir(dirpath):
    """
    Execute code from inside the given directory
    :param dirpath: String, path of the directory the command is being run.
    """
    old_path = os.getcwd()
    try:
        os.chdir(dirpath)
        yield
    finally:
        os.chdir(old_path)

# Copied from cookiecutter author's github file
# https://github.com/audreyfeldroy/cookiecutter-pypackage/blob/master/tests/test_bake_project.py
# then edited

@contextmanager
def bake_in_temp_dir(cookies, *args, **kwargs):
    """
    Delete the temporal directory that is created when executing the tests
    :param cookies: pytest_cookies.Cookies,
        cookie to be baked and its temporal files will be removed
    """
    result = cookies.bake(*args, **kwargs)
    try:
        yield result
    finally:
        rmtree(str(result.project))


def test_bake_with_defaults(cookies):
    with bake_in_temp_dir(cookies) as result:
        assert result.project.isdir()
        assert result.exit_code == 0
        assert result.exception is None

        found_toplevel_files = [f.basename for f in result.project.listdir()]
        assert 'pytest.ini' in found_toplevel_files
        assert 'test_pset.py' in found_toplevel_files
        assert 'Pipfile' in found_toplevel_files

        # Test of conditionally including or excluding csci-utils
        with open('Pipfile') as f:
            if 'csci-utils' in f.read():
                raise AssertionError



def test_project_tree(cookies):
    result = cookies.bake(extra_context={'repo_name': 'test_project'})
    assert result.exit_code == 0
    assert result.exception is None
    assert result.project.basename == 'test_project'


# def test_run_flake8(cookies):
#     result = cookies.bake(extra_context={'project_slug': 'flake8_compat'})
#     with inside_dir(str(result.project)):
#         subprocess.check_call(['flake8'])
