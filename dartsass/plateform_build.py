"""
Available dart-sass build plateform:

* linux-arm
* linux-arm64
* linux-ia32
* linux-x64
* macos-arm64
* macos-x64
* windows-ia32
* windows-x64

Prefix for dart-sass version and file archive extension have been removed from
available dart-sass build releases as from https://github.com/sass/dart-sass/releases

All builds are and will be always from a same version. If some plateform is removed
from dart-sass releases, older versions won't be keeped anymore along others.
"""
import platform

from pathlib import Path

import dartsass

from .exceptions import RunnedCommandError


def get_plateform():
    """
    Get plateform system and machine.

    Found names from Python plateform are normalized to the dart-sass plateform names.

    Tested plateforms: ::

        fred % python
        Python 3.9.9 (main, Jul 8 2022, 14:53:19)
        [Clang 13.0.0 (clang-1300.0.29.3)] on darwin
        system: Darwin
        machine: x86_64

        nico % python
        Python 3.8.16 (default, May 25 2023, 15:27:36)
        [Clang 14.0.3 (clang-1403.0.22.14.1)] on darwin
        system: Darwin
        machine: arm64

    Returns:
        tuple: First item will be system (OS) and second item will be the machine
        (CPU architecture).
    """
    system = platform.system().lower()

    if system == "darwin":
        system = "macos"

    # TODO: This probably need a lot more of name patching for non linux systems
    machine = platform.machine().lower()
    if machine == "x86_64":
        machine = "x64"

    return system, machine


def get_sass_executable():
    """
    Get the path to the dart-sass executable.

    Default behavior

    TODO: Allow to directly get executable path from an environment variable.

    Returns:
        Path: Path to executable file.
    """
    plateform_code = "-".join(get_plateform())
    return Path(dartsass.__file__).parent / "vendor" / plateform_code / "sass"


DART_SASS_EXEC = get_sass_executable()
