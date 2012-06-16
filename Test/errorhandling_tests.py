"""
Test cases for error handling in the
:py:class:`windspharm.standard.VectorWind` and
:py:class:`windspharm.metadata.VectorWind` interfaces.

"""
import unittest
from unittest import TestCase

import numpy as np
import numpy.ma as ma
try:
    import cdms2
except ImportError:
    pass

import windspharm
from testutils import generate_test_data, identify


class VectorWindInvalidTestCase(TestCase):
    """
    Error catching in the meta-data enabled :py:mod:`cdms2` interface.

    """

    def __str__(self):
        return 'verifying error handling (standard interface)'

    def setUp(self):
        pass

    def test_missingvalues(self):
        identify('missing values')
        ref = generate_test_data('standard')
        u = ref['uwnd']
        v = ref['vwnd']
        mask = np.empty(u.shape, dtype=np.bool)
        mask[:] = False
        mask[1, 1] = True
        u = ma.array(u, mask=mask, fill_value=1.e20)
        v = ma.array(v, mask=mask, fill_value=1.e20)
        self.assertRaises(ValueError, windspharm.standard.VectorWind, u, v)

    def test_nan(self):
        identify('not-a-number')
        ref = generate_test_data('standard')
        u = ref['uwnd']
        v = ref['vwnd']
        u[1, 1] = np.nan
        self.assertRaises(ValueError, windspharm.standard.VectorWind, u, v)

    def test_shape(self):
        identify('shape')
        ref = generate_test_data('standard')
        u = ref['uwnd'][:-1]
        v = ref['vwnd']
        self.assertRaises(ValueError, windspharm.standard.VectorWind, u, v)

    def test_rank(self):
        identify('rank')
        ref = generate_test_data('standard')
        u = ref['uwnd'][..., np.newaxis, np.newaxis]
        v = ref['vwnd'][..., np.newaxis, np.newaxis]
        self.assertRaises(ValueError, windspharm.standard.VectorWind, u, v)

    def test_gridtype(self):
        identify('grid type')
        ref = generate_test_data('standard')
        u = ref['uwnd']
        v = ref['vwnd']
        self.assertRaises(ValueError, windspharm.standard.VectorWind, u, v,
                gridtype='curvilinear')


@unittest.skipIf('metadata' not in dir(windspharm) or 'cdms2' not in dir(),
        'library component not available')
class VectorWindMetaDataInvalidTestCase(TestCase):
    """
    Error catching in the meta-data enabled :py:mod:`cdms2` interface.

    """

    def __str__(self):
        return 'verifying error handling (meta-data interface)'

    def setUp(self):
        pass

    def test_cdmsvariables(self):
        identify('variable type')
        ref = generate_test_data('standard')
        u = ref['uwnd']
        v = ref['vwnd']
        self.assertRaises(ValueError, windspharm.metadata.VectorWind, u, v)

    def test_order(self):
        identify('dimension order')
        ref = generate_test_data('metadata')
        u = ref['uwnd']
        v = ref['vwnd']
        v = v.reorder('xy')
        self.assertRaises(ValueError, windspharm.metadata.VectorWind, u, v)

    def test_latlongrid(self):
        identify('latitude-longitude grid')
        ref = generate_test_data('metadata')
        u = ref['uwnd']
        v = ref['vwnd']
        axes = u.getAxisList()
        latitude = cdms2.createAxis(axes[0][:], id='mylat')
        axes[0] = latitude
        u.setAxisList(axes)
        self.assertRaises(ValueError, windspharm.metadata.VectorWind, u, v)


if __name__ == '__main__':
    pass

