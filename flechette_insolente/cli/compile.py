import logging

import click

from ..compiler import ArgumentsModel, DartSassCompiler
from ..exceptions import RunnedCommandError

from . import CLICK_COERCE_TYPES, add_arguments


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
    try:
        output = compiler.compile(
            source,
            destination=destination,
            style=style,
            indented=indented,
            source_map=source_map,
            load_path=load_path,
        )
    except RunnedCommandError as e:
        print(e.get_payload_details())
        logger.critical(e)
        raise click.Abort()
    else:
        click.echo(output)
