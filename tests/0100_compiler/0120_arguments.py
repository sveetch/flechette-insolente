import json
from pathlib import Path

import pytest

from flechette_insolente.exceptions import CommandArgumentsError
from flechette_insolente.compiler.arguments import lazy_type, ArgumentsModel
from flechette_insolente.utils.jsons import DummyStr, ExtendedJsonEncoder


class DummyChoice(DummyStr):
    """
    A dummy choice class for test purposes.
    """
    def __init__(self, *args, **kwargs):
        self.args, self.kwargs = args, kwargs

    def __str__(self):
        return "/".join(*self.args)


class DummyPath(DummyStr):
    """
    A dummy path class for test purposes.
    """
    def __init__(self, *args, **kwargs):
        self.args, self.kwargs = args, kwargs

    def __str__(self):
        print(self.args, self.kwargs)
        items = [
            v
            for v in self.args
        ] + [
            "{}:{}".format(k, v)
            for k, v in self.kwargs.items()
        ]
        if items:
            return ";".join(items)

        return "<EMPTY>"


def test_lazy_type():
    """
    Method returns resolved object type with args and kwargs if type object is given,
    else just returns a tuple of args and kwargs.
    """
    assert lazy_type()() == ((), {})

    lazy_int = lazy_type("42")
    resolved = lazy_int(coerce_type=int)
    assert lazy_int() == (("42",), {})
    assert isinstance(resolved, int)
    assert resolved == 42

    lazy_string = lazy_type("42")
    resolved = lazy_string(coerce_type=str)
    assert lazy_string() == (("42",), {})
    assert isinstance(resolved, str)
    assert resolved == "42"

    lazy_path = lazy_type("/home/foo/")
    resolved = lazy_path(coerce_type=Path)
    assert lazy_path() == (("/home/foo/",), {})
    assert isinstance(resolved, Path)
    assert resolved == Path("/home/foo")

    lazy_invalid = lazy_type("invalid")
    with pytest.raises(ValueError):
        lazy_invalid(coerce_type=int)


def test_get_available_parameters_multiple_occurences():
    """
    Method should raise an error for multiple identical parameters.
    """
    # Define a custom model with a minimal spec
    class CustomArgumentsModel(ArgumentsModel):
        COMMAND_ARGUMENTS = {
            "source": {},
        }
        COMMAND_OPTIONS = {
            "source": {
                "args": ("--source",),
            },
        }

    with pytest.raises(CommandArgumentsError) as exc_info:
        CustomArgumentsModel.get_available_parameters()

    assert exc_info.value.args[0] == "Found multiple definition for parameter 'source'"


def test_get_available_parameters():
    """
    Use custom attributes to check everything is working without to assert on
    the huge parameter spec.
    """
    # Define a custom model with a minimal spec
    class CustomArgumentsModel(ArgumentsModel):
        COMMAND_ARGUMENTS = {
            "source": {},
        }
        COMMAND_OPTIONS = {
            "style": {
                "args": ("--style",),
            },
            "indented": {
                "args": ("--indented/--no-indented",),
            },
        }

    parameters = CustomArgumentsModel.get_available_parameters()

    assert parameters == {
        "source": None,
        "style": "--style",
        "indented": ["--indented", "--no-indented"]
    }


def test_get_available_parameters_former_spec():
    """
    Just get available parameters as described from ArgumentsModel attributes to ensure
    they do not have any error
    """
    parameters = ArgumentsModel.get_available_parameters()

    assert len(parameters) > 1


def test_coerce_parameter_type():
    """
    Coerce type method should properly resolve type with or without coerce_type
    """
    # Without a coerce type
    values = ArgumentsModel.coerce_parameter_type(
        {},
        "foo",
        {
            "kwargs": {
                "type": lazy_type(["plip", "plop"]),
                "required": True,
            }
        },
    )
    serialized = json.loads(json.dumps(values, cls=ExtendedJsonEncoder, indent=4))
    assert serialized == {
        "kwargs": {
            "type": [
                [["plip", "plop"]], {}
            ],
            "required": True
        }
    }

    # With a proper coerce type
    values = ArgumentsModel.coerce_parameter_type(
        {"choice": DummyChoice},
        "foo",
        {
            "coerce_type": "choice",
            "kwargs": {
                "type": lazy_type(["plip", "plop"]),
                "required": True,
            }
        },
    )
    serialized = json.loads(json.dumps(values, cls=ExtendedJsonEncoder, indent=4))
    assert serialized == {
        "kwargs": {
            "type": "plip/plop",
            "required": True
        }
    }


def test_coerce_parameter_type_errors():
    """
    Coerce type method should raise exception when defined coerce_type is unknow or
    if coerce_type is defined but item has no type kwarg.
    """
    # With an unknowed coerce type name
    with pytest.raises(CommandArgumentsError) as exc_info:
        ArgumentsModel.coerce_parameter_type(
            {},
            "foo",
            {
                "coerce_type": "nope",
                "kwargs": {
                    "type": lazy_type(["plip", "plop"]),
                    "required": True,
                }
            },
        )

    assert exc_info.value.args[0] == (
        "Argument 'foo' define a coerce type 'nope' that is not available from "
        "resolver"
    )

    # Define a coerce type but has no 'type' kwargs
    with pytest.raises(CommandArgumentsError) as exc_info:
        ArgumentsModel.coerce_parameter_type(
            {"choice": DummyChoice},
            "foo",
            {
                "coerce_type": "choice",
                "kwargs": {
                    "required": True,
                }
            },
        )

    assert exc_info.value.args[0] == (
        "Argument 'foo' define a coerce type 'choice' but has no 'type' kwarg"
    )


def test_get_cli_arguments():
    """
    Method should return the dict of argument descriptions with coerced type objects if
    there is any.
    """
    class CustomArgumentsModel(ArgumentsModel):
        COMMAND_ARGUMENTS = {
            "foo": {
                "coerce_type": "choice",
                "kwargs": {
                    "type": lazy_type(["plip", "plop"]),
                    "required": True,
                }
            },
            "bar": {
                "kwargs": {
                    "type": lazy_type(["zip", "zap"]),
                    "a_kwargs": "whatever",
                }
            },
        }

    parameters = CustomArgumentsModel.get_cli_arguments({"choice": DummyChoice})
    serialized = json.loads(json.dumps(parameters, cls=ExtendedJsonEncoder, indent=4))
    assert serialized == {
        "foo": {
            "kwargs": {
                "type": "plip/plop",
                "required": True
            }
        },
        "bar": {
            "kwargs": {
                "type": [
                    [
                        ["zip", "zap"]
                    ],
                    {}
                ],
                "a_kwargs": "whatever"
            }
        }
    }


def test_get_cli_options():
    """
    Method should return the dict of option descriptions with coerced type objects if
    there is any.
    """
    class CustomArgumentsModel(ArgumentsModel):
        COMMAND_OPTIONS = {
            "foo": {
                "coerce_type": "choice",
                "kwargs": {
                    "type": lazy_type(["plip", "plop"]),
                    "required": True,
                }
            },
            "bar": {
                "kwargs": {
                    "type": lazy_type(["zip", "zap"]),
                    "a_kwargs": "whatever",
                }
            },
        }

    parameters = CustomArgumentsModel.get_cli_options({"choice": DummyChoice})
    serialized = json.loads(json.dumps(parameters, cls=ExtendedJsonEncoder, indent=4))
    assert serialized == {
        "foo": {
            "kwargs": {
                "type": "plip/plop",
                "required": True
            }
        },
        "bar": {
            "kwargs": {
                "type": [
                    [
                        ["zip", "zap"]
                    ],
                    {}
                ],
                "a_kwargs": "whatever"
            }
        }
    }


def test_get_cli_arguments_options_former_spec():
    """
    Method should return the dict of argument descriptions with coerced type objects if
    there is any. We don't test content to avoid having huge expected content here, only
    that everything worked without errors.

    NOTE: This use only dummy coerce types. We may move this test in more apprioate
    test module related to coerce context like the CLI.
    """
    available_types = {
        "choice": DummyChoice,
        "path": DummyPath,
    }
    arguments = ArgumentsModel.get_cli_arguments(available_types)
    # serialized = json.dumps(arguments, cls=ExtendedJsonEncoder, indent=4)
    # print()
    # print(serialized)
    # print()
    assert isinstance(arguments, dict)
    assert len(arguments) > 1

    options = ArgumentsModel.get_cli_options(available_types)
    # serialized = json.dumps(options, cls=ExtendedJsonEncoder, indent=4)
    # print()
    # print(serialized)
    # print()
    assert isinstance(options, dict)
    assert len(options) > 1
