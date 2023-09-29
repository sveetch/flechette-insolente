import logging

import pytest

from click.testing import CliRunner

from dartsass import __pkgname__
from dartsass.cli.entrypoint import cli_frontend


@pytest.mark.skip
def test_compile_basic(caplog):
    """
    TODO
    - Test compiler directly before
    - CLI "compile" does not implement compiler yet
    - Need to create structure and point to it for source/destination/etc

    """
    runner = CliRunner()

    # Invoke the commandline from the CliRunner
    result = runner.invoke(cli_frontend, ["compile"])

    # To debug logs on fail
    # Commandline full output
    print("=> result.output <=")
    print(result.output)
    print()
    # Recorded logs as tuples
    print("=> caplog.record_tuples <=")
    print(caplog.record_tuples)
    print()
    # Raise possible exception from commandline, useful when there is an
    # unexpected exception during execution
    print("=> result.exception <=")
    print(result.exception)
    if result.exception:
        raise result.exception

    # Success signal from execution
    assert result.exit_code == 0

    # Expected basic output
    assert result.output == "Hello world!\n"

    # Empty logs is expected
    assert caplog.record_tuples == []
