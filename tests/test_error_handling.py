"""Test error handling.

Includes tests for :py:class:`windspharm.standard.VectorWind`,
:py:class:`windspharm.iris.VectorWind` and
:py:class:`windspharm.cdms.VectorWind`.

"""
from nose import SkipTest
from nose.tools import raises
from unittest import skipIf
import numpy as np
import numpy.ma as ma
try:
    import cdms2
except ImportError:
    pass
try:
    import iris
except ImportError:
    pass

import windspharm

from reference import reference_solutions


class TestErrorsStandard(object):
    """Tests for error handling in the :py:mod:`numpy` interface."""

    @raises(ValueError)
    def test_missing_values(self):
        """missing values raise an error?"""
        ref = reference_solutions('standard')
        u = ref['uwnd']
        v = ref['vwnd']
        mask = np.empty(u.shape, dtype=np.bool)
        mask[:] = False
        mask[1, 1] = True
        u = ma.array(u, mask=mask, fill_value=1.e20)
        v = ma.array(v, mask=mask, fill_value=1.e20)
        vw = windspharm.standard.VectorWind(u, v)

    @raises(ValueError)
    def test_not_a_number(self):
        """not-a-number raises an error?"""
        ref = reference_solutions('standard')
        u = ref['uwnd']
        v = ref['vwnd']
        u[1, 1] = np.nan
        vw = windspharm.standard.VectorWind(u, v)

    @raises(ValueError)
    def test_shape_mismatch(self):
        """different shape u and v raises an error?"""
        ref = reference_solutions('standard')
        u = ref['uwnd'][:-1]
        v = ref['vwnd']
        vw = windspharm.standard.VectorWind(u, v)

    @raises(ValueError)
    def test_rank(self):
        """incorrect rank raises an error?"""
        ref = reference_solutions('standard')
        u = ref['uwnd'][..., np.newaxis, np.newaxis]
        v = ref['vwnd'][..., np.newaxis, np.newaxis]
        vw = windspharm.standard.VectorWind(u, v)

    @raises(ValueError)
    def test_gridtype(self):
        """invalid grid type raises and error?"""
        ref = reference_solutions('standard')
        vw = windspharm.standard.VectorWind(
                ref['uwnd'], ref['vwnd'], gridtype='curvilinear')

    @raises(ValueError)
    def test_shape_invalid(self):
        """invalid shape raises an error?"""
        ref = reference_solutions('standard')
        u = ref['uwnd'][np.newaxis].repeat(2, axis=0)
        v = ref['vwnd'][np.newaxis].repeat(2, axis=0)
        vw = windspharm.standard.VectorWind(u, v)


@skipIf('cdms' not in dir(windspharm) or 'cdms2' not in dir(),
        'library component (cdms2) not available')
class TestErrorsCDMS(object):

    @raises(TypeError)
    def test_non_cdms_variables(self):
        """inputs not cdms variables raises an error?"""
        ref = reference_solutions('standard')
        vw = windspharm.cdms.VectorWind(ref['uwnd'], ref['vwnd'])

    @raises(ValueError)
    def test_dimension_order(self):
        ref = reference_solutions('cdms')
        u = ref['uwnd'].reorder('yx')
        v = ref['vwnd'].reorder('xy')
        vw = windspharm.cdms.VectorWind(u, v)

    @raises(ValueError)
    def test_lat_lon_grid(self):
        """unable to find lat/lon grid raises an error?"""
        ref = reference_solutions('cdms')
        u = ref['uwnd']
        v = ref['vwnd']
        axes = u.getAxisList()
        unknown = cdms2.createAxis(axes[0][:], id='unknown')
        axes[0] = unknown
        u.setAxisList(axes)
        vw = windspharm.cdms.VectorWind(u, v)


@skipIf('iris' not in dir(windspharm) or 'iris' not in dir(),
        'library component (cdms2) not available')
class TestErrorsIris(object):

    @raises(TypeError)
    def test_non_iris_cubes(self):
        ref = reference_solutions('standard')
        vw = windspharm.iris.VectorWind(ref['uwnd'], ref['vwnd'])

    @raises(ValueError)
    def test_dimension_order(self):
        ref = reference_solutions('iris')
        u = ref['uwnd']
        v = ref['vwnd']
        v.transpose([1, 0])
        vw = windspharm.iris.VectorWind(u, v)

    @raises(ValueError)
    def test_lat_lon_grid(self):
        ref = reference_solutions('iris')
        u = ref['uwnd']
        v = ref['vwnd']
        unknown = u.coord('latitude').rename('unknown')
        vw = windspharm.iris.VectorWind(u, v)


if __name__ == '__main__':
    pass
