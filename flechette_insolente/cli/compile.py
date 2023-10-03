import logging

import click

from ..compiler import DartSassCompiler
# from ..exceptions import RunnedCommandError


from flechette_insolente.compiler import lazy_type, ArgumentsModel

CLICK_COERCE_TYPES = {
    "choice": click.Choice,
    "path": click.Path,
}


def add_arguments(arguments, options):
    """
    Given a list of click options this creates a decorator that
    will return a function used to add the options to a click command.

    :param options: a list of click.options decorator.
    """
    def _add_arguments(func):
        """
        Given a click command and a list of click options this will
        return the click command decorated with all the options in the list.

        :param func: a click command function.
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


@click.command()
@add_arguments(
    ArgumentsModel.get_cli_arguments(CLICK_COERCE_TYPES),
    ArgumentsModel.get_cli_options(CLICK_COERCE_TYPES),
)
@click.pass_context
def compile_command(context, **kwargs):
    """
    Compile Sass sources to CSS with dart-sass compiler.
    """
    logger = logging.getLogger("flechette-insolente")

    source = kwargs["source"]
    destination = kwargs["destination"]
    style = kwargs["style"]
    load_path = kwargs["load_path"]
    indented = kwargs["indented"]
    source_map = kwargs["source_map"]

    logger.debug("source: {}".format(source))
    logger.debug("destination: {}".format(destination))
    logger.debug("style: {}".format(style))
    logger.debug("load_path: {}".format(load_path))
    logger.debug("indented: {}".format(indented))
    logger.debug("source_map: {}".format(source_map))

    compiler = DartSassCompiler()

    logger.info("Foo.")
