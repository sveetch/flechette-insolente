import json
from pathlib import Path

import pytest

from dartsass.exceptions import CommandArgumentsError, RunnedCommandError
from dartsass.compiler import DartSassCompiler
from dartsass.utils.jsons import ExtendedJsonEncoder
from dartsass.plateform_build import DART_SASS_EXEC


def temp_debug():
    try:
        # Compile sample that may fail
        output = compiler.compile(
            scss_bucket / "basic.scss",
        )
    except RunnedCommandError as e:
        print()
        print(e)
        print()
        print(
            json.dumps(e.error_payload, cls=ExtendedJsonEncoder, indent=4)
        )
        print()
    else:
        print()
        print(output)
        print()
        for item in css_bucket.iterdir():
            print("-", item)
        print()

    assert 1 == 42


def test_compiler_error_destination_mismatch_source(source_structure, settings):
    """
    Dart Sass compiler raises an error when when source and destination have different
    ressource type. Like if source is a file, it tries to resolve destination as a
    directory.
    """
    compiler = DartSassCompiler()

    scss_bucket = source_structure / "scss"
    css_bucket = source_structure / "css"
    css_bucket.mkdir()

    with pytest.raises(RunnedCommandError) as exc_info:
        compiler.compile(
            scss_bucket / "minimal.scss",
            destination=css_bucket,
        )

    assert exc_info.value.message == "Command failed with signal code: 66"

    # Test stdout value apart since it contains weird relative path
    stdout = exc_info.value.error_payload.pop("stdout")
    assert stdout.startswith("Error reading ") is True
    assert stdout.endswith(": Cannot open file.\n") is True

    assert exc_info.value.error_payload == {
        "returncode": 66,
        "cmd": [
            DART_SASS_EXEC,
            "{scss_bucket}/minimal.scss:{css_bucket}".format(
                scss_bucket=scss_bucket,
                css_bucket=css_bucket
            ),
        ],
        "stderr": None,
        "timeout": None
    }


def test_compiler_error_missing_import(source_structure, settings):
    """
    Dart Sass compiler raises an error when a Sass source try to import a module that
    is not available either from sources or load-path items.
    """
    compiler = DartSassCompiler()

    scss_bucket = source_structure / "scss"
    css_bucket = source_structure / "css"
    css_bucket.mkdir()

    with pytest.raises(RunnedCommandError) as exc_info:
        output = compiler.compile(
            scss_bucket / "basic.scss",
        )

    assert exc_info.value.message == "Command failed with signal code: 65"

    assert exc_info.value.error_payload == {
        "returncode": 65,
        "cmd": [
            DART_SASS_EXEC,
            str(scss_bucket / "basic.scss"),
        ],
        "stdout": (
            "Error: Can't find stylesheet to import.\n"
            "  \u2577\n5 \u2502 @import \"addons/addon_lib\";\n"
            "  \u2502         ^^^^^^^^^^^^^^^^^^\n  \u2575\n  "
            "{} 5:9  root stylesheet\n".format(str(scss_bucket / "basic.scss"))
        ),
        "stderr": None,
        "timeout": None
    }


def test_compiler_basic(source_structure):
    """
    With proper arguments, path and source, the compiler will correctly build CSS.
    """
    compiler = DartSassCompiler()

    scss_bucket = source_structure / "scss"
    css_bucket = source_structure / "css"
    css_bucket.mkdir()

    output = compiler.compile(
        scss_bucket,
        destination=css_bucket,
        source_map=True,
        load_paths=[
            source_structure / "libraries",
        ],
    )

    assert sorted(css_bucket.iterdir()) == [
        css_bucket / "basic.css",
        css_bucket / "basic.css.map",
        css_bucket / "minimal.css",
        css_bucket / "minimal.css.map",
    ]
