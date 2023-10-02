import click

from flechette_insolente import __version__


@click.command()
@click.option(
    "--check",
    help=(
        "Include your plateform and dart-sass information."
    ),
    is_flag=True
)
@click.pass_context
def version_command(context, check):
    """
    Print out version information.
    """
    click.echo("flechette-insolente, version {}".format(__version__))

    if check:
        from ..compiler import DartSassCompiler
        from ..exceptions import RunnedCommandError
        from ..plateform_build import get_plateform, DART_SASS_EXEC

        compiler = DartSassCompiler()

        error = None
        compiler_version = "Unknow due to error"

        try:
            compiler_version = compiler.version()
        except RunnedCommandError as e:
            error = e

        system, machine = get_plateform()

        click.echo("- Plateform: {}-{}".format(system, machine))
        click.echo("- dart-sass executable: {}".format(DART_SASS_EXEC))
        click.echo("- dart-sass version: {}".format(compiler_version))

        if error:
            print(error.get_payload_details())
            print(error)
