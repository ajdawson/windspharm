"""Tests coding standards compliance."""
# Copyright (c) 2016 Andrew Dawson
#
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
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
from __future__ import absolute_import

import os

from nose.tools import assert_equal
import pep8

import windspharm
from windspharm.tests import VectorWindTest


class TestCodingStandards(VectorWindTest):

    def test_pep8(self):
        pep8style = pep8.StyleGuide(quiet=False)
        base_paths = [os.path.dirname(windspharm.__file__)]
        result = pep8style.check_files(base_paths)
        assert_equal(result.total_errors, 0, "Found PEP8 style issues.")
