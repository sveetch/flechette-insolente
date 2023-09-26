import subprocess
from pathlib import Path

import dartsass

from .exceptions import RunnedCommandError
from .plateform_build import DART_SASS_EXEC


class DebugExecVariance:
    """
    Temporary debug stuff used in exec_dev command
    """
    def exit_1(self):
        basepath = Path(dartsass.__file__).parent.parent / "tests/fixture_datas/scripts"
        result = self._exec(cmd_name=str(basepath / "./exit_1_sample.sh"))

        return result

    def exit_2(self):
        basepath = Path(dartsass.__file__).parent.parent / "tests/fixture_datas/scripts"
        result = self._exec(cmd_name=str(basepath / "./exit_2_sample.sh"))

        return result

    def colored_error(self):
        basepath = Path(dartsass.__file__).parent.parent / "tests/fixture_datas/scripts"
        result = self._exec(cmd_name=str(basepath / "./error_colored_sample.py"))

        return result

    def sleepy_error(self):
        basepath = Path(dartsass.__file__).parent.parent / "tests/fixture_datas/scripts"
        result = self._exec(cmd_name=str(basepath / "./error_sleepy_script.py"))

        return result


class DartSassCompiler(DebugExecVariance):
    """
    This should be the wrapper around dart-sass executable compiler.

    Start from libsass signature but it may not be suitable or accurate.
    """
    DEFAULT_COMMAND_TIMEOUT = 30

    def __init__(self, command_timeout=None):
        self.command_timeout = command_timeout or self.DEFAULT_COMMAND_TIMEOUT

    def _fix_bytes(self, content):
        """
        Workaround helper for a TimeoutExpired on stdout/stderr that does not honor
        ``text=True`` argument.
        """
        if isinstance(content, bytes):
            # Blindly assume user system enable UTF-8
            content = content.decode("UTF-8")

        return content

    def _exec(self, *args, **kwargs):
        """
        Execute command.
        """
        # One can override from kwargs the default executable command path to use
        # another one, mostly used for debug/test, maybe not accurate to keep it
        cmd_name = kwargs.get("cmd_name", DART_SASS_EXEC)

        try:
            result = subprocess.run(
                [cmd_name] + list(args),
                timeout=self.command_timeout,
                check=True,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
            )
        except subprocess.CalledProcessError as e:
            raise RunnedCommandError(error_payload={
                "returncode": e.returncode,
                "cmd": e.cmd,
                "stdout": e.stdout,
                "stderr": e.stderr,
                "timeout": None,
            })
        except subprocess.TimeoutExpired as e:
            # NOTE: For unknow reason, TimeoutExpired always keep an empty stdout
            raise RunnedCommandError(error_payload={
                "returncode": None,
                "cmd": e.cmd,
                "stdout": self._fix_bytes(e.stdout),
                "stderr": self._fix_bytes(e.stderr),
                "timeout": e.timeout,
            })
        else:
            return result

        return None

    def version(self):
        result = self._exec("--version")

        return result.stdout.strip()

    def compile(self, source, destination, load_paths=None):
        """
        sass --load-path=node_modules ./scss:../project/static-sources/css/

        Decomposed:
            sass
                --load-path=node_modules
                ./scss:../project/static-sources/css/

        Where
            sass
                --load-path=PATH
                source(file|dir):destination(file|dir)

        """
        cms_args = []
        load_paths = load_paths or []

        if load_paths:
            for path in load_paths:
                cms_args.extend(["--load-path", path])

        cms_args.extend([source, destination])

        result = self._exec(*cms_args)

        return result.stdout.strip()
