from pathlib import Path

import pytest

from dartsass.exceptions import AppOperationError


class CompilerArgumentsModel:
    """
    Sample usage for source and destination:

    Only source is given as a file, compiled to css into the same dir than source: ::

        trying/
        ├── bar.css
        ├── bar.css.map
        ├── css
        └── scss
            └── sample.scss

    Source and destination given as files, packed with ':', CSS compiled at the
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
    to CSS into the given destination dir

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
        self.cmd_args = []
        self.destination = None

        self.source = self._validate_source(source)

        destination = kwargs.pop("destination")
        if destination:
            self.destination = self._validate_destination(source)

        for name, value in kwargs.items():
            print("-", name, value)
            if name not in self.AVAILABLE_ARGUMENTS:
                raise AppOperationError("Unknowed argument: {}".format(name))
            else:
                content = getattr(self, "_validate_{}".format(name))(value)
                if content:
                    self.cmd_args.extend(content)

    def __str__(self):
        print(self.cmd_args)
        return " ".join(self.cmd_args)

    def _validate_source(self, value):
        path = Path(value)
        if not path.exists():
            raise AppOperationError("Given source path does not exist: {}".format(path))

        return [path]

    def _validate_destination(self, value):
        return [value]

    def _validate_style(self, value):
        return [self.AVAILABLE_ARGUMENTS["style"], value]

    def _validate_load_paths(self, value):
        paths = []
        for item in value:
            paths.extend([self.AVAILABLE_ARGUMENTS["load_paths"], item])
        return paths


def test_default_name(scss_structure, settings):
    """
    TODO: R&D the model
    """

    print([i for i in settings.datas_path.iterdir()])

    # Source does not exist
    with pytest.raises(AppOperationError) as excinfo:
        model = CompilerArgumentsModel(
            source="foo.css",
        )

    # Invalid argument
    with pytest.raises(AppOperationError) as excinfo:
        model = CompilerArgumentsModel(
            source="foo.css",
            michou=True
        )

    model = CompilerArgumentsModel(
        source="foo.css",
        destination="dist/",
        load_paths=["../node_modules/bootstrap"],
        style="expanded",
        #michou=True
    )
    print()
    print(model)
    print()

    assert 1 == 42
