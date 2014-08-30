# -*- coding: UTF-8 -*-
#-------------------------------------------------------------------------------
# Name:    file.py        
# Package: utl
# Project: utl
#
# Created: 10.10.13 11:37    
# Copyright:  (c) Constantin Roganov, 2013 
# Licence:    The MIT License
#-------------------------------------------------------------------------------
#!/usr/bin/env python

"""File related utilities"""

__author__ = 'Constantin Roganov'


import os
import os.path
import fileinput as filein
import functools
import codecs

from . import text

binary_file = functools.partial(open, mode='rb')
binary_file.__doc__ = 'Open binary file for reading'

writable_binary_file = functools.partial(open, mode='wb')
writable_binary_file.__doc__ = 'Open binary file for writing'

text_file = functools.partial(open, mode='r')
text_file.__doc__ = 'Open text file for reading'

writable_text_file = functools.partial(open, mode='w')
writable_text_file.__doc__ = 'Open text file for writing'

utf8_bom_text_file = functools.partial(codecs.open, mode='r', encoding='utf_8_sig')
utf8_bom_text_file.__doc__ = 'Open UTF8 text file with BOM for reading'


def file_lines_count(filename):
    """Count lines in a text file"""
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
    if not lines and file_has_data:
        lines = 1

    return lines


def _rblocks(f, blocksize=4096):
    """Read file as series of blocks from end of file to start.

    The data itself is in normal order, only the order of the blocks is reversed.
    ie. "hello world" -> ["ld","wor", "lo ", "hel"]
    Note that the file must be opened in binary mode.
    """
# source:
# http://cybervadim.blogspot.ru/2009/10/reverse-file-iterator-in-python.html

    if 'b' not in f.mode.lower():
        raise Exception("File must be opened using binary mode.")

    size = os.stat(f.name).st_size
    fullblocks, lastblock = divmod(size, blocksize)

    # The first(end of file) block will be short, since this leaves
    # the rest aligned on a blocksize boundary.  This may be more
    # efficient than having the last (first in file) block be short
    f.seek(-lastblock, 2)
    yield f.read(lastblock)

    for i in xrange(fullblocks - 1, -1, -1):
        f.seek(i * blocksize)
        yield f.read(blocksize)


def rlines(f, keepends=False):
    """Iterate through the lines of a file in reverse order.

    If keepends is true, line endings are kept as part of the line.
    """
# source:
# http://cybervadim.blogspot.ru/2009/10/reverse-file-iterator-in-python.html


    buf = ''
    for block in _rblocks(f):
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
    """Generator of parsed lines from each text file (path) in iterable.

    iterable - sequence of file paths or None (there sys.argv[1:] will be used)
    parse_line - callable for processing of single line
    progress_co - coroutine with API like below:
        progress_co = progress_generator()
        progress_co.send((filename, lines_read, lines_total, lines_processed))
        ...
        progress_co.send(lines_saved)  # finalizing work

    Generates output data in format produced by parse_line()
    """

    #for pth in text.lines_stripped(iterable):
    #    name = os.path.basename(pth)
    #    lines_total = file_lines_count(pth)
    #
    #    with open(pth) as fo:
    #        for stats, data in text.lines_parser(fo, parse_line=parse_line):
    #
    #            if progress_co:
    #                progress_co.send((name, stats.read, lines_total, stats.processed))
    #            yield data

    files = None if iterable is None else text.lines_stripped(iterable)

    inp = filein.input(files=files)

    pth, name, lines_total = (None, ) * 3

    for stats, data in text.lines_parser(text.lines_stripped(inp), parse_line):
        if inp.isfirstline() or inp.filename() != pth:
            pth = inp.filename()
            name = os.path.basename(pth)

            lines_total = file_lines_count(pth)

        if progress_co:
            progress_co.send((name, inp.filelineno(), lines_total, stats.processed))

        yield data


def offset_iter(fo):
    """Generator of pairs (offset_from_beginning_of_file, string) for file object 'fo'"""

    #source: http://bytes.com/topic/python/answers/855199-file-tell-loop

    tell = fo.tell
    readline = fo.readline

    while True:
        addr = tell()
        line = readline()

        if not line:
            break

        yield addr, line


if __name__ == '__main__':

    # def m1():
    #     fo = open("example.txt", 'rb')
    #     for line in rlines(fo):
    #         pass
    #
    # import timeit
    #
    # tmr = timeit.Timer('m1()', 'from __main__ import m1\ngc.enable()')
    # t = tmr.timeit(1)
    # h = t / 3600
    # m = (t % 3600) / 60
    # s = (t % 3600) % 60
    # print('', 'Execution time(%f): %02d:%02d:%f' % (t, h, m, s))

    import unittest

    class LinesCountTest(unittest.TestCase):

        lines_count = 100
        line_content = 'LinesCountTest %03d'
        file_name = 'LinesCountTest.txt'

        def setUp(self):

            with open(LinesCountTest.file_name, 'w') as fo:

                lines = []
                for i in range(LinesCountTest.lines_count):
                    lines.append(LinesCountTest.line_content % i)

                fo.write('\n'.join(lines))

        def tearDown(self):
            # os.remove(LinesCountTest.file_name)
            pass

        def test(self):

            self.assertEqual(
                LinesCountTest.lines_count - 1,
                file_lines_count(LinesCountTest.file_name)
            )

    unittest.main()
