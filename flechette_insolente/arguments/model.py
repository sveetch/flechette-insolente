import copy

from ..exceptions import CommandArgumentsError

from .definitions import VALUE_CHOICES, COMMAND_ARGUMENTS, COMMAND_OPTIONS
from .validators import ArgumentsValidationAbstract


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
    parameters API with additional "coerce_type" item to define coerce type to perform,
    this item is removed from output for CLI.

    .. NOTE::
        The role of model is to gather every supported parameter in unique place that
        can be used to build CLI parameters or executable parameters.

        Remember we implement this package CLI and the support of dart-sass executable
        and they must match. Also we don't want to hardcode usage of Click types here
        since it may be optional.

    TODO:

    - May use more specific exceptions;
    - Available Coerce types should be defined from module using it:

        - One in compiler for the executable parameters (like "path" would use
          Path object, "choice" would use ... ?);
        - Another one in cli for the CLI args and options (click.Choice, click.Path);
        - Only implement coerce type we need, don't try to cover more for now;

    Attributes:
        VALUE_CHOICES (tuple): All available choice values for arguments and options
            that have some.
        COMMAND_ARGUMENTS (dict): Description of available click arguments.
        COMMAND_OPTIONS (dict): Description of available click arguments.
        cmd_args (list): List of all parameters to give to dart-sass executable.
    """
    # Available choices for 'style' option
    VALUE_CHOICES = VALUE_CHOICES

    # Available click arguments, note than the item name is used to name the argument
    # to Click
    COMMAND_ARGUMENTS = COMMAND_ARGUMENTS

    # Available click options, note than Click use the "args" item to name the value
    COMMAND_OPTIONS = COMMAND_OPTIONS

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
        Coerce parameter if type is defined and match available type resolvers.

        Arguments:
            cls (object): Class object.
            types (dict): A dictionnary of available coerce object indexed on their name
                related to ``coerce_type``.
            name (string): Parameter name.
            values (dict): Original dictionnary of values.

        Returns:
            dict: Given values where "coerce_type" has been removed and with possible
            type coerced.
        """
        coerce_type = None
        # Ensure we don't edit in place given values
        values = copy.deepcopy(values)

        if "coerce_type" in values:
            if values["coerce_type"] not in types:
                msg = (
                    "Argument '{name}' define a coerce type '{ctype}' that is not "
                    "available from resolver"
                )
                raise CommandArgumentsError(msg.format(
                    name=name,
                    ctype=values["coerce_type"],
                ))

            # Pop coerce_type that is not an allowed kwargs
            coerce_type_name = values["coerce_type"]
            coerce_type = types.get(values["coerce_type"])
            del values["coerce_type"]

            if "type" not in values.get("kwargs", []):
                msg = (
                    "Argument '{name}' define a coerce type '{ctype}' but has no "
                    "'type' kwarg"
                )
                raise CommandArgumentsError(msg.format(
                    name=name,
                    ctype=coerce_type_name,
                ))

        if "type" in values.get("kwargs", []):
            values["kwargs"]["type"] = values["kwargs"]["type"](
                coerce_type=coerce_type
            )

        return values

    @classmethod
    def get_cli_arguments(cls, types):
        """
        Returns commandline argument descriptions.

        Arguments:
            cls (object): Class object.
            types (dict): A dictionnary of available coerce object indexed on their name
                related to ``coerce_type``.

        Returns:
            dict: Argument descriptions.
        """
        return {
            name: cls.coerce_parameter_type(types, name, values)
            for name, values in cls.COMMAND_ARGUMENTS.items()
        }

    @classmethod
    def get_cli_options(cls, types):
        """
        Returns commandline option descriptions.

        Arguments:
            cls (object): Class object.
            types (dict): A dictionnary of available coerce object indexed on their name
                related to ``coerce_type``.

        Returns:
            dict: Argument descriptions.
        """
        return {
            name: cls.coerce_parameter_type(types, name, values)
            for name, values in cls.COMMAND_OPTIONS.items()
        }
