#!/usr/bin/env python 
# -*- coding: UTF-8 -*-
# ------------------------------------------------------------------------------
# Name:    test_hex.py       
# Package: test
# Project: python-utl
# 
# Created: 24.01.2018 20:19   
# Copyright 2018 © Constantin Roganov
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

"""Tests for utl.hex"""

import unittest
import binascii

from utl.hex import *


class TestHexStrToBytesList(unittest.TestCase):

    hex_string = 'DDFFAA33'
    malformed_hex_string = 'DDFFAA3'
    expected_result = [221, 255, 170, 51]

    def test_empty_string(self):
        with self.assertRaises(TypeError):
            hexstr2bytes_list('')

    def test_with_None(self):
        with self.assertRaises(TypeError):
            hexstr2bytes_list(None)

    def test_ok(self):
        self.assertListEqual(hexstr2bytes_list(self.hex_string), self.expected_result)

    def test_malformed(self):
        with self.assertRaises(binascii.Error):
            hexstr2bytes_list(self.malformed_hex_string)


class TestBytesListToBin(unittest.TestCase):

    input_data = [221, 255, 170, 51]
    invalid_input_data = [221, 255, 1700, 51]
    expected_result = b'\xdd\xff\xaa3'

    def test_ok(self):
        result = bytes_list2bin(self.input_data)
        self.assertEqual(result, self.expected_result)

    def test_invalid_byte_in_list(self):
        with self.assertRaises(UnicodeEncodeError):
            bytes_list2bin(self.invalid_input_data)


class TestBytesListToHexStr(unittest.TestCase):

    input_data = [221, 255, 170, 51]
    invalid_input_data = [221, 255, 1700, 51]
    expected_result = 'DDFFAA33'

    def test_ok(self):
        result = bytes_list2hexstr(self.input_data)
        self.assertEqual(result, self.expected_result)

    def test_upper_case_ok(self):
        result = bytes_list2hexstr(self.input_data, True)
        self.assertEqual(result, self.expected_result.upper())

    def test_lower_case_ok(self):
        result = bytes_list2hexstr(self.input_data, False)
        self.assertEqual(result, self.expected_result.lower())

    def test_with_invalid_input_byte(self):
        with self.assertRaises(UnicodeEncodeError):
            bytes_list2hexstr(self.invalid_input_data)


class TestIsHexString(unittest.TestCase):

    valid_hex_str = 'DDFFAA33'
    invalid_hex_str = 'failing_test'

    def test_true(self):
        self.assertTrue(is_hexstr(self.valid_hex_str))

    def test_false(self):
        self.assertFalse(is_hexstr(self.invalid_hex_str))


class TestSwapNibbles(unittest.TestCase):

    valid_input = 'd1c1a1b1'
    expected_result = '1d1c1a1b'
    invalid_input = 'd1c1a1b'
    not_hex_valid_input = 'TSNXWZ'
    not_hex_expected_result = 'STXNZW'

    def test_ok(self):
        result = swap_nibbles(self.valid_input)
        self.assertEqual(self.expected_result, result)

    def test_invalid_input(self):
        with self.assertRaises(ValueError):
            swap_nibbles(self.invalid_input)

    def test_not_hex_input(self):
        result = swap_nibbles(self.not_hex_valid_input)
        self.assertEqual(self.not_hex_expected_result, result)

