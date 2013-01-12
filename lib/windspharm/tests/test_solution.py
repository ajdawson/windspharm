"""Test vector wind computations against reference solutions.

Includes tests for: :py:class:`windspharm.standard.VectorWind`,
:py:class:`windspharm.iris.VectorWind` and
:py:class:`windspharm.cdms.VectorWind`.

"""
from __future__ import absolute_import
from nose import SkipTest
from nose.tools import assert_almost_equal
from unittest import skipIf
import numpy as np

import windspharm

from .reference import reference_solutions
from .utils import error


class TestStandard(object):
    """Tests for the :py:mod:`numpy` interface solutions."""

    @classmethod
    def setup_class(cls):
        cls.ref = reference_solutions('standard')
        cls.vw = windspharm.standard.VectorWind(
                cls.ref['uwnd'], cls.ref['vwnd'], gridtype='regular')

    def test_vorticity(self):
        """computed vorticity matches reference solution?"""
        vrt1 = self.vw.vorticity()
        vrt2 = self.ref['vrt']
        assert_almost_equal(error(vrt1, vrt2), 0., places=5)

    def test_divergence(self):
        """computed divergence matches reference solution?"""
        div1 = self.vw.divergence()
        div2 = self.ref['div']
        assert_almost_equal(error(div1, div2), 0., places=5)

    def test_streamfunction(self):
        """computed streamfunction matches reference solution?"""
        sf1 = self.vw.streamfunction()
        sf2 = self.ref['psi'].copy()
        assert_almost_equal(error(sf1, sf2), 0., places=5)

    def test_velocitypotential(self):
        """computed velocity potential matches reference solution?"""
        vp1 = self.vw.velocitypotential()
        vp2 = self.ref['chi'].copy()
        assert_almost_equal(error(vp2, vp2), 0., places=5)

    def test_nondivergent(self):
        """
        computed non-divergent vector wind matches reference solution?

        """
        upsi1, vpsi1 = self.vw.nondivergentcomponent()
        upsi2, vpsi2 = self.ref['upsi'], self.ref['vpsi']
        assert_almost_equal(error(upsi1, upsi2), 0., places=5)
        assert_almost_equal(error(upsi1, upsi2), 0., places=5)

    def test_irrotational(self):
        """
        computed irrotational vector wind matches reference solution?

        """
        uchi1, vchi1 = self.vw.irrotationalcomponent()
        uchi2, vchi2 = self.ref['uchi'], self.ref['vchi']
        assert_almost_equal(error(uchi1, uchi2), 0., places=5)
        assert_almost_equal(error(vchi1, vchi2), 0., places=5)

    def test_gradient(self):
        """computed gradient matches reference solution?"""
        uchi1, vchi1 = self.vw.gradient(self.ref['chi'])
        uchi2, vchi2 = self.ref['chigradu'], self.ref['chigradv']
        assert_almost_equal(error(uchi1, uchi2), 0., places=5)
        assert_almost_equal(error(vchi1, vchi2), 0., places=5)

    def test_vrtdiv(self):
        """vrtdiv() matches vorticity()/divergence()?"""
        vrt1, div1 = self.vw.vrtdiv()
        vrt2 = self.vw.vorticity()
        div2 = self.vw.divergence()
        assert_almost_equal(error(vrt1, vrt2), 0., places=5)
        assert_almost_equal(error(div1, div2), 0., places=5)

    def test_sfvp(self):
        """sfvp() matches streamfunction()/velocitypotential()?"""
        sf1, vp1 = self.vw.sfvp()
        sf2 = self.vw.streamfunction()
        vp2 = self.vw.velocitypotential()
        assert_almost_equal(error(sf1, sf2), 0., places=5)
        assert_almost_equal(error(vp1, vp2), 0., places=5)

    def test_helmholtz(self):
        """
        helmholtz() matches irrotationalcomponent()/nondivergentcomponent()?

        """
        uchi1, vchi1, upsi1, vpsi1 = self.vw.helmholtz()
        uchi2, vchi2 = self.vw.irrotationalcomponent()
        upsi2, vpsi2 = self.vw.nondivergentcomponent()
        uchi, vchi, upsi2, vpsi2 = self.vw.helmholtz()
        assert_almost_equal(error(uchi1, uchi2), 0., places=5)
        assert_almost_equal(error(vchi1, vchi2), 0., places=5)
        assert_almost_equal(error(upsi1, upsi2), 0., places=5)
        assert_almost_equal(error(vpsi1, vpsi2), 0., places=5)


class TestCDMS(TestStandard):
    """Tests for the :py:mod:`cdms2` interface solutions."""

    @classmethod
    def setup_class(cls):
        try:
            cls.ref = reference_solutions('cdms')
            cls.vw = windspharm.cdms.VectorWind(
                    cls.ref['uwnd'], cls.ref['vwnd'])
        except ValueError:
            raise SkipTest('library component (cdms2) not available')


class TestIris(TestStandard):
    """Tests for the :py:mod:`iris` interface solutions."""

    @classmethod
    def setup_class(cls):
        try:
            cls.ref = reference_solutions('iris')
            cls.vw = windspharm.iris.VectorWind(
                    cls.ref['uwnd'], cls.ref['vwnd'])
        except ValueError:
            raise SkipTest('library component (iris) not available')


class TestMultiple(object):
    """Tests for solutions with multiple fields."""

    @classmethod
    def setup_class(cls):
        cls.ref = reference_solutions('standard')

    def test_multiple(self):
        """multi-field solution matches individual solutions?"""
        u = self.ref['uwnd']
        v = self.ref['vwnd']
        u_multi = u[..., np.newaxis].repeat(5, axis=-1)
        v_multi = v[..., np.newaxis].repeat(5, axis=-1)
        vw_multi = windspharm.standard.VectorWind(u_multi, v_multi)
        vw_single = windspharm.standard.VectorWind(u, v)
        vrt_multi = vw_multi.vorticity()
        vrt_single = vw_single.vorticity()
        for dim in xrange(5):
            assert_almost_equal(error(vrt_multi[...,dim], vrt_single), 0.)


if __name__ == '__main__':
    pass
