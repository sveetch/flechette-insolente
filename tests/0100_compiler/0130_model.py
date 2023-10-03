from flechette_insolente.compiler.arguments import ArgumentsModel


def test_success_simple_source(source_structure):
    """
    Only giving source path
    """
    model = ArgumentsModel(source_structure / "scss/minimal.scss")
    assert model.cmd_args == ["{}/scss/minimal.scss".format(source_structure)]


def test_success_with_destination(source_structure):
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


def test_success_loadpath(source_structure):
    """
    With some load-path
    """
    model = ArgumentsModel(
        source_structure / "scss/minimal.scss",
        load_path=[
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


def test_style(source_structure):
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


def test_indented(source_structure):
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


def test_source_map(source_structure):
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


def test_success_mixed(source_structure):
    """
    With many various arguments
    """
    model = ArgumentsModel(
        source_structure / "scss/minimal.scss",
        destination=source_structure / "css/",
        load_path=[
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
