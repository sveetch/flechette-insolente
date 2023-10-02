import copy
from pathlib import Path

from ..exceptions import CommandArgumentsError

from .validators import ArgumentsValidationAbstract


def lazy_type(*args, **kwargs):
    """
    Returns a callable to resolve object with args and kwargs if coerce_type is
    given.

    Arguments:
        *args: Positionnal argument to give to object type when coercing.
        *kwargs: Non positionnal arguments to give to object type when coercing.

    Returns:
        function: A callable function which expect optional ``coerce_type`` non
            positional argument which is a class object to use to coerce to. If not
            given, args and kwargs are just returned into a tuple.
    """
    def _curried(coerce_type=None):
        print("* lazy_type: args, kwargs:", args, kwargs)
        if not coerce_type:
            return args, kwargs

        return coerce_type(*args, **kwargs)

    return _curried


class ArgumentsModel(ArgumentsValidationAbstract):
    """
    Implementation model for dart-sass arguments.

    This describe all arguments and options supported by dart-sass executable, validate
    value and possibly build the arguments and options chain to give to executable or
    build click arguments and options.

    This is the reference for supported ``dart-sass`` executable positional parameters
    which participate to build the command line arguments implemented with Click and
    the positional arguments for ``ArgumentsModel`` class.

    ``COMMAND_ARGUMENTS`` and ``COMMAND_OPTIONS`` are modelized after the Click
    parameters API.

    TODO:

    - May use more specific exceptions;

    Attributes:
        OPTION_STYLE_CHOICES (tuple): Available choices for ``style`` option.
        COMMAND_ARGUMENTS (dict): Description of available click arguments.
        COMMAND_OPTIONS (dict): Description of available click arguments.
        cmd_args (list): List of all parameters to give to dart-sass executable.
    """
    # Available choices for 'style' option
    OPTION_STYLE_CHOICES = ("expanded", "compressed")

    # Available click arguments
    COMMAND_ARGUMENTS = {
        "source": {
            "coerce_type": "path",
            "kwargs": {
                "type": lazy_type(
                    file_okay=True, dir_okay=True, writable=True, resolve_path=False,
                    path_type=Path, exists=True,
                ),
                "required": True,
            }
        },
        "destination": {
            "coerce_type": "path",
            "kwargs": {
                "type": lazy_type(
                    file_okay=True, dir_okay=True, writable=True, resolve_path=False,
                    path_type=Path,
                ),
                "required": False,
            }
        },
    }

    # Available click options
    COMMAND_OPTIONS = {
        "style": {
            "coerce_type": "choice",
            "args": ("--style",),
            "kwargs": {
                "metavar": "STRING",
                "type": lazy_type(OPTION_STYLE_CHOICES),
                "help": (
                    "Output style."
                ),
                "show_default": True,
                "default": OPTION_STYLE_CHOICES[0],
            }
        },
        "load_paths": {
            "coerce_type": "path",
            "args": ("--load-path",),
            "kwargs": {
                "metavar": "PATH",
                "type": lazy_type(
                    file_okay=False, dir_okay=True, writable=True, resolve_path=False,
                    path_type=Path, exists=True,
                ),
                "multiple": True,
                "help": (
                    "A path to use when resolving imports. May be passed multiple "
                    "times."
                ),
            }
        },
        # Not sure about this option since it only mention stdin, is that only common
        # shell standard input ? If so, remove it since we won't support it (yet?).
        "indented": {
            "args": ("--indented/--no-indented",),
            "kwargs": {
                "default": None,
                "help": (
                    "Use the indented syntax for input from stdin."
                ),
            }
        },
        "source_map": {
            "args": ("--source-map/--no-source-map",),
            "kwargs": {
                "default": True,
                "help": (
                    "Whether to generate source maps."
                ),
            }
        },
    }

    def __init__(self, source, **kwargs):
        self.destination = None

        # Get source path
        self.source = self._validate_source(source)
        sources = [str(self.source)]

        # Get optional destination path
        destination = kwargs.pop("destination", None)
        if destination:
            self.destination = self._validate_destination(destination)
            sources.append(str(self.destination))

        # Start argument with gathered ressource paths
        self.cmd_args = [":".join(sources)]

        # Get each parameter, validate it and store into command arguments
        for name, value in kwargs.items():
            if name not in self.get_available_parameters():
                raise CommandArgumentsError("Unknowed argument: {}".format(name))
            else:
                content = getattr(self, "_validate_{}".format(name))(value)
                if content:
                    self.cmd_args.extend(content)

    def __str__(self):
        return " ".join(self.cmd_args)

    @classmethod
    def get_available_parameters(cls):
        """
        Get all available arguments for 'ArgumentsModel'.
        """
        parameters = {k: None for k, v in cls.COMMAND_ARGUMENTS.items()}

        for k, v in cls.COMMAND_OPTIONS.items():
            if k in parameters:
                msg = "Found multiple definition for parameter '{}'"
                raise CommandArgumentsError(msg.format(k))

            parameters[k] = v["args"][0].split("/")
            if len(parameters[k]) == 1:
                parameters[k] = parameters[k][0]

        return parameters

    @classmethod
    def coerce_parameter_type(cls, types, name, values):
        """
        TODO:
        Coerce parameter type in place if type is defined.
        """
        coerce_type = None

        if "coerce_type" in values:
            print("- values['coerce_type']", values["coerce_type"])
            if values["coerce_type"] not in types:
                msg = (
                    "Argument '{name}' define a coerce type '{ctype}' that is not "
                    "available from resolver."
                )
                raise CommandArgumentsError(msg.format(
                    name=name,
                    ctype=values["coerce_type"],
                ))

            # Pop coerce_type that is not an allowed kwargs
            coerce_type = types.get(values["coerce_type"])
            del values["coerce_type"]
            print("- coerce_type", coerce_type)

            if "type" not in values.get("kwargs", []):
                msg = (
                    "Argument '{name}' define a coerce type '{ctype}' but has no "
                    "'type' kwarg."
                )
                raise CommandArgumentsError(msg.format(
                    name=name,
                    ctype=coerce_type,
                ))

        if "type" in values.get("kwargs", []):
            print("- values['kwargs']['type']", values["kwargs"]["type"])
            values["kwargs"]["type"] = values["kwargs"]["type"](
                coerce_type=coerce_type
            )

        return

    @classmethod
    def get_cli_arguments(cls, types):
        """
        TODO:
        Returns the arguments descriptions with lazy type callables coerced to the
        right type.
        """
        arguments = copy.deepcopy(cls.COMMAND_ARGUMENTS)

        for name, values in arguments.items():
            print()
            print("📄 arg:", name, values)

            cls.coerce_parameter_type(types, name, values)

        return arguments
