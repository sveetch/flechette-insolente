from pathlib import Path

from flechette_insolente.exceptions import CommandArgumentsError


class ArgumentsModel:
    """
    Object to receive and validate arguments to produce normalized argument for
    dart-sass executable.

    TODO: Use more specific exceptions.
    """
    AVAILABLE_ARGUMENTS = {
        "source": None,
        "destination": None,
        "style": "--style",
        "load_paths": "--load-path",
        "indented": ("--indented", "--no-indented"),
        "source_map": ("--source-map", "--no-source-map"),
    }
    AVAILABLE_STYLE = ("expanded", "compressed")

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
            if name not in self.AVAILABLE_ARGUMENTS:
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
        if value not in self.AVAILABLE_STYLE:
            msg = "Invalid given output style '{value}', it should be one of: {names}"
            raise CommandArgumentsError(msg.format(
                value=value,
                names=", ".join(self.AVAILABLE_STYLE),
            ))

        return [self.AVAILABLE_ARGUMENTS["style"], value]

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
            self.AVAILABLE_ARGUMENTS["indented"][0],
            self.AVAILABLE_ARGUMENTS["indented"][1],
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
            self.AVAILABLE_ARGUMENTS["source_map"][0],
            self.AVAILABLE_ARGUMENTS["source_map"][1],
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
            paths.extend([self.AVAILABLE_ARGUMENTS["load_paths"], str(item)])

        return paths
