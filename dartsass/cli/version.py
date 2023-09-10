import click

from dartsass import __version__


@click.command()
@click.pass_context
def version_command(context):
    """
    Print out version information.
    """
    click.echo("flechette-insolente {}".format(__version__))
