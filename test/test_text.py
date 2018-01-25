#!/usr/bin/env python 
# -*- coding: UTF-8 -*-
# ------------------------------------------------------------------------------
# Name:    test_text.py       
# Package: test
# Project: python-utl
# 
# Created: 25.01.2018 11:55   
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

"""Tests for utl.text"""

import unittest
from contextlib import redirect_stdout
from io import StringIO

from utl.text import *


class TestChunk(unittest.TestCase):

    text1 = 'aaabbbcccdddeee'
    text2 = 'aaa'
    input_data1 = (text1, 3)
    expected_result1 = ['aaa', 'bbb', 'ccc', 'ddd', 'eee']
    input_data2 = (text1, 4)
    expected_result2 = ['aaab', 'bbcc', 'cddd', 'eee']
    input_data3 = (text2, 4)
    expected_result3 = ['aaa']

    def test1(self):
        result = list(chunk(*self.input_data1))
        self.assertListEqual(self.expected_result1, result)

    def test2(self):
        result = list(chunk(*self.input_data2))
        self.assertListEqual(self.expected_result2, result)

    def test3(self):
        result = list(chunk(*self.input_data3))
        self.assertListEqual(self.expected_result3, result)


class TestLinesStripped(unittest.TestCase):

    input_data_default = [' aaa ', '\tbbb\n', 'ccc']
    expected_result_default = ['aaa', 'bbb', 'ccc']
    input_data1 = (['xaaax', '  bbb', '__ccc__'], 'x_')
    expected_result1 = ['aaa', '  bbb', 'ccc']
    expected_result2 = ['aaa', 'bbb', 'ccc']

    def test_default(self):
        result = list(lines_stripped(self.input_data_default))
        self.assertListEqual(self.expected_result_default, result)

    def test_customized(self):
        result = list(lines_stripped(*self.input_data1))
        self.assertListEqual(self.expected_result1, result)

    def test_identity(self):
        result = list(lines_stripped(self.expected_result2))
        self.assertListEqual(self.expected_result2, result)


class TestLinesUncommented(unittest.TestCase):

    input_data1 = ['aaa', '; bbb', '#ccc ', 'ddd']
    expected_result1 = ['aaa', 'ddd']
    input_data2 = (['** aaa', '*bbb', '#ccc ', ' ddd'], ('**', ' '))
    expected_result2 = ['*bbb', '#ccc ']

    def test_default_comments(self):
        result = list(lines_uncommented(self.input_data1))
        self.assertListEqual(self.expected_result1, result)

    def test_custom_comments(self):
        result = list(lines_uncommented(*self.input_data2))
        self.assertListEqual(self.expected_result2, result)


def parse_line(line):
    if line.startswith(' '):
        return None
    return True if line else False


class TestLinesParser(unittest.TestCase):

    input_data1 = ('', 'aaa', 'bbb', ' ccc')
    expected_result1 = [
        (ParseStats(read=1, processed=1), False),
        (ParseStats(read=2, processed=2), True),
        (ParseStats(read=3, processed=3), True)
    ]
    input_data2 = ('', 'aaa', ' ccc', 'bbb')
    expected_result2 = [
        (ParseStats(read=1, processed=1), False),
        (ParseStats(read=2, processed=2), True),
        (ParseStats(read=4, processed=3), True)
    ]

    def test1(self):
        result = list(lines_parser(self.input_data1, parse_line))
        self.assertListEqual(self.expected_result1, result)

    def test2(self):
        result = list(lines_parser(self.input_data2, parse_line))
        self.assertListEqual(self.expected_result2, result)


class TestProcessCo(unittest.TestCase):

    input1 = ('file.txt', 3, 7, 1)
    expected1 = '\rfile.txt 3/7 (processed: 1)  Lines saved: 0'
    input2 = 200
    expected2 = '\rfile.txt 3/7 (processed: 1)  Lines saved: 200'
    input3 = ('another_file.txt', 0, 10, 0)
    expected3 = ' Done!\n\ranother_file.txt 0/10 (processed: 0)  Lines saved: 200'

    def setUp(self):
        self.progress = progress_co(0)

    def test(self):
        stdout = StringIO()
        with redirect_stdout(stdout):
            self.progress.send(self.input1)
            self.assertEqual(stdout.getvalue(), self.expected1)

        stdout = StringIO()
        with redirect_stdout(stdout):
            self.progress.send(self.input2)
            self.assertEqual(stdout.getvalue(), self.expected2)

        stdout = StringIO()
        with redirect_stdout(stdout):
            self.progress.send(self.input3)
            self.assertEqual(stdout.getvalue(), self.expected3)
