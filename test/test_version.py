#!/usr/bin/env python 
# -*- coding: UTF-8 -*-
# ------------------------------------------------------------------------------
# Name:    test_version.py       
# Package: test
# Project: python-utl
# 
# Created: 25.01.2018 14:31   
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

"""Tests for utl.version"""

import unittest
from os import remove

from utl.version import *
from utl.version import _MAIN_VERSION_FILE, _FULL_VERSION_FILE


class TestVersion(unittest.TestCase):

    current_version = '1.0.0'
    new_version = '1.0.1'

    def setUp(self):
        get_current_version()

    def tearDown(self):
        for name in (_MAIN_VERSION_FILE, _FULL_VERSION_FILE):
            remove(name)

    def test_get_new_version(self):
        version = get_new_version()
        self.assertEqual(self.new_version, version)

    def test_get_current_version(self):
        version = get_current_version()
        self.assertEqual(self.current_version, version)
