import logging

import click

from ..compiler import DartSassCompiler
from ..exceptions import RunnedCommandError


@click.command()
@click.pass_context
def execdev_command(context):
    """
    R&D on managing subprocess success and failure from command execution
    """
    logger = logging.getLogger("flechette-insolente")

    logger.warning("🚨 This is temporary R&D script.")
    compiler = DartSassCompiler()

    print()
    print("-"*40)
    print()

    try:
        print(
            compiler.exit_1()
        )
    except RunnedCommandError as e:
        print(e.get_payload_details())
        print(e)

    print()
    print("-"*40)
    print()

    try:
        print(
            compiler.exit_2()
        )
    except RunnedCommandError as e:
        print(e.get_payload_details())
        print(e)

    print()
    print("-"*40)
    print()

    try:
        print(
            compiler.colored_error()
        )
    except RunnedCommandError as e:
        print(e.get_payload_details())
        print(e)

    print()
    print("-"*40)
    print()

    compiler = DartSassCompiler(command_timeout=1)
    try:
        print(
            compiler.sleepy_error()
        )
    except RunnedCommandError as e:
        print(e.get_payload_details())
        print(e)

    print()
    print("-"*40)
    print()

    error = None
    try:
        compiler_version = compiler.version()
    except RunnedCommandError as e:
        error = e

    if error:
        print(error.get_payload_details())
        print(error)
    else:
        print(compiler_version)
