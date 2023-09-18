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

    TODO: Allow to override this from environment variable.

    Returns:
        Path: Path to executable file.
    """
    plateform_code = "-".join(get_plateform())
    return Path(dartsass.__file__).parent / "vendor" / plateform_code / "sass"


DART_SASS_EXEC = get_sass_executable()
