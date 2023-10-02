import datetime
import json
from pathlib import Path


class DummyStr:
    """
    An object inheriting from this one will be recognized from ``ExtendedJsonEncoder``
    to just use the ``object.__str__`` method to represent it.
    """
    pass


class DummyRepr:
    """
    An object inheriting from this one will be recognized from ``ExtendedJsonEncoder``
    to just use the ``object.__repr__`` method to represent it.
    """
    pass


class ExtendedJsonEncoder(json.JSONEncoder):
    """
    Additional opiniated support for more basic object types.
    """
    def default(self, obj):
        if isinstance(obj, bytes):
            return obj.decode("utf-8")
        # Support for pathlib.Path to a string
        if isinstance(obj, Path):
            return str(obj)
        # Support for set to a list
        if isinstance(obj, set):
            return list(obj)
        # Support date, time and datetime to iso formatting
        if isinstance(obj, (datetime.datetime, datetime.date, datetime.time)):
            return obj.isoformat()
        # Support dummy objects
        if isinstance(obj, DummyStr):
            return str(obj)
        if isinstance(obj, DummyRepr):
            return repr(obj)

        # Let the base class default method raise the TypeError
        return json.JSONEncoder.default(self, obj)
