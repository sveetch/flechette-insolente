import pytest

from flechette_insolente.exceptions import CommandArgumentsError
from flechette_insolente.compiler.arguments import ArgumentsModel


def test_arguments_error_source_invalid():
    """
    Source does not exist
    """
    with pytest.raises(CommandArgumentsError) as exc_info:
        ArgumentsModel(
            "foo.css",
        )
    assert exc_info.value.args[0] == "Given source path does not exist: foo.css"


def test_arguments_error_unknow_argument(source_structure):
    """
    Invalid argument
    """
    with pytest.raises(CommandArgumentsError) as exc_info:
        ArgumentsModel(
            source_structure / "scss/minimal.scss",
            michou=True
        )
    assert exc_info.value.args[0] == "Unknowed argument: michou"


def test_arguments_error_invalid_loadpath(source_structure):
    """
    Invalid load-path
    """
    with pytest.raises(CommandArgumentsError) as exc_info:
        ArgumentsModel(
            source_structure / "scss/minimal.scss",
            load_paths=[
                source_structure / "libraries/addons/",
                "../nope",
                "niet"
            ],
        )
    assert exc_info.value.args[0] == (
        "Some given 'load-path' does not exist: \n../nope\nniet"
    )


def test_arguments_error_style_invalid(source_structure):
    """
    Invalid output style name
    """
    with pytest.raises(CommandArgumentsError) as exc_info:
        ArgumentsModel(
            source_structure / "scss/minimal.scss",
            style="niet",
        )
    assert exc_info.value.args[0] == (
        "Invalid given output style 'niet', it should be one of: expanded, compressed"
    )
