"""Test windspharm computations against reference solutions."""
# Copyright (c) 2012-2014 Andrew Dawson
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
from nose.tools import assert_almost_equal
import numpy as np

import windspharm
from windspharm.tests import VectorWindTest, solvers
from .reference import reference_solutions
from .utils import error


class SolutionTest(VectorWindTest):
    """Base class for all solution test classes."""
    interface = None
    gridtype = None

    @classmethod
    def setup_class(cls):
        skip_message = 'library component not available for {!s} interface'
        try:
            cls.solution = reference_solutions(cls.interface, cls.gridtype)
        except ValueError:
            raise SkipTest(skip_message.format(cls.interface))
        cls.modify_solution()
        try:
            # gridtype argument only available for the standard interface
            kwargs = {}
            if cls.interface == 'standard':
                kwargs['gridtype'] = cls.gridtype
            cls.vw = solvers[cls.interface](cls.solution['uwnd'],
                                            cls.solution['vwnd'], **kwargs)
        except KeyError:
            raise SkipTest(skip_message.format(cls.interface))
        cls.unmodify_solution()

    @classmethod
    def modify_solution(cls):
        pass

    @classmethod
    def unmodify_solution(cls):
        pass

    def test_magnitude(self):
        # computed magnitude matches magnitude of reference solution?
        mag1 = self.vw.magnitude()
        mag2 = (self.solution['uwnd'] ** 2 + self.solution['vwnd'] ** 2) ** 0.5
        assert_almost_equal(error(mag1, mag2), 0., places=5)

    def test_vorticity(self):
        # computed vorticity matches reference solution?
        vrt1 = self.vw.vorticity()
        vrt2 = self.solution['vrt']
        assert_almost_equal(error(vrt1, vrt2), 0., places=5)

    def test_divergence(self):
        # computed divergence matches reference solution?
        div1 = self.vw.divergence()
        div2 = self.solution['div']
        assert_almost_equal(error(div1, div2), 0., places=5)

    def test_streamfunction(self):
        # computed streamfunction matches reference solution?
        sf1 = self.vw.streamfunction()
        sf2 = self.solution['psi'].copy()
        assert_almost_equal(error(sf1, sf2), 0., places=5)

    def test_velocitypotential(self):
        # computed velocity potential matches reference solution?
        vp1 = self.vw.velocitypotential()
        vp2 = self.solution['chi'].copy()
        assert_almost_equal(error(vp2, vp2), 0., places=5)

    def test_nondivergent(self):
        # computed non-divergent vector wind matches reference solution?
        upsi1, vpsi1 = self.vw.nondivergentcomponent()
        upsi2, vpsi2 = self.solution['upsi'], self.solution['vpsi']
        assert_almost_equal(error(upsi1, upsi2), 0., places=5)
        assert_almost_equal(error(upsi1, upsi2), 0., places=5)

    def test_irrotational(self):
        # computed irrotational vector wind matches reference solution?
        uchi1, vchi1 = self.vw.irrotationalcomponent()
        uchi2, vchi2 = self.solution['uchi'], self.solution['vchi']
        assert_almost_equal(error(uchi1, uchi2), 0., places=5)
        assert_almost_equal(error(vchi1, vchi2), 0., places=5)

    def test_gradient(self):
        # computed gradient matches reference solution?
        uchi1, vchi1 = self.vw.gradient(self.solution['chi'])
        uchi2, vchi2 = self.solution['chigradu'], self.solution['chigradv']
        assert_almost_equal(error(uchi1, uchi2), 0., places=5)
        assert_almost_equal(error(vchi1, vchi2), 0., places=5)

    def test_vrtdiv(self):
        # vrtdiv() matches vorticity()/divergence()?
        vrt1, div1 = self.vw.vrtdiv()
        vrt2 = self.vw.vorticity()
        div2 = self.vw.divergence()
        assert_almost_equal(error(vrt1, vrt2), 0., places=5)
        assert_almost_equal(error(div1, div2), 0., places=5)

    def test_sfvp(self):
        # sfvp() matches streamfunction()/velocitypotential()?
        sf1, vp1 = self.vw.sfvp()
        sf2 = self.vw.streamfunction()
        vp2 = self.vw.velocitypotential()
        assert_almost_equal(error(sf1, sf2), 0., places=5)
        assert_almost_equal(error(vp1, vp2), 0., places=5)

    def test_helmholtz(self):
        # helmholtz() matches irrotationalcomponent()/nondivergentcomponent()?
        uchi1, vchi1, upsi1, vpsi1 = self.vw.helmholtz()
        uchi2, vchi2 = self.vw.irrotationalcomponent()
        upsi2, vpsi2 = self.vw.nondivergentcomponent()
        uchi, vchi, upsi2, vpsi2 = self.vw.helmholtz()
        assert_almost_equal(error(uchi1, uchi2), 0., places=5)
        assert_almost_equal(error(vchi1, vchi2), 0., places=5)
        assert_almost_equal(error(upsi1, upsi2), 0., places=5)
        assert_almost_equal(error(vpsi1, vpsi2), 0., places=5)

    def test_truncate(self):
        # vorticity truncated to T21 matches reference?
        div_trunc = self.vw.truncate(self.solution['vrt'], truncation=21)
        assert_almost_equal(error(div_trunc, self.solution['vrt_trunc']),
                            0., places=5)


#-----------------------------------------------------------------------------
# Tests for the standard interface


class StandardSolutionTest(SolutionTest):
    """Base class for all standard interface solution test classes."""
    interface = 'standard'


class TestStandardRegular(StandardSolutionTest):
    """Regular grid."""
    gridtype = 'regular'


#class TestStandardGaussian(StandardSolutionTest):
#    """Gaussian grid."""
#    gridtype = 'gaussian'


class TestStandardRegularSingleton(StandardSolutionTest):
    """Singleton right-most dimension."""
    gridtype = 'regular'

    @classmethod
    def modify_solution(cls):
        for field_name in cls.solution:
            cls.solution[field_name] = \
                cls.solution[field_name][..., np.newaxis]


#class TestStandardGaussianSingleton(StandardSolutionTest):
#    """Singleton right-most dimension."""
#    gridtype = 'gaussian'
#
#    @classmethod
#    def modify_solution(cls):
#        cls.solution['uwnd'] = cls.solution['uwnd'][..., np.newaxis]
#        cls.solution['vwnd'] = cls.solution['vwnd'][..., np.newaxis]


class TestStandardMultiTime(StandardSolutionTest):
    gridtype = 'regular'

    @classmethod
    def modify_solution(cls):
        repeater = lambda a: a[..., np.newaxis].repeat(5, axis=-1)
        for field_name in cls.solution:
            cls.solution[field_name] = repeater(cls.solution[field_name])


#-----------------------------------------------------------------------------
# Tests for the CDMS interface


class CDMSSolutionTest(SolutionTest):
    """Base class for all CDMS interface solution test classes."""
    interface = 'cdms'


class TestCDMSRegular(CDMSSolutionTest):
    """Regular grid."""
    gridtype = 'regular'


#class TestCDMSGaussian(CDMSSolutionTest):
#    """Gaussian grid."""
#    gridtype = 'gaussian'


class TestCDMSGridTranspose(CDMSSolutionTest):
    gridtype = 'regular'

    @classmethod
    def modify_solution(cls):
        for field_name in cls.solution:
            cls.solution[field_name] = cls.solution[field_name].reorder('xy')

class TestCDMSInvertedLatitude(CDMSSolutionTest):
    gridtype = 'regular'

    @classmethod
    def modify_solution(cls):
        for field_name in ('uwnd', 'vwnd'):
            cls.solution[field_name] = \
                cls.solution[field_name](latitude=(-90, 90))

    @classmethod
    def unmodify_solution(cls):
        for field_name in ('uwnd', 'vwnd'):
            cls.solution[field_name] = \
                cls.solution[field_name](latitude=(90, -90))


#-----------------------------------------------------------------------------
# Tests for the Iris interface


class IrisSolutionTest(SolutionTest):
    """Base class for all Iris interface solution test classes."""
    interface = 'iris'


class TestIrisRegular(IrisSolutionTest):
    """Regular grid."""
    gridtype = 'regular'


#class TestIrisGaussian(IrisSolutionTest):
#    """Gaussian grid."""
#    gridtype = 'gaussian'


class TestIrisGridTranspose(IrisSolutionTest):
    gridtype = 'regular'

    @classmethod
    def modify_solution(cls):
        for field_name in cls.solution.keys():
            cls.solution[field_name].transpose([1, 0])


class TestIrisInvertedLatitude(IrisSolutionTest):
    gridtype = 'regular'

    @classmethod
    def modify_solution(cls):
        for field_name in ('uwnd', 'vwnd'):
            cls.solution[field_name] = cls.solution[field_name][::-1]

    @classmethod
    def unmodify_solution(cls):
        for field_name in ('uwnd', 'vwnd'):
            cls.solution[field_name] = cls.solution[field_name][::-1]
