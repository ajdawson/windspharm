"""
Test cases for the tools for data preparation in
:py:mod:`windspharm.tools`.

"""
from unittest import TestCase

import numpy as np

import windspharm.tools
from testutils import error, identify


class ToolsTestCase(TestCase):

    def __str__(self):
        return 'checking consistency of data preparation tools'

    def test_reverse_latdim(self):
        identify('reverse latitude dimension')
        u = np.random.rand(12, 17, 73, 144)
        v = np.random.rand(12, 17, 73, 144)
        ur, vr = windspharm.tools.reverse_latdim(u, v, axis=2)
        urr, vrr = windspharm.tools.reverse_latdim(ur, vr, axis=2)
        erru = error(u, urr)
        errv = error(v, vrr)
        self.assertAlmostEqual(erru, 0., places=7)
        self.assertAlmostEqual(errv, 0., places=7)

    def test_order_latdim_null(self):
        identify('order latitude dimension (null)')
        u = np.random.rand(12, 17, 73, 144)
        v = np.random.rand(12, 17, 73, 144)
        lat = np.arange(90, -92.5, -2.5)
        latr, ur, vr = windspharm.tools.order_latdim(lat, u, v, axis=2)
        errl = error(lat, latr)
        erru = error(u, ur)
        errv = error(v, vr)
        self.assertAlmostEqual(errl, 0., places=7)
        self.assertAlmostEqual(erru, 0., places=7)
        self.assertAlmostEqual(errv, 0., places=7)
    
    def test_order_latdim(self):
        identify('order latitude dimension')
        u = np.random.rand(12, 17, 73, 144)
        v = np.random.rand(12, 17, 73, 144)
        lat = np.arange(-90, 92.5, 2.5)
        latr, ur, vr = windspharm.tools.order_latdim(lat, u, v, axis=2)
        errl = error(lat[::-1], latr)
        erru = error(u[:,:,::-1], ur)
        errv = error(v[:,:,::-1], vr)
        self.assertAlmostEqual(errl, 0., places=7)
        self.assertAlmostEqual(erru, 0., places=7)
        self.assertAlmostEqual(errv, 0., places=7)

    def test_prep_recover_data(self):
        identify('preparing and recovering data shape')
        u = np.random.rand(12, 17, 73, 144)
        up, uinfo = windspharm.tools.prep_data(u, 'tzyx')
        ur = windspharm.tools.recover_data(up, uinfo)
        err = error(u, ur)
        self.assertAlmostEqual(err, 0., places=7)


if __name__ == '__main__':
    pass

