import pytest

from dartsass.exceptions import CommandArgumentsError
from dartsass.compiler.arguments import ArgumentsAbstract


def test_arguments_errors(source_structure, settings):
    """
    TODO: Possible errors, need more specific excepions to recognize
    """
    # Source does not exist
    with pytest.raises(CommandArgumentsError) as excinfo:
        model = ArgumentsAbstract(
            "foo.css",
        )

    # Invalid argument
    with pytest.raises(CommandArgumentsError) as excinfo:
        model = ArgumentsAbstract(
            "foo.css",
            michou=True
        )


def test_arguments_success(source_structure, settings):
    """
    TODO:
    Argument model should properly gather valid arguments.
    """
    print(source_structure)
    print()
    print([i for i in source_structure.iterdir()])
    print()

    # Only giving source path
    model = ArgumentsAbstract(source_structure / "scss/minimal.scss")
    assert model.cmd_args == ["{}/scss/minimal.scss".format(source_structure)]

    # Giving source as file and destination as directory (model can not validate this
    # but compiler will raise issue because of incompatible ressource type)
    model = ArgumentsAbstract(
        source_structure / "scss/minimal.scss",
        destination=source_structure / "css",
    )
    assert model.cmd_args == [
        "{}/scss/minimal.scss:{}/css".format(source_structure, source_structure),
    ]

    # Giving many valid arguments
    model = ArgumentsAbstract(
        source_structure / "scss/minimal.scss",
        destination=(source_structure / "css/"),
        load_paths=["../node_modules/bootstrap", "foo"],
        style="expanded",
    )
    assert model.cmd_args == [
        "{}/scss/minimal.scss:{}/css".format(source_structure, source_structure),
        "--load-path",
        "../node_modules/bootstrap",
        "--load-path",
        "foo",
        "--style",
        "expanded"
    ]
