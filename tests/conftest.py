"""
Pytest fixtures
"""
import shutil
from pathlib import Path

import pytest

import flechette_insolente


class FixturesSettingsTestMixin(object):
    """
    A mixin containing settings about application. This is almost only about useful
    paths which may be used in tests.

    Attributes:
        application_path (pathlib.Path): Absolute path to the application directory.
        package_path (pathlib.Path): Absolute path to the package directory.
        tests_dir (pathlib.Path): Directory name which include tests.
        tests_path (pathlib.Path): Absolute path to the tests directory.
        datas_dir (pathlib.Path): Directory name which include tests datas.
        datas_path (pathlib.Path): Absolute path to the tests datas.
    """
    def __init__(self):
        self.application_path = Path(
            flechette_insolente.__file__
        ).parents[0].resolve()

        self.package_path = self.application_path.parent

        self.tests_dir = "tests"
        self.tests_path = self.package_path / self.tests_dir

        self.datas_dir = "fixture_datas"
        self.datas_path = self.tests_path / self.datas_dir

    def format(self, content):
        """
        Format given string to include some values related to this application.

        Arguments:
            content (str): Content string to format with possible values.

        Returns:
            str: Given string formatted with possible values.
        """
        return content.format(
            HOMEDIR=Path.home(),
            PACKAGE=str(self.package_path),
            APPLICATION=str(self.application_path),
            TESTS=str(self.tests_path),
            FIXTURES=str(self.datas_path),
            VERSION=flechette_insolente.__version__,
        )


@pytest.fixture(scope="function")
def temp_builds_dir(tmp_path):
    """
    Prepare a temporary build directory.

    NOTE: You should use directly the "tmp_path" fixture in your tests.
    """
    return tmp_path


@pytest.fixture(scope="function")
def source_structure(tmp_path, settings):
    """
    Copy the Sass source structure into a temporary directory.

    Returns:
        Path: The path to the copied structure in temp directory.
    """
    sample_dirname = "sources"
    basic_sample_path = settings.datas_path / sample_dirname
    destination = tmp_path / sample_dirname

    shutil.copytree(basic_sample_path, destination)

    return destination


@pytest.fixture(scope="module")
def settings():
    """
    Initialize and return settings for tests.

    Example:
        You may use it like: ::

            def test_foo(settings):
                print(settings.package_path)
                print(settings.format("Application version: {VERSION}"))
    """
    return FixturesSettingsTestMixin()
