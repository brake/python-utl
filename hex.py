# -*- coding: UTF-8 -*-
#-------------------------------------------------------------------------------
# Name:    hex.py        
# Package: utl
# Project: utl     
#
# Created: 10.10.13 11:43    
# Copyright:  (c) Constantin Roganov, 2013 
# Licence:    The MIT License
#-------------------------------------------------------------------------------
#!/usr/bin/env python

"""Hex string to binary conversions and vice versa"""

__author__ = 'Constantin Roganov'

from binascii import hexlify, unhexlify


bin2hexstr = lambda bindata: hexlify(bindata).upper()

hexstr2bin = unhexlify
hexstr2bin_list = lambda hexstr: map(ord, hexstr2bin(hexstr))


def is_hexstr(s):
    """Check a string s for presence a valid hexadecimal data"""
    try:
        unhexlify(s)
        return True

    except TypeError:
        return False