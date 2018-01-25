#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# ------------------------------------------------------------------------------
# Name:    hex.py
# Package: utl
# Project: utl
#
# Created: 10.10.13 11:43
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


"""Hex string to binary conversions and vice versa"""


from __future__ import unicode_literals, absolute_import
from builtins import *

from binascii import hexlify, unhexlify, Error


__author__ = 'Constantin Roganov'


def hexstr2bytes_list(hexstr):
    """Convert the hex string to list of bytes"""
    if not hexstr:
        raise TypeError("hexstr2bytes_list: input must be a hex string, '{}' received".format(hexstr))
    # python 2
    # return list(map(ord, unhexlify(hexstr)))
    return [i for i in unhexlify(hexstr)]


def bytes_list2bin(bl):
    """Convert list of bytes to binary string"""
    return b''.join(chr(i).encode('latin-1') for i in bl)


def bytes_list2hexstr(bl, uppercase=True):
    """Convert list of bytes to hex string"""
    # python2
    # result = hexlify(bytes_list2bin(bl))
    result = bytes_list2bin(bl).hex()

    return result.upper() if uppercase else result


def is_hexstr(s):
    """Check a string s for presence a valid hexadecimal data"""
    try:
        unhexlify(s)
        return True

    except (TypeError, Error):
        return False


def swap_nibbles(s):
    r"""Swap nibbles in a hex string.
    len(s) must be even otherwise ValueError will be raised.


    """
    if len(s) % 2:
        raise ValueError('Odd-length string')
    return ''.join([y+x for x,y in zip(*[iter(s)] * 2)])


