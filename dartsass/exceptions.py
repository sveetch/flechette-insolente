"""
Specific application exceptions.
"""
from pathlib import Path


class FlechetteInsolenteBaseException(Exception):
    """
    Exception base.

    You should never use it directly except for test purpose. Instead make or
    use a dedicated exception related to the error context.
    """
    pass


class AppOperationError(FlechetteInsolenteBaseException):
    """
    Sample exception to raise from your code.
    """
    pass


class CommandArgumentsError(FlechetteInsolenteBaseException):
    """
    Exception for invalid command arguments
    """
    pass


class RunnedCommandError(FlechetteInsolenteBaseException):
    """
    A special error related to an executed commandline which failed.

    Attribute ``error_payload`` contains a dict of runned command details.

    Keyword Arguments:
        error_payload (dict): A dictionnary of command response error details. It
            won't output as exception message from traceback, you need to exploit it
            yourself if needed.
    """
    def __init__(self, *args, **kwargs):
        self.error_payload = kwargs.pop("error_payload", None)
        self.message = self.get_payload_message()
        super().__init__(*args, **kwargs)

    def get_payload_message(self):
        if self.error_payload:
            if self.error_payload.get("returncode"):
                return "Command failed with signal code: {}".format(
                    self.error_payload["returncode"]
                )
            elif self.error_payload.get("timeout"):
                return "Command exceeded timeout: {}".format(
                    self.error_payload["timeout"]
                )

        return "Unexpected error"

    def get_payload_details(self):
        if self.error_payload:
            cmd = self.error_payload.get("cmd", [])

            lines = [
                # Enforce string for possible Path objects
                " ".join([str(p) for p in cmd])
            ]

            if self.error_payload.get("stdout"):
                lines.append(self.error_payload.get("stdout"))

            if self.error_payload.get("stderr"):
                lines.append(self.error_payload.get("stderr"))

            return "\n\n".join([item for item in lines if item])

        return ""

    def __str__(self):
        return self.message
