from pathlib import Path

from ..exceptions import CommandArgumentsError


class ArgumentsValidationAbstract:
    """
    An abstract to include all argument validators. It need to work conjointly with
    ArgumentsModel.
    """
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
        if value not in self.VALUE_CHOICES["style"]:
            msg = "Invalid given output style '{value}', it should be one of: {names}"
            raise CommandArgumentsError(msg.format(
                value=value,
                names=", ".join(self.VALUE_CHOICES["style"]),
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

    def _validate_load_path(self, value):
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
            paths.extend([self.get_available_parameters()["load_path"], str(item)])

        return paths
