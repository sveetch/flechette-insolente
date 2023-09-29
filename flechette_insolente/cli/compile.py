import logging

import click

from ..compiler import DartSassCompiler
# from ..exceptions import RunnedCommandError


@click.command()
@click.pass_context
def compile_command(context):
    """
    R&D on managing subprocess success and failure from command execution
    """
    logger = logging.getLogger("flechette-insolente")

    compiler = DartSassCompiler()
    compiler.version()

    logger.info("Foo.")
