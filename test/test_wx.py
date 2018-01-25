#!/usr/bin/env python 
# -*- coding: UTF-8 -*-
# ------------------------------------------------------------------------------
# Name:    test_wx.py       
# Package: test
# Project: python-utl
# 
# Created: 25.01.2018 15:12   
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

"""Tests for utl.wx_"""

import unittest

from utl.wx_ import *


@modal_dialog
class DummyDialog(object):

    destroyed = False

    def Destroy(self):
        self.destroyed = True


class TestModalDialog(unittest.TestCase):

    def test(self):

        with DummyDialog() as dialog:
            pass

        self.assertTrue(dialog.destroyed)


class SkipableEvent(object):

    skipped = False

    def Skip(self):
        self.skipped = True


class TestTransparentHandler(unittest.TestCase):

    @transparent_event_handler
    def handler(self, event):
        pass

    def test(self):
        event = SkipableEvent()
        self.handler(event)

        self.assertTrue(event.skipped)
