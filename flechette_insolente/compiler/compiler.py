from .executable import ExecutableAbstract
from .arguments import ArgumentsModel


class DartSassCompiler(ExecutableAbstract):
    """
    This is the wrapper interface for dart-sass executable compiler.
    """

    def version(self):
        result = self._exec("--version")

        return result.stdout.strip()

    def compile(self, *args, **kwargs):
        """
        TODO

        Arguments:
            source (pathlib.Path):

        Keyword Arguments:
            destination (pathlib.Path):
            load_paths (list):

        Returns:
            string:
        """
        args_model = ArgumentsModel(*args, **kwargs)

        result = self._exec(*args_model.cmd_args)

        return result.stdout.strip()
