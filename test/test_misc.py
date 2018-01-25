#!/usr/bin/env python 
# -*- coding: UTF-8 -*-
# ------------------------------------------------------------------------------
# Name:    test_misc.py       
# Package: test
# Project: python-utl
# 
# Created: 25.01.2018 11:26   
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

"""Tests for utl.misc"""

import unittest
import sys

from utl.misc import *


class TestFlatten(unittest.TestCase):

    valid_input = [1, 2, 3, 4, [[[5, 6], 7]], 8, [9]]
    expected_result = [1, 2, 3, 4, 5, 6, 7, 8, 9]

    def test_ok(self):
        result = list(flatten(self.valid_input))
        self.assertListEqual(self.expected_result, result)

    def test_invalid_input(self):
        with self.assertRaises(TypeError):
            list(flatten(1))


if sys.version_info[0] == 2:
    class TestIgnored(unittest.TestCase):

        def test_ok(self):
            try:
                with ignored(TypeError):
                    _ = 'aaa' / 4

            except TypeError:
                self.fail('Unexpected TypeError Exception')

        def test_uncatched_exception(self):
            with self.assertRaises(TypeError):
                with ignored(ValueError):
                    _ = 'aaa' / 4


class TestSingleton(unittest.TestCase):

    class A(object, metaclass=Singleton):
        pass

    def test_ok(self):
        a1 = TestSingleton.A()
        a2 = TestSingleton.A()

        self.assertIs(a1, a2)

