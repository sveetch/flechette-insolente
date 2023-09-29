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


def test_arguments_success_simple_source(source_structure):
    """
    Only giving source path
    """
    model = ArgumentsModel(source_structure / "scss/minimal.scss")
    assert model.cmd_args == ["{}/scss/minimal.scss".format(source_structure)]


def test_arguments_success_with_destination(source_structure):
    """
    Giving source as file and destination as directory (model can not validate this
    but compiler will raise issue because of incompatible ressource type)
    """
    model = ArgumentsModel(
        source_structure / "scss/minimal.scss",
        destination=source_structure / "css",
    )
    assert model.cmd_args == [
        "{}/scss/minimal.scss:{}/css".format(source_structure, source_structure),
    ]


def test_arguments_success_loadpath(source_structure):
    """
    With some load-path
    """
    model = ArgumentsModel(
        source_structure / "scss/minimal.scss",
        load_paths=[
            source_structure / "libraries/",
            source_structure / "libraries/addons/",
        ],
    )
    assert model.cmd_args == [
        "{}/scss/minimal.scss".format(source_structure),
        "--load-path",
        "{}/libraries".format(source_structure),
        "--load-path",
        "{}/libraries/addons".format(source_structure),
    ]


def test_arguments_style(source_structure):
    """
    With style argument
    """
    model = ArgumentsModel(
        source_structure / "scss/minimal.scss",
        style="expanded",
    )
    assert model.cmd_args == [
        "{}/scss/minimal.scss".format(source_structure),
        "--style",
        "expanded"
    ]


def test_arguments_indented(source_structure):
    """
    With indented flag argument
    """
    model = ArgumentsModel(
        source_structure / "scss/minimal.scss",
        indented=True,
    )
    assert model.cmd_args == [
        "{}/scss/minimal.scss".format(source_structure),
        "--indented",
    ]

    model = ArgumentsModel(
        source_structure / "scss/minimal.scss",
        indented=False,
    )
    assert model.cmd_args == [
        "{}/scss/minimal.scss".format(source_structure),
        "--no-indented",
    ]

    model = ArgumentsModel(
        source_structure / "scss/minimal.scss",
        indented="nope",
    )
    assert model.cmd_args == ["{}/scss/minimal.scss".format(source_structure)]


def test_arguments_source_map(source_structure):
    """
    With source_map flag argument
    """
    model = ArgumentsModel(
        source_structure / "scss/minimal.scss",
        source_map=True,
    )
    assert model.cmd_args == [
        "{}/scss/minimal.scss".format(source_structure),
        "--source-map",
    ]

    model = ArgumentsModel(
        source_structure / "scss/minimal.scss",
        source_map=False,
    )
    assert model.cmd_args == [
        "{}/scss/minimal.scss".format(source_structure),
        "--no-source-map",
    ]

    model = ArgumentsModel(
        source_structure / "scss/minimal.scss",
        source_map="nope",
    )
    assert model.cmd_args == ["{}/scss/minimal.scss".format(source_structure)]


def test_arguments_success_mixed(source_structure):
    """
    With many various arguments
    """
    model = ArgumentsModel(
        source_structure / "scss/minimal.scss",
        destination=source_structure / "css/",
        load_paths=[
            source_structure / "libraries/",
            source_structure / "libraries/addons/",
        ],
        style="expanded",
    )
    assert model.cmd_args == [
        "{}/scss/minimal.scss:{}/css".format(source_structure, source_structure),
        "--load-path",
        "{}/libraries".format(source_structure),
        "--load-path",
        "{}/libraries/addons".format(source_structure),
        "--style",
        "expanded"
    ]
