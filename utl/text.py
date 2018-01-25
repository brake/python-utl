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

import sys

if sys.version_info[0] == 2:
    from future.standard_library import install_aliases
    install_aliases()

import collections
import itertools

__author__ = 'Constantin Roganov'


ParseStats = collections.namedtuple('ParseStats', ('read', 'processed'))


def chunk(s, p):
    """Split string s into sections with size p"""
    return list(map(''.join, itertools.zip_longest(*[iter(s)] * p, fillvalue='')))


def lines_stripped(iterable, chars=None):
    """Return Iterable object containing lines from input iterable with strip(chars) applied"""
    return map(lambda s: s.strip(chars), iterable)


def lines_uncommented(iterable, comments=(';', '#')):
    """Return Iterable object containing only lines from iterable which didn't begin with comment"""
    return itertools.filterfalse(lambda s: s.startswith(comments), iterable)


def lines_parser(iterable, parse_line):
    """Generator of pairs:

        - ParseStats
        - result of applying parse_line() function to text line from iterable.

    parse_line() should return None if parsing of some line fails. In this case generator will not yield
        anything but will switch to next line.
    """

    processed = 0

    for i, res in enumerate(map(parse_line, iterable), start=1):

        if res is not None:
            processed += 1
            yield ParseStats(i, processed), res


def progress_co(justify=75):
    """Print some processing state to console. Return a generator.

    Usage example:
        progress = progress_co()
        progress.send((filename, lines_read, lines_total, lines_processed))
        ...
        progress.send(lines_saved)
    """
    def inner():
        info_dict = {'saved_lines': 0}

        saved_name = ''
        while True:
            # input can be integer or tuple (name, read, lines_total, processed)
            info = yield

            # python 2 (long)
            # if isinstance(info, (int, long)):
            if isinstance(info, int):
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
    next(gen)

    return gen

