"""Tests for the `windspharm` package."""
# Copyright (c) 2012-2016 Andrew Dawson
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

import pytest

import windspharm
from .utils import error


# Create a mapping from interface name to VectorWind class.
solvers = {'standard': windspharm.standard.VectorWind}
try:
    solvers['cdms'] = windspharm.cdms.VectorWind
except AttributeError:
    pass
try:
    solvers['iris'] = windspharm.iris.VectorWind
except AttributeError:
    pass
try:
    solvers['xarray'] = windspharm.xarray.VectorWind
except AttributeError:
    pass


class VectorWindTest(object):
    """Base class for vector wind tests."""

    def assert_error_is_zero(self, f1, f2):
        assert error(f1, f2) == pytest.approx(0., abs=1e-5)
