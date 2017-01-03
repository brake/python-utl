#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# ------------------------------------------------------------------------------
# Name:    wx_.py
# Package: utl
# Project: utl
#
# Created: 18.09.13 16:37
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


"""wx.Python utilities"""


from __future__ import unicode_literals

__author__ = 'Constantin Roganov'


_DESTROY_METHOD_NAME = 'Destroy'
_SKIP_METHOD_NAME = 'Skip'


def modal_dialog(cls):
    """Decorator adding to classes derived from wx.Dialog feature of modal call via context manager protocol.

    Example:
        @utl.wx_.modal_dialog
        class MyDialog extends wx.Dialog:
            pass
        ...

        with MyDialog() as dlg:
            dlg.ShowModal()
    """

    # assert issubclass(cls, wx.Dialog)

    def enter(inst):
        if not hasattr(inst, _DESTROY_METHOD_NAME):
            raise TypeError('Class {} does not provide required method {}()'.format(
                inst.__class__.__name__,
                _DESTROY_METHOD_NAME
            ))
        return inst

    def exit_(inst, *args):
        inst.Destroy()

    cls.__enter__ = enter
    cls.__exit__ = exit_

    return cls


def transparent_event_handler(fn):
    """Decorator for event handlers which should call event.Skip().
    Prevents event handler from explict annoying call of event.Skip().

    Assumes that handler receives event as second parameter.
    """

    def skip(*args):

        if len(args) and hasattr(args[1], _SKIP_METHOD_NAME):
            args[1].Skip()

        return fn(*args)

    return skip

