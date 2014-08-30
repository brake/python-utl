# -*- coding: UTF-8 -*-
#-------------------------------------------------------------------------------
# Name:    misc.py        
# Package: utl
# Project: utl     
#
# Created: 28.08.14 18:13    
# Copyright:  (c) Constantin Roganov, 2014 
# Licence:    The MIT License
#-------------------------------------------------------------------------------
#!/usr/bin/env python

"""Uncategorized utilities"""

__author__ = 'Constantin Roganov'

import collections
import contextlib as cont


def flatten(iterable):
    """Generator of flattened sequence from input iterable.

    iterable can contain scalars and another iterables.
    [1, 2, 3, 4, [[[5, 6], 7]], 8, [9]] -> [1, 2, 3, 4, 5, 6, 7, 8, 9]

    >>> list(flatten([1, 2, 3, 4, [[[5, 6], 7]], 8, [9]]))
    [1, 2, 3, 4, 5, 6, 7, 8, 9]

    >>> list(flatten(1))
    Traceback (most recent call last):
    ...
    TypeError: 'int' object is not iterable
    """
    for e in iterable:
        if isinstance(e, collections.Iterable):
            for i in flatten(e):
                yield i
        else:
            yield e


@cont.contextmanager
def ignored(*exceptions):
    """Create context manager ignoring exceptions from input sequence

    >>> with ignored(TypeError):
    ...     'aaa' / 4


    >>> with ignored(ValueError):
    ...     'aaa' / 4
    Traceback (most recent call last):
    ...
    TypeError: unsupported operand type(s) for /: 'str' and 'int'

    """
    try:
        yield
    except exceptions:
        pass


class Singleton(type):
    """Meta class for Singleton creation

    >>> class A(object):
    ...    __metaclass__ = Singleton

    >>> a1 = A()

    >>> a2 = A()

    >>> id(a1) == id(a2)
    True
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)

        return cls._instances[cls]

if __name__ == '__main__':

    import doctest
    doctest.testmod()


