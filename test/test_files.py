#!/usr/bin/env python 
# -*- coding: UTF-8 -*-
# ------------------------------------------------------------------------------
# Name:    test_files.py       
# Package: test
# Project: python-utl
# 
# Created: 24.01.2018 17:34   
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

"""Unittests for utl.files"""

import unittest
from os import remove

from utl.files import *
from utl.files import _reverse_blocks_generator


class TestLinesCount(unittest.TestCase):

    test_file_name = 'LinesCountTest.txt'

    def create_test_file(self, num):
        with writable_text_file(self.test_file_name) as fd:
            for i in range(num):
                if i:
                    fd.write('\n')
                fd.write('LinesCountTest {:03d}'.format(i))

    def tearDown(self):
        remove(self.test_file_name)

    def test_simple(self):
        lines_expected = 101
        self.create_test_file(lines_expected)
        result = file_lines_count(self.test_file_name)

        self.assertEqual(lines_expected, result)

    def test_zero_length(self):
        lines_expected = 0
        self.create_test_file(lines_expected)
        result = file_lines_count(self.test_file_name)

        self.assertEqual(lines_expected, result)

    def test_single_line(self):
        lines_expected = 1
        self.create_test_file(lines_expected)
        result = file_lines_count(self.test_file_name)

        self.assertEqual(lines_expected, result)


class TestReverseBlocksGenerator(unittest.TestCase):

    test_file_name = 'ReverseBlocksTest.txt'
    test_content = '111122223333444'
    test_block_size = 4
    expected_result = [b'444', b'3333', b'2222', b'1111']

    def create_test_file(self):
        with writable_text_file(self.test_file_name, encoding='ascii') as fd:
            fd.write(self.test_content)

    def tearDown(self):
        remove(self.test_file_name)

    def test_ok(self):
        self.create_test_file()
        with binary_file(self.test_file_name) as fd:
            result = list(_reverse_blocks_generator(fd, self.test_block_size))

        self.assertListEqual(self.expected_result, result)

    def test_invalid_file_mode(self):
        self.create_test_file()

        with self.assertRaises(TypeError):
            with text_file(self.test_file_name) as fd:
                list(_reverse_blocks_generator(fd))


class TestReverseLines(unittest.TestCase):

    test_file_name = 'ReverseBlocksTest.txt'
    test_content = '1111\n2222\n3333\n444'
    test_block_size = 3
    expected_result = [u'444', u'3333', u'2222', u'1111']
    expected_result_newlines = [u'444', u'3333\n', u'2222\n', u'1111\n']

    def create_test_file(self):
        with writable_text_file(self.test_file_name, encoding='ascii') as fd:
            fd.write(self.test_content)

    def tearDown(self):
        remove(self.test_file_name)

    def test_ok(self):
        self.create_test_file()

        with binary_file(self.test_file_name) as fd:
            result = list(reverse_lines(fd))

        self.assertListEqual(self.expected_result, result)

    def test_with_newlines_ok(self):
        self.create_test_file()

        with binary_file(self.test_file_name) as fd:
            result = list(reverse_lines(fd, True, self.test_block_size))

        self.assertListEqual(self.expected_result_newlines, result)

    def test_invalid_file_mode(self):
        self.create_test_file()

        with self.assertRaises(TypeError):
            with text_file(self.test_file_name) as fd:
                list(reverse_lines(fd))

def _fill_files(name_template):
    return [name_template.format(i) for i in range(2)]

class TestFileListProcessor(unittest.TestCase):

    name_template = 'filelist_proc_test{}.txt'

    files = _fill_files(name_template)
    expected_result = [
        'filelist_proc_test0.txt 0',
        'filelist_proc_test0.txt 1',
        'filelist_proc_test1.txt 0',
        'filelist_proc_test1.txt 1',
    ]

    @staticmethod
    def create_file(name):
        with writable_text_file(name) as fd:
            for i in range(2):
                fd.write('{} {}\n'.format(name, i))

    def create_files(self):
        for n in self.files:
            TestFileListProcessor.create_file(n)

    def tearDown(self):
        for name in self.files:
            remove(name)

    def test_ok(self):
        self.create_files()

        result = list(filelist_processor(self.files, lambda x: x))

        self.assertListEqual(self.expected_result, result)


class TestOffsetIter(unittest.TestCase):

    test_file_name = 'OffserIterTest.txt'
    test_input = '1111\n2222\n3333\n444'

    def create_test_file(self):
        with writable_text_file(self.test_file_name, encoding='ascii') as fd:
            fd.write(self.test_input)

    def tearDown(self):
        remove(self.test_file_name)

    def test_ok(self):
        self.create_test_file()

        with binary_file(self.test_file_name) as fd:
            offset, result = list(offset_iter(fd))[-1]

        with binary_file(self.test_file_name) as fd:
            fd.seek(offset, os.SEEK_SET)
            self.assertEqual(result, fd.readline())
