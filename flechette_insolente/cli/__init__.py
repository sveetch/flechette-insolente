import click


# Available coerce type for Click
CLICK_COERCE_TYPES = {
    "choice": click.Choice,
    "path": click.Path,
}


def add_arguments(arguments, options):
    """
    A decorator which will attach parameters (arguments and options) to a command
    function.

    Arguments:
        arguments (dict): Dictionnary of arguments descriptions, commonly what is
            returned from method ``ArgumentsModel.get_cli_arguments``.
        options (dict): Dictionnary of arguments options, commonly what is
            returned from method ``ArgumentsModel.get_cli_options``.

    Returns:
        function: The embedded function which will attach parameters to the function
        which is decorated.
    """
    def _add_arguments(func):
        """
        Given a click command and a list of click options this will
        return the click command decorated with all the options in the list.

        :param func: a click command function.

        Arguments:
            func (function):

        Returns:
            function:
        """
        for name, values in reversed(options.items()):
            func = click.option(
                *values.get("args", []),
                **values.get("kwargs", {})
            )(func)

        for name, values in reversed(arguments.items()):
            func = click.argument(
                name,
                **values.get("kwargs", {})
            )(func)

        return func

    return _add_arguments
