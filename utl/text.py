#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# ------------------------------------------------------------------------------
# Name:    text.py
# Package: utl
# Project: utl
#
# Created: 18.02.14 13:27
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


"""Text utilities"""

from __future__ import unicode_literals, absolute_import, print_function
from builtins import *
from future.standard_library import install_aliases
install_aliases()

import collections
import itertools

__author__ = 'Constantin Roganov'


ParseStats = collections.namedtuple('ParseStats', ('read', 'processed'))


def chunk(s, p):
    r"""Split string s into sections with size p.

    >>> chunk('aaabbbcccdddeee', 3)
    [u'aaa', u'bbb', u'ccc', u'ddd', u'eee']

    >>> chunk('aaaabbbbccccee', 4)
    [u'aaaa', u'bbbb', u'cccc', u'ee']

    >>> chunk('aaa', 4)
    [u'aaa']

    """
    return list(map(''.join, itertools.zip_longest(*[iter(s)] * p, fillvalue='')))


def lines_stripped(iterable, chars=None):
    r"""Return Iterable object containing lines from input iterable with strip(chars) applied.

    >>> list(lines_stripped([' aaa ', '\tbbb\n', 'ccc']))
    [u'aaa', u'bbb', u'ccc']

    >>> list(lines_stripped(['xaaax', '  bbb', '__ccc__'], 'x_'))
    [u'aaa', u'  bbb', u'ccc']

    >>> l = [u'aaa', u'bbb', u'ccc']
    >>> list(lines_stripped(l)) == l
    True

    """
    return map(lambda s: s.strip(chars), iterable)


def lines_uncommented(iterable, comments=(';', '#')):
    """Return Iterable object containing only lines from iterable which didn't begin with comment.

    >>> lines = ('aaa', '; bbb', '#ccc ', 'ddd')
    >>> list(lines_uncommented(lines))
    [u'aaa', u'ddd']

    >>> lines = ('** aaa', '*bbb', '#ccc ', ' ddd')
    >>> list(lines_uncommented(lines, ('**', ' ')))
    [u'*bbb', u'#ccc ']

    """
    return itertools.filterfalse(lambda s: s.startswith(comments), iterable)


def lines_parser(iterable, parse_line):
    """Generator of pairs:

        - ParseStats
        - result of applying parse_line() function to text line from iterable.

    parse_line() should return None if parsing of some line fails. In this case generator will not yield
        anything but will switch to next line.

    >>> def parse_line(line):
    ...     if line.startswith(' '):
    ...         return None
    ...     return True if line else False
    >>> lines = ('', 'aaa', 'bbb', ' ccc')
    >>> list(lines_parser(lines, parse_line))
    [(ParseStats(read=1, processed=1), False), (ParseStats(read=2, processed=2), True), (ParseStats(read=3, processed=3), True)]

    >>> def parse_line(line):
    ...     if line.startswith(' '):
    ...         return None
    ...     return True if line else False
    >>> lines = ('', 'aaa', ' ccc', 'bbb')
    >>> list(lines_parser(lines, parse_line))
    [(ParseStats(read=1, processed=1), False), (ParseStats(read=2, processed=2), True), (ParseStats(read=4, processed=3), True)]
    """

    processed = 0

    for i, res in enumerate(map(parse_line, iterable), start=1):

        if res is not None:
            processed += 1
            yield ParseStats(i, processed), res


def progress_co(justify=75):
    r"""Print some processing state to console. Return a generator.

    Usage example:
        progress = progress_co()
        progress.send((filename, lines_read, lines_total, lines_processed))
        ...
        progress.send(lines_saved)

    >>> progress = progress_co(0)
    >>> progress.send(('file.txt', 3, 7, 1))   #doctest: +NORMALIZE_WHITESPACE
    file.txt 3/7 (processed: 1)  Lines saved: 0
    >>> progress.send(100)                     #doctest: +NORMALIZE_WHITESPACE
    file.txt 3/7 (processed: 1)  Lines saved: 100
    >>> progress.send(('another_file.txt', 0, 10, 0))  #doctest: +NORMALIZE_WHITESPACE
         Done!
    another_file.txt 0/10 (processed: 0)  Lines saved: 100

    """
    def inner():
        info_dict = {'saved_lines': 0}

        saved_name = ''
        while True:
            # input can be integer or tuple (name, read, lines_total, processed)
            info = yield

            if isinstance(info, (int, long)):
                info_dict['saved_lines'] += info

            else:
                info_dict.update(zip(('name', 'read', 'lines_total', 'processed'), info))

                if info_dict['name'] != saved_name:
                    if saved_name:
                        print(' Done!')

                    saved_name = info_dict['name']

            print('\r{name} {read:n}/{lines_total:n} (processed: {processed:n})  Lines saved: {saved_lines:n}'.format(
                **info_dict
            ).ljust(justify), end='')

    gen = inner()
    gen.next()

    return gen


if __name__ == '__main__':
    import doctest
    doctest.testmod()

