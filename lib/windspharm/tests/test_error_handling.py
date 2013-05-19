"""Tests for error handling in `windspharm`."""
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

from nose import SkipTest
from nose.tools import raises
import numpy as np
import numpy.ma as ma

import windspharm
from windspharm.tests import VectorWindTest, solvers
from .reference import reference_solutions


class ErrorHandlersTest(VectorWindTest):
    """Base class for all error handler tests."""
    interface = None
    gridtype = None

    @classmethod
    def setup_class(cls):
        skip_message = 'library component not available for {!s} interface'
        if cls.interface not in solvers:
            raise SkipTest(skip_message.format(cls.interface))


#-----------------------------------------------------------------------------
# Tests for the standard interface


class TestStandardErrorHandlers(ErrorHandlersTest):
    """Standard interface error handler tests."""
    interface = 'standard'
    gridtype = 'regular'

    @raises(ValueError)
    def test_masked_values(self):
        # masked values in inputs should raise an error
        solution = reference_solutions(self.interface, self.gridtype)
        mask = np.empty(solution['uwnd'].shape, dtype=np.bool)
        mask[:] = False
        mask[1, 1] = True
        u = ma.array(solution['uwnd'], mask=mask, fill_value=1.e20)
        v = ma.array(solution['vwnd'], mask=mask, fill_value=1.e20)
        vw = solvers[self.interface](u, v, gridtype=self.gridtype)

    @raises(ValueError)
    def test_nan_values(self):
        # NaN values in inputs should raise an error
        solution = reference_solutions(self.interface, self.gridtype)
        solution['vwnd'][1, 1] = np.nan
        vw = solvers[self.interface](solution['uwnd'], solution['vwnd'],
                                     gridtype=self.gridtype)

    @raises(ValueError)
    def test_invalid_shape_components(self):
        # invalid shape inputs should raise an error
        solution = reference_solutions(self.interface, self.gridtype)
        vw = solvers[self.interface](
            solution['uwnd'][np.newaxis].repeat(2, axis=0),
            solution['vwnd'][np.newaxis].repeat(2, axis=0),
            gridtype=self.gridtype)

    @raises(ValueError)
    def test_different_shape_components(self):
        # different shape inputs should raise an error
        solution = reference_solutions(self.interface, self.gridtype)
        vw = solvers[self.interface](solution['uwnd'], solution['vwnd'][:-1],
                                     gridtype=self.gridtype)

    @raises(ValueError)
    def test_invalid_rank_components(self):
        # invalid rank inputs should raise an error
        solution = reference_solutions(self.interface, self.gridtype)
        vw = solvers[self.interface](
            solution['uwnd'][..., np.newaxis, np.newaxis],
            solution['vwnd'][..., np.newaxis, np.newaxis],
            gridtype=self.gridtype)

    @raises(ValueError)
    def test_different_rank_components(self):
        # different rank inputs should raise an error
        solution = reference_solutions(self.interface, self.gridtype)
        vw = solvers[self.interface](solution['uwnd'][..., np.newaxis],
                                     solution['vwnd'],
                                     gridtype=self.gridtype)

    @raises(ValueError)
    def test_invalid_gridtype(self):
        # invalid grid type specification should raise an error
        solution = reference_solutions(self.interface, self.gridtype)
        vw = solvers[self.interface](solution['uwnd'], solution['vwnd'],
                                     gridtype='curvilinear')

    @raises(ValueError)
    def test_gradient_masked_values(self):
        # masked values in gradient input should raise an error
        solution = reference_solutions(self.interface, self.gridtype)
        vw = solvers[self.interface](solution['uwnd'], solution['vwnd'],
                                     gridtype=self.gridtype)
        mask = np.empty(solution['uwnd'].shape, dtype=np.bool)
        mask[:] = False
        mask[1, 1] = True
        chi = ma.array(solution['chi'], mask=mask, fill_value=1.e20)
        uchi, vchi = vw.gradient(chi)

    @raises(ValueError)
    def test_gradient_nan_values(self):
        # NaN values in gradient input should raise an error
        solution = reference_solutions(self.interface, self.gridtype)
        vw = solvers[self.interface](solution['uwnd'], solution['vwnd'],
                                     gridtype=self.gridtype)
        solution['chi'][1, 1] = np.nan
        uchi, vchi = vw.gradient(solution['chi'])

    @raises(ValueError)
    def test_gradient_invalid_shape(self):
        # input to gradient of different shape should raise an error
        solution = reference_solutions(self.interface, self.gridtype)
        vw = solvers[self.interface](solution['uwnd'], solution['vwnd'],
                                     gridtype=self.gridtype)
        uchi, vchi = vw.gradient(solution['chi'][:-1])


#-----------------------------------------------------------------------------
# Tests for the cdms interface


class TestCDMSErrorHandlers(ErrorHandlersTest):
    """cdms interface error handler tests."""
    interface = 'cdms'
    gridtype = 'regular'

    @raises(TypeError)
    def test_non_variable_input(self):
        # input not a cdms2 variable should raise an error
        solution = reference_solutions('standard', self.gridtype)
        vw = solvers[self.interface](solution['uwnd'], solution['vwnd'])

    @raises(ValueError)
    def test_different_shape_components(self):
        # inputs not the same shape should raise an error
        solution = reference_solutions(self.interface, self.gridtype)
        vw = solvers[self.interface](solution['uwnd'],
                                     solution['vwnd'].reorder('xy'))

    @raises(ValueError)
    def test_unknown_grid(self):
        # inputs where a lat-lon grid cannot be identified should raise an
        # error
        solution = reference_solutions(self.interface, self.gridtype)
        lat = solution['vwnd'].getLatitude()
        delattr(lat, 'axis')
        lat.id = 'unknown'
        vw = solvers[self.interface](solution['uwnd'], solution['vwnd'])

    @raises(TypeError)
    def test_non_variable_gradient_input(self):
        # input to gradient not a cdms2 variable should raise an error
        solution = reference_solutions(self.interface, self.gridtype)
        vw = solvers[self.interface](solution['uwnd'], solution['vwnd'])
        dummy_solution = reference_solutions('standard', self.gridtype)
        uchi, vchi = vw.gradient(dummy_solution['chi'])

    @raises(TypeError)
    def test_gradient_non_variable_input(self):
        # input to gradient not a cdms2 variable should raise an error
        solution = reference_solutions(self.interface, self.gridtype)
        vw = solvers[self.interface](solution['uwnd'], solution['vwnd'])
        dummy_solution = reference_solutions('standard', self.gridtype)
        uchi, vchi = vw.gradient(dummy_solution['chi'])

    @raises(ValueError)
    def test_gradient_different_shape(self):
        # input to gradient of different shape should raise an error
        solution = reference_solutions(self.interface, self.gridtype)
        vw = solvers[self.interface](solution['uwnd'], solution['vwnd'])
        uchi, vchi = vw.gradient(solution['chi'][:-1])

    @raises(ValueError)
    def test_gradient_unknown_grid(self):
        # input to gradient with no identifiable grid should raise an error
        solution = reference_solutions(self.interface, self.gridtype)
        vw = solvers[self.interface](solution['uwnd'], solution['vwnd'])
        lat = solution['chi'].getLatitude()
        delattr(lat, 'axis')
        lat.id = 'unknown'
        uchi, vchi = vw.gradient(solution['chi'])


#-----------------------------------------------------------------------------
# Tests for the iris interface


class TestIrisErrorHandlers(ErrorHandlersTest):
    """Iris interface error handler tests."""
    interface = 'iris'
    gridtype = 'regular'

    @raises(TypeError)
    def test_non_cube_input(self):
        # input not an iris cube should raise an error
        solution = reference_solutions('standard', self.gridtype)
        vw = solvers[self.interface](solution['uwnd'], solution['vwnd'])

    @raises(ValueError)
    def test_different_shape_components(self):
        # inputs not the same shape should raise an error
        solution = reference_solutions(self.interface, self.gridtype)
        solution['vwnd'].transpose([1, 0])
        vw = solvers[self.interface](solution['uwnd'], solution['vwnd'])

    @raises(ValueError)
    def test_unknown_grid(self):
        # inputs where a lat-lon grid cannot be identified should raise an
        # error
        solution = reference_solutions(self.interface, self.gridtype)
        solution['vwnd'].coord('latitude').rename('unknown')
        vw = solvers[self.interface](solution['uwnd'], solution['vwnd'])

    @raises(TypeError)
    def test_gradient_non_cube_input(self):
        # input to gradient not an iris cube should raise an error
        solution = reference_solutions(self.interface, self.gridtype)
        vw = solvers[self.interface](solution['uwnd'], solution['vwnd'])
        dummy_solution = reference_solutions('standard', self.gridtype)
        uchi, vchi = vw.gradient(dummy_solution['chi'])

    @raises(ValueError)
    def test_gradient_different_shape(self):
        # input to gradient of different shape should raise an error
        solution = reference_solutions(self.interface, self.gridtype)
        vw = solvers[self.interface](solution['uwnd'], solution['vwnd'])
        uchi, vchi = vw.gradient(solution['chi'][:-1])

    @raises(ValueError)
    def test_gradient_unknown_grid(self):
        # input to gradient with no identifiable grid should raise an error
        solution = reference_solutions(self.interface, self.gridtype)
        vw = solvers[self.interface](solution['uwnd'], solution['vwnd'])
        solution['chi'].coord('latitude').rename('unknown')
        uchi, vchi = vw.gradient(solution['chi'])
