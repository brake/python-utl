#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# ------------------------------------------------------------------------------
# Name:    version.py
# Package: utl
# Project: utl
#
# Created: 24.03.14 17:50
# Copyright 2014-2016 © Constantin Roganov
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


"""Application version management.

Based on files:
    - main_version.txt
    - previous version of file app_version.py

create a new file app_version.py containing current application version.
Only a "build" code, which is responsible for version increment requires to import this module. Code reading
the application version depends only from automatically updated app_version.py

Version is a string consisting from three parts: major.minor.build
    - major (0...255)
    - minor (0...255)
    - build (0...65535)

In case you need increment major and/or minor version numbers and reset a build number to zero, you have to:
    - edit the 'main_version.txt' to set major and minor versions
    - remove 'app_version.py'

Usage:
    Inside each "build" code you have to call get_new_version()
    In a code where there the version number is need
        import app_version
        ...
        version = app_version.version

"""

from __future__ import unicode_literals
from builtins import *

import itertools
import sys

from .files import text_file, writable_text_file
from .text import lines_stripped, lines_uncommented

if sys.version_info[0] == 2:
    from .misc import ignored as suppress
else:
    from contextlib import suppress

__author__ = 'Constantin Roganov'

_MAIN_VERSION_FILE = 'main_version.txt'
_FULL_VERSION_FILE = 'app_version.py'
_DEFAULT_MAIN_VERSION = '1.0'  # minor and major versions
_MAX_BUILD = 65535
_MAX_MAJOR = 255
_MAX_MINOR = _MAX_MAJOR
_VARIABLE_SEP = '='
_VERSION_SEP = '.'
_SINGLE_QUOTE = " '"


def _read_single_line_from_file(name):
    with text_file(name) as fo:
        for line in itertools.dropwhile(lambda s: not s, lines_uncommented(lines_stripped(fo))):
            return line


def _validate_main_version(txt):
    """Check validity of major and minor version components"""

    version_parts = map(int, txt.split(_VERSION_SEP))

    version_params = (
        ('major', _MAX_MAJOR),
        ('minor', _MAX_MINOR),
    )
    message = 'Version: {} version value exceed the maximum {}'

    for i, ver in enumerate(version_parts):
        if ver > version_params[i][1]:
            raise ValueError(message.format(*version_params[i]))


def _get_main_version():
    """Read major/minor versions from file.
    If file does not exist creates with default start values.
    """

    version = _DEFAULT_MAIN_VERSION

    try:
        version = _read_single_line_from_file(_MAIN_VERSION_FILE)

    except IOError:
        with writable_text_file(_MAIN_VERSION_FILE) as fo:
            fo.write(version)

    _validate_main_version(version)
    return version


def _get_new_build_number():
    """Return a text representation of new build number (incremented by 1 current value)"""

    build = 0

    get_build_num = lambda v: v.split(_VARIABLE_SEP)[1].strip("'").split(_VERSION_SEP)[2]

    with suppress(IOError):
        version = _read_single_line_from_file(_FULL_VERSION_FILE)
        if version and _VARIABLE_SEP in version:
            build = int(get_build_num(version))
            if build > _MAX_BUILD:
                raise ValueError('Version: Maximum or build number reached')
            else:
                build += 1

    return str(build)


def get_new_version():
    """Return a new full version number"""

    version = _VERSION_SEP.join((_get_main_version(), _get_new_build_number()))

    with writable_text_file(_FULL_VERSION_FILE) as fo:
        fo.write("# last autogenerated application version\n\nversion = '{}'\n".format(version))

    return version


def get_current_version():
    """Return a full current version number.
    If version information have not initialized yet it will be generated.
    """

    try:
        version = _read_single_line_from_file(_FULL_VERSION_FILE)
        if version:
            if _VARIABLE_SEP in version:
                return version.split(_VARIABLE_SEP)[1].strip(_SINGLE_QUOTE)
            else:
                return version.strip(_SINGLE_QUOTE)

    except IOError:
        return get_new_version()


