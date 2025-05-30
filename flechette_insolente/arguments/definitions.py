from pathlib import Path

from ..utils.lazy import lazy_type


VALUE_CHOICES = {
    "style": ("expanded", "compressed"),
    "source_map_urls": ("relative", "absolute"),
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
    "charset": {
        "args": ("--charset/--no-charset",),
        "kwargs": {
            "default": True,
            "help": (
                "Emit a @charset or BOM for CSS with non-ASCII characters."
            ),
        }
    },
    "embed_sources": {
        "args": ("--embed-sources/--no-embed-sources",),
        "kwargs": {
            "default": False,
            "help": (
                "Embed source file contents in source maps."
            ),
        }
    },
    "embed_source_map": {
        "args": ("--embed-source-map/--no-embed-source-map",),
        "kwargs": {
            "default": False,
            "help": (
                "Embed source map contents in CSS."
            ),
        }
    },
    "error_css": {
        "args": ("--error-css/--no-error-css",),
        "kwargs": {
            "default": True,
            "help": (
                "When an error occurs, emit a stylesheet describing it."
            ),
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
    "source_map": {
        "args": ("--source-map/--no-source-map",),
        "kwargs": {
            "default": True,
            "help": (
                "Whether to generate source maps."
            ),
        }
    },
    "source_map_urls": {
        "coerce_type": "choice",
        "args": ("--source-map-urls",),
        "kwargs": {
            "metavar": "STRING",
            "type": lazy_type(VALUE_CHOICES["source_map_urls"]),
            "help": (
                "How to link from source maps to source files."
            ),
            "show_default": True,
            "default": VALUE_CHOICES["source_map_urls"][0],
        }
    },
    "stop_on_error": {
        "args": ("--stop-on-error/--no-stop-on-error",),
        "kwargs": {
            "default": True,
            "help": (
                "Don't compile more files once an error is encountered."
            ),
        }
    },
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
    "update": {
        "args": ("--update",),
        "kwargs": {
            "default": False,
            "help": (
                "Only compile out-of-date stylesheets."
            ),
        }
    },
}
"""
Available click options, note than Click use the "args" item to name the parameter.
"""
