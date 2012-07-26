"""
Test cases for vector wind computational interfaces
:py:class:`windspharm.standard.VectorWind` and
:py:class:`windspharm.metadata.VectorWind`.

"""
import unittest
from unittest import TestCase

import numpy as np
try:
    import cdms2
except ImportError:
    pass

import windspharm
from testutils import generate_test_data, error, identify


class VectorWindTestCase(TestCase):
    """Functionality of the standard :py:mod:`numpy` interface."""

    def __str__(self):
        return 'validating against reference solution (standard interface)'

    def setUp(self):
        self.ref = generate_test_data('standard')
        self.vw = windspharm.standard.VectorWind(self.ref['uwnd'],
                self.ref['vwnd'], gridtype='regular')

    def test_vorticity(self):
        identify('vorticity')
        vrt1 = self.vw.vorticity()
        vrt2 = self.ref['vrt']
        err = error(vrt1, vrt2)
        self.assertAlmostEqual(err, 0., places=5)

    def test_divergence(self):
        identify('divergence')
        div1 = self.vw.divergence()
        div2 = self.ref['div']
        err = error(div1, div2)
        self.assertAlmostEqual(err, 0., places=5)

    def test_streamfunction(self):
        identify('streamfunction')
        psi1 = self.vw.streamfunction()
        psi2 = self.ref['psi'].copy()
        err = error(psi1, psi2)
        self.assertAlmostEqual(err, 0., places=5)

    def test_velocitypotential(self):
        identify('velocity potential')
        chi1 = self.vw.velocitypotential()
        chi2 = self.ref['chi'].copy()
        err = error(chi1, chi2)
        self.assertAlmostEqual(err, 0., places=5)
    
    def test_nondivergent(self):
        identify('non-divergent component')
        upsi1, vpsi1 = self.vw.nondivergentcomponent()
        upsi2, vpsi2 = self.ref['upsi'], self.ref['vpsi']
        erru = error(upsi1, upsi2)
        errv = error(vpsi1, vpsi2)
        self.assertAlmostEqual(erru, 0., places=5)
        self.assertAlmostEqual(errv, 0., places=5)

    def test_irrotational(self):
        identify('irrotational component')
        uchi1, vchi1 = self.vw.irrotationalcomponent()
        uchi2, vchi2 = self.ref['uchi'], self.ref['vchi']
        erru = error(uchi1, uchi2)
        errv = error(vchi1, vchi2)
        self.assertAlmostEqual(erru, 0., places=5)
        self.assertAlmostEqual(errv, 0., places=5)

    def test_gradient(self):
        identify('gradient function')
        uchi1, vchi1 = self.vw.gradient(self.ref['chi'])
        uchi2, vchi2 = self.ref['chigradu'], self.ref['chigradv']
        erru = error(uchi1, uchi2)
        errv = error(vchi1, vchi2)
        self.assertAlmostEqual(erru, 0., places=5)
        self.assertAlmostEqual(errv, 0., places=5)

    def test_vorticity_crosscheck(self):
        identify('vorticity (cross-check)')
        vrt1 = self.vw.vorticity()
        vrt2, div = self.vw.vrtdiv()
        err = error(vrt1, vrt2)
        self.assertAlmostEqual(err, 0., places=5)

    def test_divergence_crosscheck(self):
        identify('divergence (cross-check)')
        div1 = self.vw.divergence()
        vrt, div2 = self.vw.vrtdiv()
        err = error(div1, div2)
        self.assertAlmostEqual(err, 0., places=5)

    def test_streamfunction_crosscheck(self):
        identify('streamfunction (cross-check)')
        sf1 = self.vw.streamfunction()
        sf2, vp = self.vw.sfvp()
        err = error(sf1, sf2)
        self.assertAlmostEqual(err, 0., places=5)

    def test_velocitypotential_crosscheck(self):
        identify('velocity potential (cross-check)')
        vp1 = self.vw.velocitypotential()
        sf, vp2 = self.vw.sfvp()
        err = error(vp1, vp2)
        self.assertAlmostEqual(err, 0., places=5)

    def test_nondivergent_crosscheck(self):
        identify('non-divergent component (cross-check)')
        upsi1, vpsi1 = self.vw.nondivergentcomponent()
        uchi, vchi, upsi2, vpsi2 = self.vw.helmholtz()
        erru = error(upsi1, upsi2)
        errv = error(vpsi1, vpsi2)
        self.assertAlmostEqual(erru, 0., places=5)
        self.assertAlmostEqual(errv, 0., places=5)

    def test_irrotational_crosscheck(self):
        identify('irrotational component (cross-check)')
        uchi1, vchi1 = self.vw.irrotationalcomponent()
        uchi2, vchi2, upsi, vpsi = self.vw.helmholtz()
        erru = error(uchi1, uchi2)
        errv = error(vchi1, vchi2)
        self.assertAlmostEqual(erru, 0., places=5)
        self.assertAlmostEqual(errv, 0., places=5)


@unittest.skipIf('metadata' not in dir(windspharm) or 'cdms2' not in dir(),
        'library component not available')
class VectorWindMetaDataTestCase(VectorWindTestCase):
    """
    Functionality of the meta-data enabled :py:mod:`cdms2` interface.
    
    """

    def __str__(self):
        return 'validating against reference solution (meta-data interface)'

    def setUp(self):
        self.ref = generate_test_data('metadata')
        self.vw = windspharm.metadata.VectorWind(self.ref['uwnd'],
                self.ref['vwnd'])


class MultipleFieldsTest(TestCase):
    """Consistency for multiple field computations."""

    def __str__(self):
        return 'validating soulution with multiple fields'

    def setUp(self):
        self.ref = generate_test_data('standard')
        self.vw = windspharm.standard.VectorWind(self.ref['uwnd'],
                self.ref['vwnd'])

    def test_multiple_fields(self):
        identify('multiple fields')
        uwnd_multi = np.concatenate((self.ref['uwnd'][...,np.newaxis],
                self.ref['uwnd'][...,np.newaxis]), axis=-1)
        vwnd_multi = np.concatenate((self.ref['vwnd'][...,np.newaxis],
                self.ref['vwnd'][...,np.newaxis]), axis=-1)
        vw_multi = windspharm.standard.VectorWind(uwnd_multi, vwnd_multi)
        vw_single = windspharm.standard.VectorWind(self.ref['uwnd'],
                self.ref['vwnd'])
        vrt_multi = vw_multi.vorticity()
        vrt_single = vw_single.vorticity()
        err1 = error(vrt_multi[...,0], vrt_single)
        err2 = error(vrt_multi[...,1], vrt_single)
        self.assertAlmostEqual(err1, 0., places=7)
        self.assertAlmostEqual(err2, 0., places=7)


if __name__ == '__main__':
    pass

