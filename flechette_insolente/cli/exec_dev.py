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
            "result:", compiler.exit_1()
        )
    except RunnedCommandError as e:
        print("detail:", e.get_payload_details())
        print("error:", e)

    print()
    print("-"*40)
    print()

    try:
        print(
            "result:", compiler.exit_2()
        )
    except RunnedCommandError as e:
        print("detail:", e.get_payload_details())
        print("error:", e)

    print()
    print("-"*40)
    print()

    try:
        print(
            "result:", compiler.colored_error()
        )
    except RunnedCommandError as e:
        print("detail:", e.get_payload_details())
        print("error:", e)

    print()
    print("-"*40)
    print()

    compiler = DartSassCompiler(command_timeout=1)
    try:
        print(
            "result:", compiler.sleepy_error()
        )
    except RunnedCommandError as e:
        print("detail:", e.get_payload_details())
        print("error:", e)

    print()
    print("-"*40)
    print()

    error = None
    try:
        compiler_version = compiler.version()
    except RunnedCommandError as e:
        error = e

    if error:
        print("detail:", error.get_payload_details())
        print("error:", error)
    else:
        print("result:", compiler_version)
