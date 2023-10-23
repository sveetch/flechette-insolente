from ..arguments import ArgumentsModel

from .executable import ExecutableAbstract


class DartSassCompiler(ExecutableAbstract):
    """
    This is the wrapper interface for dart-sass executable compiler.
    """

    def version(self):
        result = self._exec("--version")

        return result.stdout.strip()

    def compile(self, *args, **kwargs):
        """
        Execute compiler command with given arguments.

        Arguments:
            *args:
            *kwargs:

        Returns:
            string: Command response from standard output.
        """
        args_model = ArgumentsModel(*args, **kwargs)

        result = self._exec(*args_model.cmd_args)

        return result.stdout.strip()
