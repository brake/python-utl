#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# ------------------------------------------------------------------------------
# Name:    misc.py
# Package: utl
# Project: utl
#
# Created: 28.08.14 18:13
# Copyright 2014-2016 © Constantin Roganov
# License: The MIT License
# ------------------------------------------------------------------------------
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# ------------------------------------------------------------------------------


"""Uncategorized utilities"""

from __future__ import unicode_literals, absolute_import

import collections
import contextlib
import sys

__author__ = 'Constantin Roganov'


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


if sys.version_info[0] == 2:

    @contextlib.contextmanager
    def ignored(*exceptions):
        """Create context manager ignoring exceptions from input sequence

        >>> with ignored(TypeError):
        ...     'aaa' / 4


        >>> with ignored(ValueError):
        ...     'aaa' / 4                       # doctest: +ELLIPSIS
        Traceback (most recent call last):
        ...
        TypeError: unsupported operand type(s) ...

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


