from pathlib import Path

from flechette_insolente.exceptions import CommandArgumentsError


def lazy_path_type(*args, **kwargs):
    """
    This way so importing click is only done during resolution in command
    """
    # return click.Path
    return


def lazy_choice_type(*args, **kwargs):
    """
    This way so importing click is only done during resolution in command
    """
    # return click.Choice
    return


class ArgumentsModel:
    """
    Implementation model for dart-sass arguments.

    This describe all arguments and options supported by dart-sass executable, validate
    value and possibly build the arguments and options chain to give to executable or
    build click arguments and options.

    TODO: Use more specific exceptions.

    Attributes:
        OPTION_STYLE_CHOICES (tuple): Available choices for ``style`` option.
        COMMAND_ARGUMENTS (dict): Description of available click arguments. This is
            the reference for supported ``dart-sass`` executable positional parameters
            which participate to build the command line arguments implemented with
            Click and the positional arguments for ``ArgumentsModel`` class.
        COMMAND_OPTIONS (dict): Description of available click arguments. This is
            the reference for supported ``dart-sass`` executable non positional
            parameters which participate to build the command line options
            implemented with Click and the non positional arguments for
            ``ArgumentsModel`` class.
    """
    # Available choices for 'style' option
    OPTION_STYLE_CHOICES = ("expanded", "compressed")

    # Available click arguments
    COMMAND_ARGUMENTS = {
        "source": {
            "kwargs": {
                "type": lazy_path_type(
                    file_okay=True, dir_okay=True, writable=True, resolve_path=False,
                    path_type=Path, exists=True,
                ),
                "required": True,
            }
        },
        "destination": {
            "kwargs": {
                "type": lazy_path_type(
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
            "args": ("--style",),
            "kwargs": {
                "metavar": "STRING",
                "type": lazy_choice_type(OPTION_STYLE_CHOICES),
                "help": (
                    "Output style."
                ),
                "show_default": True,
                "default": OPTION_STYLE_CHOICES[0],
            }
        },
        "load_paths": {
            "args": ("--load-path",),
            "kwargs": {
                "metavar": "PATH",
                "type": lazy_path_type(
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

        for name, value in kwargs.items():
            if name not in self.get_available_parameters():
                raise CommandArgumentsError("Unknowed argument: {}".format(name))
            else:
                content = getattr(self, "_validate_{}".format(name))(value)
                if content:
                    self.cmd_args.extend(content)

    def __str__(self):
        return " ".join(self.cmd_args)

    def validate_boolean_flag(self, value, arg_true, arg_false):
        """
        Create arguments for given boolean flag

        Arguments:
            value (boolean): If True enable the 'indented' argument, if False enable
                the 'no-indented' argument. Else nothing is done.

        Returns:
            list: List with argument according to the flag if value is boolean, else an
            empty list.
        """
        if value is True:
            return [arg_true]
        elif value is False:
            return [arg_false]

        return []

    def _validate_source(self, value):
        path = Path(value)

        if not path.exists():
            msg = "Given source path does not exist: {}"
            raise CommandArgumentsError(msg.format(path))

        return path

    def _validate_destination(self, value):
        """
        Note:
        We can"t validate anything since Python os/pathlib need an existing ressource
        to check if it is a dir or not. But destination may not exists if it is a file.
        """
        return Path(value)

    def _validate_style(self, value):
        """
        Create arguments for given output style name.

        TODO: Validate style from available choice (to be synchronized with dart-sass
        spec)
        """
        if value not in self.OPTION_STYLE_CHOICES:
            msg = "Invalid given output style '{value}', it should be one of: {names}"
            raise CommandArgumentsError(msg.format(
                value=value,
                names=", ".join(self.OPTION_STYLE_CHOICES),
            ))

        return [self.get_available_parameters()["style"], value]

    def _validate_indented(self, value):
        """
        Create arguments for given indented flag

        Arguments:
            value (boolean): If True enable the 'indented' argument, if False enable
                the 'no-indented' argument. Else nothing is done.

        Returns:
            list: List with argument according to the flag if value is boolean, else an
            empty list.
        """
        return self.validate_boolean_flag(
            value,
            self.get_available_parameters()["indented"][0],
            self.get_available_parameters()["indented"][1],
        )

    def _validate_source_map(self, value):
        """
        Create arguments for given source-map flag

        Arguments:
            value (boolean): If True enable the 'source-map' argument, if False enable
                the 'no-source-map' argument. Else nothing is done.

        Returns:
            list: List with argument according to the flag if value is boolean, else an
            empty list.
        """
        return self.validate_boolean_flag(
            value,
            self.get_available_parameters()["source_map"][0],
            self.get_available_parameters()["source_map"][1],
        )

    def _validate_load_paths(self, value):
        """
        Create arguments for each given path.
        """
        errors = [
            item
            for item in value
            if not Path(item).exists()
        ]
        if len(errors):
            msg = "Some given 'load-path' does not exist: \n{}"
            raise CommandArgumentsError(msg.format(
                "\n".join(errors)
            ))

        paths = []
        for item in value:
            paths.extend([self.get_available_parameters()["load_paths"], str(item)])

        return paths

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
