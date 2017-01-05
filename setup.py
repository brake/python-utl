#!/usr/bin/env python 
# -*- coding: UTF-8 -*-
# ------------------------------------------------------------------------------
# Name:    setup.py       
# Package: 
# Project: utl
# 
# Created: 18.12.16 21:04   
# Copyright 2016 © Constantin Roganov
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

from __future__ import unicode_literals, absolute_import
from setuptools import setup, find_packages
import sys

__author__ = 'Constantin Roganov'
__version__ = '0.1.0'

install_requires = ['future >= 0.16.0'] if sys.version_info[0] == 2 else []


setup(
    name='utl',
    version=__version__,
    packages=find_packages(),
    zip_safe=True,
    install_requires=install_requires,
    author=__author__,
    author_email='rccbox at gmail dot com',
    description='My Python utilities for every day',
    long_description=open('README.md').read(),
    license=open('LICENSE.txt').read(),
    url='https://github.com/brake/python-utl',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
    ],
)
