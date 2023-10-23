
def lazy_type(*args, **kwargs):
    """
    Returns a callable to resolve object with args and kwargs if coerce_type is
    given.

    Arguments:
        *args: Positionnal argument to give to object type when coercing.
        *kwargs: Non positionnal arguments to give to object type when coercing.

    Returns:
        function: A callable function which expect optional ``coerce_type`` non
            positional argument which is a class object to use to coerce to. If not
            given, args and kwargs are just returned into a tuple.
    """
    def _curried(coerce_type=None):
        if not coerce_type:
            return args, kwargs

        return coerce_type(*args, **kwargs)

    return _curried
