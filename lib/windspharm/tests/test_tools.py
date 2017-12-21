"""Tests for the `windspharm.tools` module."""
# Copyright (c) 2012-2013 Andrew Dawson
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

import numpy as np
from numpy.testing import assert_array_equal

from windspharm.tools import (prep_data, recover_data, get_recovery,
                              reverse_latdim, order_latdim)
from windspharm.tests import VectorWindTest


class TestTools(VectorWindTest):
    """Tests for extra tools."""

    def test_prep_recover_data(self):
        # applying preparation and recovery should yield an identical data set
        u = np.random.rand(12, 17, 73, 144)
        up, uinfo = prep_data(u, 'tzyx')
        ur = recover_data(up, uinfo)
        assert_array_equal(u, ur)

    def test_get_recovery(self):
        # recovery helper should produce the same result as the manual method
        u = np.random.rand(12, 17, 73, 144)
        up, uinfo = prep_data(u, 'tzyx')
        ur1 = recover_data(up, uinfo)
        recover = get_recovery(uinfo)
        ur2, = recover(up)
        assert_array_equal(ur1, ur2)

    def test_reverse_latdim(self):
        # applying reversal to the latitude dimension twice should return it to
        # its original
        u = np.random.rand(12, 17, 73, 144)
        v = np.random.rand(12, 17, 73, 144)
        ur, vr = reverse_latdim(u, v, axis=2)
        urr, vrr = reverse_latdim(ur, vr, axis=2)
        assert_array_equal(u, urr)
        assert_array_equal(v, vrr)

    def test_order_latdim(self):
        # order_latdim should reverse a south-north latitude dimension
        u = np.random.rand(12, 17, 73, 144)
        v = np.random.rand(12, 17, 73, 144)
        lat = np.arange(-90, 92.5, 2.5)
        latr, ur, vr = order_latdim(lat, u, v, axis=2)
        assert_array_equal(lat[::-1], latr)
        assert_array_equal(u[:, :, ::-1], ur)
        assert_array_equal(v[:, :, ::-1], vr)

    def test_order_latdim_null(self):
        # order_latdim should not reverse a north-south latitude dimension
        u = np.random.rand(12, 17, 73, 144)
        v = np.random.rand(12, 17, 73, 144)
        lat = np.arange(90, -92.5, -2.5)
        latr, ur, vr = order_latdim(lat, u, v, axis=2)
        assert_array_equal(lat, latr)
        assert_array_equal(u, ur)
        assert_array_equal(v, vr)
