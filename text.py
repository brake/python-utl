# -*- coding: UTF-8 -*-
#-------------------------------------------------------------------------------
# Name:    text.py
# Package: utl
# Project: utl     
#
# Created: 18.02.14 13:27    
# Copyright:  (c) Constantin Roganov, 2014 
# Licence:    The MIT License
#-------------------------------------------------------------------------------
#!/usr/bin/env python

"""Text utilities"""

__author__ = 'Constantin Roganov'

import collections
import itertools


ParseStats = collections.namedtuple('ParseStats', ('read', 'processed'))

chunk = lambda s, p: map(type(s)('').join, zip(*[iter(s)] * p))
chunk.__doc__ = "Split string/unicode into sections with size p"


def lines_stripped(iterable, chars=None):
    """Return Iterable object containing lines from input iterable with strip(chars) applied"""

    return itertools.imap(lambda s: s.strip(chars), iterable)


def lines_uncommented(iterable, comments=(';', '#')):
    """Return Iterable object containing only lines from iterable which didn't begin with comment"""

    return itertools.ifilterfalse(lambda s: s.startswith(comments), iterable)


def lines_parser(iterable, parse_line):
    """Generator of pairs:

        - ParseStats
        - result of applying parse_line() function to text line from iterable.

    parse_line() should return None if parsing of some line fails. In this case generator will not yield
        anything but will switch to next line.
    """

    processed = 0

    for i, res in enumerate(itertools.imap(parse_line, iterable), start=1):

        if res:
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
            # int or
            # (name, read, lines_total, processed)
            info = yield

            if isinstance(info, (int, long)):
                info_dict['saved_lines'] += info

            else:
                info_dict.update(zip(('name', 'read', 'lines_total', 'processed'), info))

                if info_dict['name'] != saved_name:
                    if saved_name:
                        print ' Done!'

                    saved_name = info_dict['name']

            print '\r{name} {read:n}/{lines_total:n} (processed: {processed:n})  Lines saved: {saved_lines:n}'.format(
                **info_dict
            ).ljust(justify),

    gen = inner()
    gen.next()

    return gen


