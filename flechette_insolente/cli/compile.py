import logging

import click

from ..compiler import DartSassCompiler
# from ..exceptions import RunnedCommandError


@click.command()
@click.pass_context
def compile_command(context):
    """
    Compile Sass sources to CSS with dart-sass compiler.
    """
    logger = logging.getLogger("flechette-insolente")

    compiler = DartSassCompiler()
    compiler.version()

    logger.info("Foo.")
