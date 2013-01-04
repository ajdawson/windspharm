""" Test :py:mod:`windspharm.tools` tools for consistency."""
from nose.tools import assert_almost_equal
import numpy as np

from windspharm.tools import (prep_data, recover_data, get_recovery,
        reverse_latdim, order_latdim)

from utils import error


class TestTools(object):
    """Tests for extra tools."""

    def test_prep_recover_data(self):
        """prepared and recovered data matches original?"""
        u = np.random.rand(12, 17, 73, 144)
        up, uinfo = prep_data(u, 'tzyx')
        ur = recover_data(up, uinfo)
        err = error(u, ur)
        assert_almost_equal(err, 0.)

    def test_get_recovery(self):
        """
        get_recovery(info)(pdata) matches recover_data(pdata, info)?

        """
        u = np.random.rand(12, 17, 73, 144)
        up, uinfo = prep_data(u, 'tzyx')
        ur1 = recover_data(up, uinfo)
        recover = get_recovery(uinfo)
        ur2 = recover(up)
        err = error(ur1, ur2)
        assert_almost_equal(err, 0.)

    def test_reverse_latdim(self):
        """reverse_latdim() twice matches original?"""
        u = np.random.rand(12, 17, 73, 144)
        v = np.random.rand(12, 17, 73, 144)
        ur, vr = reverse_latdim(u, v, axis=2)
        urr, vrr = reverse_latdim(ur, vr, axis=2)
        erru = error(u, urr)
        errv = error(v, vrr)
        assert_almost_equal(erru, 0.)
        assert_almost_equal(errv, 0.)

    def test_order_latdim(self):
        """order_latdim() reverses south-to-north latitude dimension?"""
        u = np.random.rand(12, 17, 73, 144)
        v = np.random.rand(12, 17, 73, 144)
        lat = np.arange(-90, 92.5, 2.5)
        latr, ur, vr = order_latdim(lat, u, v, axis=2)
        errl = error(lat[::-1], latr)
        erru = error(u[:,:,::-1], ur)
        errv = error(v[:,:,::-1], vr)
        assert_almost_equal(errl, 0., places=7)
        assert_almost_equal(erru, 0., places=7)
        assert_almost_equal(errv, 0., places=7)

    def test_order_latdim_null(self):
        """
        order_latdim() does not modify north-to-south latitude dimension?

        """
        u = np.random.rand(12, 17, 73, 144)
        v = np.random.rand(12, 17, 73, 144)
        lat = np.arange(90, -92.5, -2.5)
        latr, ur, vr = order_latdim(lat, u, v, axis=2)
        errl = error(lat, latr)
        erru = error(u, ur)
        errv = error(v, vr)
        assert_almost_equal(errl, 0., places=7)
        assert_almost_equal(erru, 0., places=7)
        assert_almost_equal(errv, 0., places=7)


if __name__ == '__main__':
    pass
