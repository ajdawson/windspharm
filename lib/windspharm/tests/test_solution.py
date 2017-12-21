"""Test windspharm computations against reference solutions."""
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

import numpy as np
import pytest

from windspharm.tests import VectorWindTest, solvers
from .reference import reference_solutions


class SolutionTest(VectorWindTest):
    """Base class for all solution test classes."""
    interface = None
    gridtype = None
    radius = None

    @classmethod
    def setup_class(cls):
        msg = 'missing dependencies required to test the {!s} interface'
        try:
            cls.solution = reference_solutions(cls.interface, cls.gridtype)
        except ValueError:
            pytest.skip(msg.format(cls.interface))
        cls.pre_modify_solution()
        try:
            # gridtype argument only available for the standard interface
            kwargs = {}
            if cls.interface == 'standard':
                kwargs['gridtype'] = cls.gridtype
            if cls.radius is not None:
                kwargs['rsphere'] = cls.radius
            cls.vw = solvers[cls.interface](cls.solution['uwnd'],
                                            cls.solution['vwnd'], **kwargs)
        except KeyError:
            pytest.skip(msg.format(cls.interface))
        cls.post_modify_solution()

    @classmethod
    def pre_modify_solution(cls):
        pass

    @classmethod
    def post_modify_solution(cls):
        pass

    def test_magnitude(self):
        # computed magnitude matches magnitude of reference solution?
        mag1 = self.vw.magnitude()
        mag2 = (self.solution['uwnd'] ** 2 + self.solution['vwnd'] ** 2) ** 0.5
        self.assert_error_is_zero(mag1, mag2)

    def test_vorticity(self):
        # computed vorticity matches reference solution?
        vrt1 = self.vw.vorticity()
        vrt2 = self.solution['vrt']
        self.assert_error_is_zero(vrt1, vrt2)

    def test_divergence(self):
        # computed divergence matches reference solution?
        div1 = self.vw.divergence()
        div2 = self.solution['div']
        self.assert_error_is_zero(div1, div2)

    def test_streamfunction(self):
        # computed streamfunction matches reference solution?
        sf1 = self.vw.streamfunction()
        sf2 = self.solution['psi'].copy()
        self.assert_error_is_zero(sf1, sf2)

    def test_velocitypotential(self):
        # computed velocity potential matches reference solution?
        vp1 = self.vw.velocitypotential()
        vp2 = self.solution['chi'].copy()
        self.assert_error_is_zero(vp1, vp2)

    def test_nondivergent(self):
        # computed non-divergent vector wind matches reference solution?
        upsi1, vpsi1 = self.vw.nondivergentcomponent()
        upsi2, vpsi2 = self.solution['upsi'], self.solution['vpsi']
        self.assert_error_is_zero(upsi1, upsi2)
        self.assert_error_is_zero(vpsi1, vpsi2)

    def test_irrotational(self):
        # computed irrotational vector wind matches reference solution?
        uchi1, vchi1 = self.vw.irrotationalcomponent()
        uchi2, vchi2 = self.solution['uchi'], self.solution['vchi']
        self.assert_error_is_zero(uchi1, uchi2)
        self.assert_error_is_zero(vchi1, vchi2)

    def test_gradient(self):
        # computed gradient matches reference solution?
        uchi1, vchi1 = self.vw.gradient(self.solution['chi'])
        uchi2, vchi2 = self.solution['chigradu'], self.solution['chigradv']
        self.assert_error_is_zero(uchi1, uchi2)
        self.assert_error_is_zero(vchi1, vchi2)

    def test_vrtdiv(self):
        # vrtdiv() matches vorticity()/divergence()?
        vrt1, div1 = self.vw.vrtdiv()
        vrt2 = self.vw.vorticity()
        div2 = self.vw.divergence()
        self.assert_error_is_zero(vrt1, vrt2)
        self.assert_error_is_zero(div1, div2)

    def test_sfvp(self):
        # sfvp() matches streamfunction()/velocitypotential()?
        sf1, vp1 = self.vw.sfvp()
        sf2 = self.vw.streamfunction()
        vp2 = self.vw.velocitypotential()
        self.assert_error_is_zero(sf1, sf2)
        self.assert_error_is_zero(vp1, vp2)

    def test_helmholtz(self):
        # helmholtz() matches irrotationalcomponent()/nondivergentcomponent()?
        uchi1, vchi1, upsi1, vpsi1 = self.vw.helmholtz()
        uchi2, vchi2 = self.vw.irrotationalcomponent()
        upsi2, vpsi2 = self.vw.nondivergentcomponent()
        uchi, vchi, upsi2, vpsi2 = self.vw.helmholtz()
        self.assert_error_is_zero(uchi1, uchi2)
        self.assert_error_is_zero(vchi1, vchi2)
        self.assert_error_is_zero(upsi1, upsi2)
        self.assert_error_is_zero(vpsi1, vpsi2)

    def test_truncate(self):
        # vorticity truncated to T21 matches reference?
        vrt_trunc = self.vw.truncate(self.solution['vrt'], truncation=21)
        self.assert_error_is_zero(vrt_trunc, self.solution['vrt_trunc'])


# ----------------------------------------------------------------------------
# Tests for the standard interface


class StandardSolutionTest(SolutionTest):
    """Base class for all standard interface solution test classes."""
    interface = 'standard'


class TestStandardRegular(StandardSolutionTest):
    """Regular grid."""
    gridtype = 'regular'


class TestStandardGaussian(StandardSolutionTest):
    """Gaussian grid."""
    gridtype = 'gaussian'


class TestStandardRegularSingleton(StandardSolutionTest):
    """Singleton right-most dimension."""
    gridtype = 'regular'

    @classmethod
    def pre_modify_solution(cls):
        for field_name in cls.solution:
            cls.solution[field_name] = \
                cls.solution[field_name][..., np.newaxis]


class TestStandardGaussianSingleton(StandardSolutionTest):
    """Singleton right-most dimension."""
    gridtype = 'gaussian'

    @classmethod
    def pre_modify_solution(cls):
        for field_name in cls.solution:
            cls.solution[field_name] = \
                cls.solution[field_name][..., np.newaxis]


class TestStandardMultiTime(StandardSolutionTest):
    gridtype = 'regular'

    @classmethod
    def pre_modify_solution(cls):
        for field_name in cls.solution:
            cls.solution[field_name] = \
                cls.solution[field_name][..., np.newaxis].repeat(5, axis=-1)


class TestStandardRadiusDefaultExplicit(StandardSolutionTest):
    gridtype = 'regular'
    radius = 6.3712e6


class TestStandardRadius(StandardSolutionTest):
    gridtype = 'regular'
    radius = 6.3712e6 / 16.

    @classmethod
    def post_modify_solution(cls):
        # Divergence and vorticity should be scaled by the inverse of the
        # radius factor.
        cls.solution['vrt'] = cls.solution['vrt'] * 16.
        cls.solution['div'] = cls.solution['div'] * 16.
        cls.solution['vrt_trunc'] = cls.solution['vrt_trunc'] * 16
        # Stream function and velocity potential should be scaled by the
        # radius factor.
        cls.solution['psi'] = cls.solution['psi'] / 16
        cls.solution['chi'] = cls.solution['chi'] / 16


# ----------------------------------------------------------------------------
# Tests for the CDMS interface


class CDMSSolutionTest(SolutionTest):
    """Base class for all CDMS interface solution test classes."""
    interface = 'cdms'

    def test_truncate_reversed(self):
        # vorticity truncated to T21 matches reference?
        vrt_trunc = self.vw.truncate(self.solution['vrt'][::-1], truncation=21)
        self.assert_error_is_zero(vrt_trunc, self.solution['vrt_trunc'])


class TestCDMSRegular(CDMSSolutionTest):
    """Regular grid."""
    gridtype = 'regular'


class TestCDMSGaussian(CDMSSolutionTest):
    """Gaussian grid."""
    gridtype = 'gaussian'


class TestCDMSGridTranspose(CDMSSolutionTest):
    gridtype = 'regular'

    @classmethod
    def pre_modify_solution(cls):
        for field_name in cls.solution:
            cls.solution[field_name] = cls.solution[field_name].reorder('xy')

    def test_truncate_reversed(self):
        # vorticity truncated to T21 matches reference?
        vrt_trunc = self.vw.truncate(self.solution['vrt'][:, ::-1],
                                     truncation=21)
        self.assert_error_is_zero(vrt_trunc, self.solution['vrt_trunc'])


class TestCDMSInvertedLatitude(CDMSSolutionTest):
    gridtype = 'regular'

    @classmethod
    def pre_modify_solution(cls):
        for field_name in ('uwnd', 'vwnd'):
            cls.solution[field_name] = \
                cls.solution[field_name](latitude=(-90, 90))

    @classmethod
    def post_modify_solution(cls):
        for field_name in ('uwnd', 'vwnd'):
            cls.solution[field_name] = \
                cls.solution[field_name](latitude=(90, -90))


class TestCDMSRadiusDefaultExplicit(CDMSSolutionTest):
    gridtype = 'regular'
    radius = 6.3712e6


class TestCDMSRadius(CDMSSolutionTest):
    gridtype = 'regular'
    radius = 6.3712e6 / 16.

    @classmethod
    def post_modify_solution(cls):
        # Divergence and vorticity should be scaled by the inverse of the
        # radius factor.
        cls.solution['vrt'] = cls.solution['vrt'] * 16.
        cls.solution['div'] = cls.solution['div'] * 16.
        cls.solution['vrt_trunc'] = cls.solution['vrt_trunc'] * 16
        # Stream function and velocity potential should be scaled by the
        # radius factor.
        cls.solution['psi'] = cls.solution['psi'] / 16
        cls.solution['chi'] = cls.solution['chi'] / 16

# ----------------------------------------------------------------------------
# Tests for the Iris interface


class IrisSolutionTest(SolutionTest):
    """Base class for all Iris interface solution test classes."""
    interface = 'iris'

    def test_truncate_reversed(self):
        vrt_trunc = self.vw.truncate(self.solution['vrt'][::-1], truncation=21)
        self.assert_error_is_zero(vrt_trunc, self.solution['vrt_trunc'])


class TestIrisRegular(IrisSolutionTest):
    """Regular grid."""
    gridtype = 'regular'


class TestIrisGaussian(IrisSolutionTest):
    """Gaussian grid."""
    gridtype = 'gaussian'


class TestIrisGridTranspose(IrisSolutionTest):
    gridtype = 'regular'

    @classmethod
    def pre_modify_solution(cls):
        for field_name in cls.solution.keys():
            cls.solution[field_name].transpose([1, 0])

    def test_truncate_reversed(self):
        vrt_trunc = self.vw.truncate(self.solution['vrt'][:, ::-1],
                                     truncation=21)
        self.assert_error_is_zero(vrt_trunc, self.solution['vrt_trunc'])


class TestIrisInvertedLatitude(IrisSolutionTest):
    gridtype = 'regular'

    @classmethod
    def pre_modify_solution(cls):
        for field_name in ('uwnd', 'vwnd'):
            cls.solution[field_name] = cls.solution[field_name][::-1]

    @classmethod
    def post_modify_solution(cls):
        for field_name in ('uwnd', 'vwnd'):
            cls.solution[field_name] = cls.solution[field_name][::-1]


class TestIrisRadiusDefaultExplicit(IrisSolutionTest):
    gridtype = 'regular'
    radius = 6.3712e6


class TestIrisRadius(IrisSolutionTest):
    gridtype = 'regular'
    radius = 6.3712e6 / 16.

    @classmethod
    def post_modify_solution(cls):
        # Divergence and vorticity should be scaled by the inverse of the
        # radius factor.
        cls.solution['vrt'] = cls.solution['vrt'] * 16.
        cls.solution['div'] = cls.solution['div'] * 16.
        cls.solution['vrt_trunc'] = cls.solution['vrt_trunc'] * 16
        # Stream function and velocity potential should be scaled by the
        # radius factor.
        cls.solution['psi'] = cls.solution['psi'] / 16
        cls.solution['chi'] = cls.solution['chi'] / 16


# ----------------------------------------------------------------------------
# Tests for the Xarray interface


class XarraySolutionTest(SolutionTest):
    """Base class for all Xarray interface solution test classes."""
    interface = 'xarray'

    def test_truncate_reversed(self):
        vrt_trunc = self.vw.truncate(self.solution['vrt'][::-1], truncation=21)
        self.assert_error_is_zero(vrt_trunc, self.solution['vrt_trunc'])


class TestXarrayRegular(XarraySolutionTest):
    """Regular grid."""
    gridtype = 'regular'


class TestXarrayGaussian(XarraySolutionTest):
    """Gaussian grid."""
    gridtype = 'gaussian'


class TestXarrayGridTranspose(XarraySolutionTest):
    gridtype = 'regular'

    @classmethod
    def pre_modify_solution(cls):
        for field_name in cls.solution.keys():
            cls.solution[field_name] = cls.solution[field_name].transpose()

    def test_truncate_reversed(self):
        vrt_trunc = self.vw.truncate(self.solution['vrt'][:, ::-1],
                                     truncation=21)
        self.assert_error_is_zero(vrt_trunc, self.solution['vrt_trunc'])


class TestXarrayInvertedLatitude(XarraySolutionTest):
    gridtype = 'regular'

    @classmethod
    def pre_modify_solution(cls):
        for field_name in ('uwnd', 'vwnd'):
            cls.solution[field_name] = cls.solution[field_name][::-1]

    @classmethod
    def post_modify_solution(cls):
        for field_name in ('uwnd', 'vwnd'):
            cls.solution[field_name] = cls.solution[field_name][::-1]


class TestXarrayRadiusDefaultExplicit(XarraySolutionTest):
    gridtype = 'regular'
    radius = 6.3712e6


class TestXarrayRadius(XarraySolutionTest):
    gridtype = 'regular'
    radius = 6.3712e6 / 16.

    @classmethod
    def post_modify_solution(cls):
        # Divergence and vorticity should be scaled by the inverse of the
        # radius factor.
        cls.solution['vrt'] = cls.solution['vrt'] * 16.
        cls.solution['div'] = cls.solution['div'] * 16.
        cls.solution['vrt_trunc'] = cls.solution['vrt_trunc'] * 16
        # Stream function and velocity potential should be scaled by the
        # radius factor.
        cls.solution['psi'] = cls.solution['psi'] / 16
        cls.solution['chi'] = cls.solution['chi'] / 16
