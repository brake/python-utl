#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# ------------------------------------------------------------------------------
# Name:    file.py
# Package: utl
# Project: utl
#
# Created: 10.10.13 11:37
# Copyright 2013-2016 © Constantin Roganov
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


"""File related utilities"""

from __future__ import absolute_import, unicode_literals, print_function
from builtins import *

import os
import os.path
import fileinput
import functools

from . import text

__author__ = 'Constantin Roganov'


binary_file = functools.partial(open, mode='rb')
binary_file.__doc__ = 'Open binary file for reading'

writable_binary_file = functools.partial(open, mode='wb')
writable_binary_file.__doc__ = 'Open binary file for writing'

text_file = functools.partial(open, mode='r')
text_file.__doc__ = 'Open text file for reading'

writable_text_file = functools.partial(open, mode='w')
writable_text_file.__doc__ = 'Open text file for writing'

utf8_bom_text_file = functools.partial(open, mode='r', encoding='utf_8_sig')
utf8_bom_text_file.__doc__ = 'Open UTF8 text file with BOM for reading'


def file_lines_count(filename):
    r"""Count lines in a text file.

    >>> file_name = 'LinesCountTest.txt'
    >>> def create_test_file():
    ...     with writable_text_file(file_name) as fd:
    ...         for i in range(100):
    ...             fd.write('LinesCountTest {:03d}\n'.format(i))
    ...         fd.write('final line')
    >>> create_test_file()
    >>> file_lines_count(file_name)
    101

    >>> file_name = 'LinesCountTest.txt'
    >>> from os import remove; remove(file_name)  # doctest: -SKIP
    >>> def create_test_file():
    ...     with writable_text_file(file_name):
    ...         pass
    >>> create_test_file()
    >>> file_lines_count(file_name)
    0

    >>> file_name = 'LinesCountTest.txt'
    >>> from os import remove; remove(file_name)  # doctest: -SKIP
    >>> def create_test_file():
    ...     with writable_text_file(file_name) as fd:
    ...         fd.write('single test line')
    >>> create_test_file()
    >>> file_lines_count(file_name)
    1

    >>> file_name = 'LinesCountTest.txt'
    >>> from os import remove; remove(file_name)  # doctest: -SKIP
    """
# source:
#  http://stackoverflow.com/questions/845058/how-to-get-line-count-cheaply-in-python

    f = open(filename)
    lines = 0
    buf_size = 1024 * 1024
    read_f = f.read  # loop optimization

    file_has_data = False

    buf = read_f(buf_size)
    if buf:
        file_has_data = True

    while buf:
        lines += buf.count('\n')
        buf = read_f(buf_size)

    # nonempty file has 1 line at least
    if file_has_data:
        lines += 1

    return lines


def _reverse_blocks_generator(fd, block_size=4096):
    r"""Return generator which reads file as series of blocks from the tail of file up to to head.

    The data itself is in normal order, only the order of the blocks is reversed.
    ie. "hello world" -> ["ld","wor", "lo ", "hel"]
    Note that the file must be opened in binary mode.

    >>> file_name = 'ReverseBlocksTest.txt'
    >>> block_size = 4
    >>> line = '111122223333444'
    >>> def create_test_file():
    ...     with writable_text_file(file_name, encoding='ascii') as fd:
    ...         fd.write(line)
    >>> create_test_file()
    >>> with binary_file(file_name) as fd:
    ...     list(_reverse_blocks_generator(fd, block_size))
    ['444', '3333', '2222', '1111']

    >>> file_name = 'ReverseBlocksTest.txt'
    >>> line = '111122223333444'
    >>> def create_test_file():
    ...     with writable_text_file(file_name, encoding='ascii') as fd:
    ...         fd.write(line)
    >>> create_test_file()
    >>> with text_file(file_name) as fd:
    ...     list(_reverse_blocks_generator(fd))
    Traceback (most recent call last):
    ...
    TypeError: File must be opened in binary mode

    >>> from os import remove; remove(file_name)
    """
# source:
# http://cybervadim.blogspot.ru/2009/10/reverse-file-iterator-in-python.html

    if 'b' not in fd.mode.lower():
        raise TypeError('File must be opened in binary mode')

    size = os.stat(fd.name).st_size
    fullblocks, lastblock = divmod(size, block_size)

    # The first(end of file) block will be short, since this leaves
    # the rest aligned on a blocksize boundary.  This may be more
    # efficient than having the last (first in file) block be short
    fd.seek(-lastblock, os.SEEK_END)
    yield fd.read(lastblock)

    for i in range(fullblocks - 1, -1, -1):
        fd.seek(i * block_size)
        yield fd.read(block_size)


def reverse_lines(fd, keepends=False, block_size=4096):
    r"""Iterate through the lines of a file in reverse order.

    If keepends is true, line endings are kept as part of the line.
    Return generator.

    >>> file_name = 'ReverseLinesTest.txt'
    >>> block_size = 4
    >>> line = '1111\n2222\n3333\n444'
    >>> def create_test_file():
    ...     with writable_text_file(file_name, encoding='ascii') as fd:
    ...         fd.write(line)
    >>> create_test_file()
    >>> with binary_file(file_name) as fd:
    ...     list(reverse_lines(fd))
    [u'444', u'3333', u'2222', u'1111']

    >>> file_name = 'ReverseLinesTest.txt'
    >>> line = '1111\n2222\n3333\n444'
    >>> def create_test_file():
    ...     with writable_text_file(file_name, encoding='ascii') as fd:
    ...         fd.write(line)
    >>> create_test_file()
    >>> with binary_file(file_name) as fd:
    ...     list(reverse_lines(fd, True, block_size=3))
    [u'444', u'3333\n', u'2222\n', u'1111\n']

    >>> from os import remove; remove(file_name)
    >>> file_name = 'ReverseLinesTest.txt'
    >>> line = '1111\n2222\n3333\n444'
    >>> def create_test_file():
    ...     with writable_text_file(file_name, encoding='ascii') as fd:
    ...         fd.write(line)
    >>> create_test_file()
    >>> with text_file(file_name) as fd:
    ...     list(reverse_lines(fd))
    Traceback (most recent call last):
    ...
    TypeError: File must be opened in binary mode

    >>> from os import remove; remove(file_name)    """
# source:
# http://cybervadim.blogspot.ru/2009/10/reverse-file-iterator-in-python.html

    buf = ''
    for block in _reverse_blocks_generator(fd, block_size):
        buf = block + buf
        lines = buf.splitlines(keepends)
        # Return all lines except the first (since may be partial)
        if lines:
            lines.reverse()
            buf = lines.pop()  # Last line becomes end of new first line.
            for line in lines:
                yield line
    yield buf  # First line.


def filelist_processor(iterable, parse_line,  progress_co=None):
    r"""Generator of parsed lines from each text file (path) in iterable.

    iterable - sequence of file paths or None (there sys.argv[1:] will be used)
    parse_line - callable for processing of single line
    progress_co - coroutine with API like below:
        progress_co = progress_generator()
        progress_co.send((filename, lines_read, lines_total, lines_processed))
        ...
        progress_co.send(lines_saved)  # finalizing work

    Generates output data in format produced by parse_line()

    >>> name_template = 'filelist_proc_test{}.txt'
    >>> files = [name_template.format(i) for i in range(2)]
    >>> def create_file(name):
    ...     with writable_text_file(name) as fd:
    ...         for i in range(2):
    ...             fd.write('{} {}\n'.format(name, i))
    >>> for n in files:
    ...     create_file(n)
    >>> list(filelist_processor(files, lambda x: x))
    ['filelist_proc_test0.txt 0', 'filelist_proc_test0.txt 1', 'filelist_proc_test1.txt 0', 'filelist_proc_test1.txt 1']
    >>> from os import remove; [remove(n) for n in files]  # doctest: +ELLIPSIS
    [...]

    """

    files = None if iterable is None else text.lines_stripped(iterable)

    inp = fileinput.input(files=files)

    pth, name, lines_total = (None, ) * 3

    for stats, data in text.lines_parser(text.lines_stripped(inp), parse_line):
        if inp.isfirstline() or inp.filename() != pth:
            pth = inp.filename()
            name = os.path.basename(pth)

            lines_total = file_lines_count(pth)

        if progress_co:
            progress_co.send((name, inp.filelineno(), lines_total, stats.processed))

        yield data


def offset_iter(fd):
    r"""Generator of pairs (offset_from_beginning_of_file, string) for file object 'fd'.

    >>> file_name = 'OffserIterTest.txt'
    >>> line = '1111\n2222\n3333\n444'
    >>> def create_test_file():
    ...     with writable_text_file(file_name, encoding='ascii') as fd:
    ...         fd.write(line)
    >>> create_test_file()
    >>> from os import SEEK_SET
    >>> with binary_file(file_name) as fd:
    ...     offset, val = list(offset_iter(fd))[-1]
    >>> with binary_file(file_name) as fd:
    ...     _ = fd.seek(offset, SEEK_SET)
    ...     fd.readline() == val
    True
    >>> from os import remove; remove(file_name)

    """
    # source: http://bytes.com/topic/python/answers/855199-file-tell-loop

    tell = fd.tell
    readline = fd.readline

    while True:
        addr = tell()
        line = readline()

        if not line:
            break

        yield addr, line


