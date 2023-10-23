from pathlib import Path

from ..utils.lazy import lazy_type


VALUE_CHOICES = {
    "style": ("expanded", "compressed"),
}
"""
Available choices for 'style' option
"""


COMMAND_ARGUMENTS = {
    "source": {
        "coerce_type": "path",
        "kwargs": {
            "type": lazy_type(
                file_okay=True, dir_okay=True, writable=True, resolve_path=False,
                path_type=Path, exists=True,
            ),
            "required": True,
        }
    },
    "destination": {
        "coerce_type": "path",
        "kwargs": {
            "type": lazy_type(
                file_okay=True, dir_okay=True, writable=True, resolve_path=False,
                path_type=Path,
            ),
            "required": False,
        }
    },
}
"""
Available click arguments, note than the item name is used to name the argument
to Click
"""

COMMAND_OPTIONS = {
    "style": {
        "coerce_type": "choice",
        "args": ("--style",),
        "kwargs": {
            "metavar": "STRING",
            "type": lazy_type(VALUE_CHOICES["style"]),
            "help": (
                "Output style."
            ),
            "show_default": True,
            "default": VALUE_CHOICES["style"][0],
        }
    },
    "load_path": {
        "coerce_type": "path",
        "args": ("--load-path",),
        "kwargs": {
            "metavar": "PATH",
            "type": lazy_type(
                file_okay=False, dir_okay=True, writable=True, resolve_path=False,
                path_type=Path, exists=True,
            ),
            "multiple": True,
            "help": (
                "A path to use when resolving imports. May be passed multiple "
                "times."
            ),
        }
    },
    # Not sure about this option since it only mention stdin, is that only common
    # shell standard input ? If so, remove it since we won't support it (yet?).
    "indented": {
        "args": ("--indented/--no-indented",),
        "kwargs": {
            "default": None,
            "help": (
                "Use the indented syntax for input from stdin."
            ),
        }
    },
    "source_map": {
        "args": ("--source-map/--no-source-map",),
        "kwargs": {
            "default": True,
            "help": (
                "Whether to generate source maps."
            ),
        }
    },
}
"""
Available click options, note than Click use the "args" item to name the value
"""
