from pathlib import Path

from ..exceptions import CommandArgumentsError


class ArgumentsValidationAbstract:
    """
    An abstract to include all argument validators. It need to work conjointly with
    ArgumentsModel.

    .. NOTE::

        Validation methods does not only validate, they also return a list of options
        parameters to pass to command. This is a list because it is how we have to give
        it to 'subprocess'. Excepted for source and destination that are not options.
    """
    def validate_boolean_flag(self, value, arg_true, arg_false):
        """
        Create arguments for given boolean flag value.

        Arguments:
            value (boolean): The value to check against.
            arg_true (string): Argument name to use if ``value`` is True.
            arg_false (string): Argument name to use if ``value`` is False.

        Returns:
            list: If True use list will include value from ``arg_true``, else if False
                use value from ``arg_false``. If none of these booleans match the value
                an empty list is returned.
        """
        if value is True:
            return [arg_true]
        elif value is False:
            return [arg_false]

        return []

    def _validate_source(self, value):
        """
        Validate given source path value exists on filesystem.

        Raises:
            CommandArgumentsError: If path validation fails, this exception is raised.

        Arguments:
            value (string or Path): The path to check against.

        Returns:
            Path: A Path object from given value.
        """
        path = Path(value)

        if not path.exists():
            msg = "Given source path does not exist: {}"
            raise CommandArgumentsError(msg.format(path))

        return path

    def _validate_destination(self, value):
        """
        This should validation destination path.

        However we can"t validate anything since Python os/pathlib need an existing
        ressource to check if it is a dir or not. But destination may not exists if it
        is a file.

        Returns:
            Path: A Path object from given value.
        """
        return Path(value)

    def _validate_style(self, value):
        """
        Validate given style value is an available choice.

        Raises:
            CommandArgumentsError: If value is not an available choice.

        Arguments:
            value (string or Path): The value to check against style choices.

        Returns:
            list: List with argument according to the value.
        """
        if value not in self.VALUE_CHOICES["style"]:
            msg = "Invalid given output style '{value}', it should be one of: {names}"
            raise CommandArgumentsError(msg.format(
                value=value,
                names=", ".join(self.VALUE_CHOICES["style"]),
            ))

        return [self.get_available_parameters()["style"], value]

    def _validate_charset(self, value):
        """
        Create arguments for given charset flag

        Arguments:
            value (boolean): If True enable the 'charset' argument, if False enable
                the 'no-charset' argument. Else nothing is done.

        Returns:
            list: List with argument according to the value.
        """
        return self.validate_boolean_flag(
            value,
            self.get_available_parameters()["charset"][0],
            self.get_available_parameters()["charset"][1],
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

    def _validate_load_path(self, value):
        """
        Create an argument ``load-path`` for each given path.

        Arguments:
            value (list): A list of path to add as argument ``load-path``. Each path
                must exists on filesystem.

        Raises:
            CommandArgumentsError: If some paths does not exists, a list of invalid
                paths are given in a message.

        Returns:
            list: List with all arguments for given path.
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
            paths.extend([self.get_available_parameters()["load_path"], str(item)])

        return paths
