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


def test_arguments_lazy_type():
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


def test_arguments_get_available_parameters_multiple_occurences():
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


def test_arguments_get_available_parameters():
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


def test_arguments_coerce_parameter_type():
    """
    TODO
    """
    values = {
        "coerce_type": "choice",
        "kwargs": {
            "type": lazy_type(["plip", "plop"]),
            "required": True,
        }
    }
    ArgumentsModel.coerce_parameter_type(
        {
            "choice": DummyChoice,
        },
        "foo",
        values,
    )

    print()
    print(
        json.dumps(values, cls=ExtendedJsonEncoder, indent=4)
    )
    print()

    assert 1 == 42


@pytest.mark.skip
def test_arguments_get_cli_arguments():
    """
    TODO Method should return the dict of arguments description with resolved type
    objects.
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

    parameters = CustomArgumentsModel.get_cli_arguments({
        "choice": DummyChoice,
    })

    print()
    print(
        json.dumps(parameters, cls=ExtendedJsonEncoder, indent=4)
    )
    print()

    values = {
        "coerce_type": "choice",
        "kwargs": {
            "type": lazy_type(["plip", "plop"]),
            "required": True,
        }
    }
    ArgumentsModel.coerce_parameter_type(
        {
            "choice": DummyChoice,
        },
        "foo",
        values,
    )

    print()
    print(
        json.dumps(values, cls=ExtendedJsonEncoder, indent=4)
    )
    print()

    assert 1 == 42


def test_arguments_get_available_parameters_formerly_spec():
    """
    Just get available parameters as described from ArgumentsModel attributes to ensure
    they do not have any error
    """
    parameters = ArgumentsModel.get_available_parameters()

    assert len(parameters) > 1
