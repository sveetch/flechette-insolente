from pathlib import Path

from dartsass.exceptions import CommandArgumentsError


class ArgumentsAbstract:
    """
    Object to receive and validate arguments to produce normalized argument for
    dart-sass executable.

    TODO: Use more specific exceptions.

    Sample usage for source and destination:

    Only source is given as a file, compiled to css into the same dir than source: ::

        trying/
        ├── bar.css
        ├── bar.css.map
        ├── css
        └── scss
            └── sample.scss

    Source and destination given as files, packed with ":", CSS compiled at the
    destination: ::

        $ dartsass/vendor/linux-x64/sass trying/scss/sample.scss:trying/css/foo.css
        $ tree trying/
        trying/
        ├── bar.css
        ├── bar.css.map
        ├── css
        │   ├── foo.css
        │   └── foo.css.map
        └── scss
            └── sample.scss

    Source given as a file and destination as a dir, lead to error,
    package source/destination must be the same file type: ::

        $ dartsass/vendor/linux-x64/sass trying/scss/sample.scss:trying/css/
        Error reading trying/css: Cannot open file.

    Source and destination given as directories, All Sass from source dir are compiled
    to CSS into the given destination dir. HINT: If destination directory does not
    exists yet, compiler will creating it.

        $ dartsass/vendor/linux-x64/sass trying/scss/:trying/css/
        $ tree trying/
        trying/
        ├── bar.css
        ├── bar.css.map
        ├── css
        │   ├── foo.css
        │   ├── foo.css.map
        │   ├── sample.css
        │   └── sample.css.map
        └── scss
            └── sample.scss
    """
    AVAILABLE_ARGUMENTS = {
        "source": None,
        "destination": None,
        "style": "--style",
        "load_paths": "--load-path",
    }

    def __init__(self, source, **kwargs):
        self.destination = None

        # Get source path
        self.source = self._validate_source(source)
        sources = [str(self.source)]

        # Get optional destination path
        destination = kwargs.pop("destination", None)
        if destination:
            self.destination = self._validate_destination(destination)
            sources.append(str(self.destination))

        # Start argument with gathered ressource paths
        self.cmd_args = [":".join(sources)]

        for name, value in kwargs.items():
            #print("-", name, value)
            if name not in self.AVAILABLE_ARGUMENTS:
                raise CommandArgumentsError("Unknowed argument: {}".format(name))
            else:
                content = getattr(self, "_validate_{}".format(name))(value)
                if content:
                    self.cmd_args.extend(content)

    def __str__(self):
        return " ".join(self.cmd_args)

    def _validate_source(self, value):
        path = Path(value)

        if not path.exists():
            msg = "Given source path does not exist: {}"
            raise CommandArgumentsError(msg.format(path))

        return path

    def _validate_destination(self, value):
        """
        Note:
        We can"t validate anything since Python os/pathlib need an existing ressource
        to check if it is a dir or not. But destination may not exists if it is a file.
        """
        return Path(value)

    def _validate_style(self, value):
        """
        Create a ``--style`` argument for given style name.

        TODO: Validate style from available choice (to be synchronized with dart-sass
        spec)
        """
        return [self.AVAILABLE_ARGUMENTS["style"], value]

    def _validate_load_paths(self, value):
        """
        Create a ``--load-path`` argument for each given path.

        TODO: Validate each given path exists
        """
        paths = []
        for item in value:
            paths.extend([self.AVAILABLE_ARGUMENTS["load_paths"], item])
        return paths
