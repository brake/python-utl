# -*- coding: UTF-8 -*-
#-------------------------------------------------------------------------------
# Name:    wx_.py
# Package: utl
# Project: utl     
#
# Created: 18.09.13 16:37    
# Copyright:  (c) Constantin Roganov, 2013 
# Licence:    The MIT License
#-------------------------------------------------------------------------------
#!/usr/bin/env python

"""wx.Python utilities"""

__author__ = 'Constantin Roganov'

# import wx


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

        if len(args) > 1 and issubclass(args[1].__class__, wx.Event):
            args[1].Skip()

        return fn(*args)

    return skip

