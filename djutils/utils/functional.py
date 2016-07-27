# -*- coding: utf-8 -*-


def noop(*args, **kwargs):
    """A function that accepts any arguments and does nothing.
    It may be useful in a context where a function expects a callback but you
    don't want it to do anything.
    """
    return
