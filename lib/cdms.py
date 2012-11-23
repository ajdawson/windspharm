"""Spherical harmonic vector wind computations (meta-data interface)."""
# Copyright (c) 2012 Andrew Dawson
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
import cdms2

from . import standard


class VectorWind(object):
    """
    Vector wind computations (meta-data enabled :py:mod:`cdms2`
    interface).

    """

    def __init__(self, u, v):
        """Initialize a VectorWind instance.

        **Arguments:**

        *u*, *v*
            Zonal and meridional components of the vector wind
            respectively. Both components should be :py:mod:`cdms2`
            variables. The components must have the same shape and
            contain no missing values.

        **Example:**

        Initialize a VectorWind instance with zonal and meridional
        components of the vector wind:

        >>> from windspharm.metadata import VectorWind
        >>> w = VectorWind(u, v)

        """
        # Ensure the input are cdms2 variables.
        if not (cdms2.isVariable(u) and cdms2.isVariable(v)):
            raise TypeError('u and v must be cdms2 variables')
        # Check that both u and v have dimensions in the same order and that
        # there are latitude and longitude dimensions present.
        uorder = u.getOrder()
        vorder = v.getOrder()
        if uorder != vorder:
            raise ValueError('u and v must have the same dimension order')
        for order in (uorder, vorder):
            if 'x' not in order or 'y' not in order:
                raise ValueError('a latitude-longitude grid is required')
        self.order = uorder
        # Assess how to re-order the inputs to be compatible with the
        # computation API.
        apiorder = 'yx' + ''.join([a for a in order if a not in 'xy'])
        # Order the dimensions correctly.
        u = u.reorder(apiorder)
        v = v.reorder(apiorder)
        # Do a region selection on the inputs to ensure the latitude dimension
        # is north-to-south.
        u = u(latitude=(90,-90))
        v = v(latitude=(90,-90))
        # Determine the grid type,
        lon = u.getLongitude()
        lat = u.getLatitude()
        if lon is None or lat is None:
            raise ValueError('a latitude-longitude grid is required')
        gridtype = self._gridtype(lat)
        # Store the shape and axes when data is in the API order.
        self.ishape = u.shape
        self.axes = u.getAxisList()
        # Re-shape to 3-dimensional (compatible with API)
        u = u.reshape(u.shape[:2] + (np.prod(u.shape[2:]),))
        v = v.reshape(v.shape[:2] + (np.prod(v.shape[2:]),))
        # Instantiate a VectorWind object to do the computations.
        self.api = standard.VectorWind(u, v, gridtype=gridtype)

    def _gridtype(self, lat):
        """Determines the type of grid from the latitude dimension.

        Performs basic checks to make sure the axis is valid for
        spherical harmonic computations.

        """
        nlat = len(lat)
        d = np.abs(np.diff(lat))
        if (np.abs(d - d[0]) > 0.001).any():
            # Might be a Gaussian axis, construct one and check.
            gax = cdms2.createGaussianAxis(nlat)
            d = np.abs(np.abs(lat) - np.abs(gax))
            if (d > 0.001).any():
                raise ValueError('non-evenly-spaced latitudes are not Gaussian')
            gridtype = 'gaussian'
        else:
            # Grid is evenly spaced, does it match what we expect?
            if nlat % 2:
                eax = np.linspace(-90, 90, nlat)
            else:
                dlat = 180. / nlat
                eax = np.linspace(-90+0.5*dlat, 90-0.5*dlat, nlat)
            d = np.abs(np.abs(lat) - np.abs(eax))
            if (d > 0.001).any():
                raise ValueError('evenly-spaced grid is invalid')
            gridtype = 'regular'
        return gridtype

    def _metadata(self, var, **attributes):
        """Re-shape and re-order raw results, and add meta-data."""
        if 'id' not in attributes.keys():
            raise ValueError('meta-data construction requires id')
        var = cdms2.createVariable(var.reshape(self.ishape), axes=self.axes)
        var = var.reorder(self.order)
        for attribute, value in attributes.items():
            setattr(var, attribute, value)
        return var

    def u(self):
        """Zonal component of vector wind.

        **Example:**

        >>> u = w.u()

        """
        u = self.api.u
        u = self._metadata(u, id='u', standard_name='eastward_wind',
                units='m s**-1', long_name='eastward component of wind')
        return u

    def v(self):
        """Meridional component of vector wind.

        **Example:**

        >>> v = w.v()

        """
        v = self.api.v
        v = self._metadata(v, id='v', standard_name='northward_wind',
                units='m s**-1', long_name='northward component of wind')
        return v

    def magnitude(self):
        """Wind speed (magnitude of vector wind).

        **Example:**

        >>> spd = w.magnitude()

        """
        m = self.api.magnitude()
        m = self._metadata(m, id='mag', standard_name='wind_speed',
                units='m s**-1', long_name='wind speed')
        return m

    def vrtdiv(self, truncation=None):
        """Relative vorticity and horizontal divergence.

        **Optional argument:**

        *truncation*
            Truncation limit (triangular truncation) for the spherical
            harmonic computation.

        **Examples:**

        Compute the relative vorticity and divergence:

        >>> vrt, div = w.vrtdiv()

        Compute the relative vorticity and divergence and apply spectral
        truncation at triangular T13:

        >>> vrtT13, divT13 = w.vrtdiv(truncation=13)

        """
        vrt, div = self.api.vrtdiv(truncation=truncation)
        vrt = self._metadata(vrt, id='vrt', units='s**-1',
                standard_name='atmosphere_relative_vorticity',
                long_name='relative vorticity')
        div = self._metadata(div, id='div', units='s**-1',
                standard_name='divergence_of_wind',
                long_name='horizontal divergence')
        return vrt, div

    def vorticity(self, truncation=None):
        """Relative vorticity.

        **Optional argument:**

        *truncation*
            Truncation limit (triangular truncation) for the spherical
            harmonic computation.

        **Examples:**

        Compute the relative vorticity:

        >>> vrt = w.vorticity()

        Compute the relative vorticity and apply spectral truncation at
        triangular T13:

        >>> vrtT13 = w.vorticity(truncation=13)

        """
        vrt = self.api.vorticity(truncation=truncation)
        vrt = self._metadata(vrt, id='vrt', units='s**-1',
                standard_name='atmosphere_relative_vorticity',
                long_name='relative vorticity')
        return vrt

    def divergence(self, truncation=None):
        """Horizontal divergence.

        **Optional argument:**

        *truncation*
            Truncation limit (triangular truncation) for the spherical
            harmonic computation.

        **Examples:**

        Compute the divergence:

        >>> div = w.divergence()

        Compute the divergence and apply spectral truncation at
        triangular T13:

        >>> divT13 = w.divergence(truncation=13)

        """
        div = self.api.divergence(truncation=truncation)
        div = self._metadata(div, id='div', units='s**-1',
                standard_name='divergence_of_wind',
                long_name='horizontal divergence')
        return div

    def planetaryvorticity(self, omega=None):
        """Planetary vorticity (Coriolis parameter).

        **Optional argument:**

        *omega*
            Earth's angular velocity. The default value if not specified
            is 7.292x10**-5 s**-1.

        **Example:**

        Compute planetary vorticity using default values:

        >>> pvrt = w.planetaryvorticity()

        Override the default value for Earth's angular velocity:

        >>> pvrt = w.planetaryvorticity(omega=7.2921150)

        """
        f = self.api.planetaryvorticity(omega=omega)
        f = self._metadata(f, id='f', units='s**-1',
                standard_name='coriolis_parameter',
                long_name='planetary vorticity (coriolis parameter)')
        return f

    def absolutevorticity(self, omega=None, truncation=None):
        """Absolute vorticity (sum of relative and planetary vorticity).

        **Optional arguments:**

        *omega*
            Earth's angular velocity. The default value if not specified
            is 7.292x10**-5 s**-1.

        *truncation*
            Truncation limit (triangular truncation) for the spherical
            harmonic computation.

        **Examples:**

        Compute absolute vorticity:

        >>> avrt = w.absolutevorticity()

        Compute absolute vorticity and apply spectral truncation at
        triangular T13, also override the default value for Earth's
        angular velocity:

        >>> avrt = w.absolutevorticity(omega=7.2921150, truncation=13)

        """
        avrt = self.api.absolutevorticity(omega=omega, truncation=truncation)
        avrt = self._metadata(avrt, id='absvrt', units='s**-1',
                standard_name='atmosphere_absolute_vorticity',
                long_name='absolute vorticity')
        return avrt

    def sfvp(self, truncation=None):
        """Streamfunction and velocity potential.

        **Optional argument:**

        *truncation*
            Truncation limit (triangular truncation) for the spherical
            harmonic computation.

        **Examples:**

        Compute streamfunction and velocity potential:

        >>> sf, vp = w.sfvp()

        Compute streamfunction and velocity potential and apply spectral
        truncation at triangular T13:

        >>> sfT13, vpT13 = w.sfvp(truncation=13)

        """
        sf, vp = self.api.sfvp(truncation=truncation)
        sf = self._metadata(sf, id='psi', units='m**2 s**-1',
                standard_name='atmosphere_horizontal_streamfunction',
                long_name='streamfunction')
        vp = self._metadata(vp, id='chi', units='m**2 s**-1',
                standard_name='atmosphere_horizontal_velocity_potential',
                long_name='velocity potential')
        return sf, vp

    def streamfunction(self, truncation=None):
        """Streamfunction.

        **Optional argument:**

        *truncation*
            Truncation limit (triangular truncation) for the spherical
            harmonic computation.

        **Examples:**

        Compute streamfunction:

        >>> sf = w.streamfunction()

        Compute streamfunction and apply spectral truncation at
        triangular T13:

        >>> sfT13 = w.streamfunction(truncation=13)

        """
        sf = self.api.streamfunction(truncation=truncation)
        sf = self._metadata(sf, id='psi', units='m**2 s**-1',
                standard_name='atmosphere_horizontal_streamfunction',
                long_name='streamfunction')
        return sf

    def velocitypotential(self, truncation=None):
        """Velocity potential.

        **Optional argument:**

        *truncation*
            Truncation limit (triangular truncation) for the spherical
            harmonic computation.

        **Examples:**

        Compute velocity potential:

        >>> vp = w.velocity potential()

        Compute velocity potential and apply spectral truncation at
        triangular T13:

        >>> vpT13 = w.velocity potential(truncation=13)

        """
        vp = self.api.velocitypotential(truncation=truncation)
        vp = self._metadata(vp, id='chi', units='m**2 s**-1',
                standard_name='atmosphere_horizontal_velocity_potential',
                long_name='velocity potential')
        return vp

    def helmholtz(self, truncation=None):
        """Irrotational and non-divergent components of the vector wind.

        Returns a 4-tuple of the eastward and northward components of
        the irrotational and non-divergent wind components respectively.

        **Optional argument:**

        *truncation*
            Truncation limit (triangular truncation) for the spherical
            harmonic computation.

        **Examples:**

        Compute the irrotational and non-divergent components of the
        vector wind:

        >>> uchi, vchi, upsi, vpsi = w.helmholtz()

        Compute the irrotational and non-divergent components of the
        vector wind and apply spectral truncation at triangular T13:

        >>> uchiT13, vchiT13, upsiT13, vpsiT13 = \
w.helmholtz(truncation=13)

        """
        uchi, vchi, upsi, vpsi = self.api.helmholtz(truncation=truncation)
        uchi = self._metadata(uchi, id='uchi', units='m s**-1',
                long_name='irrotational_eastward_wind')
        vchi = self._metadata(vchi, id='vchi', units='m s**-1',
                long_name='irrotational_northward_wind')
        upsi = self._metadata(upsi, id='upsi', units='m s**-1',
                long_name='non_divergent_eastward_wind')
        vpsi = self._metadata(vpsi, id='vpsi', units='m s**-1',
                long_name='non_divergent_northward_wind')
        return uchi, vchi, upsi, vpsi

    def irrotationalcomponent(self, truncation=None):
        """Irrotational (divergent) component of the vector wind.

        Returns a 2-tuple of the eastward and northward components of
        the irrotational wind. If both the irrotational and
        non-divergent components are required use
        :py:meth:`~windspharm.metadata.VectorWind.helmholtz` instead.

        **Optional argument:**

        *truncation*
            Truncation limit (triangular truncation) for the spherical
            harmonic computation.

        **Examples:**

        Compute the irrotational component of the vector wind:

        >>> uchi, vchi = w.irrotationalcomponent()

        Compute the irrotational component of the vector wind and apply
        spectral truncation at triangular T13:

        >>> uchiT13, vchiT13 = w.irrotationalcomponent(truncation=13)

        """
        uchi, vchi = self.api.irrotationalcomponent(truncation=truncation)
        uchi = self._metadata(uchi, id='uchi', units='m s**-1',
                long_name='irrotational_eastward_wind')
        vchi = self._metadata(vchi, id='vchi', units='m s**-1',
                long_name='irrotational_northward_wind')
        return uchi, vchi

    def nondivergentcomponent(self, truncation=None):
        """Non-divergent (rotational) component of the vector wind.

        Returns a 2-tuple of the eastward and northward components of
        the non-divergent wind. If both the irrotational and
        non-divergent components are required use
        :py:meth:`~windspharm.metadata.VectorWind.helmholtz` instead.

        **Optional argument:**

        *truncation*
            Truncation limit (triangular truncation) for the spherical
            harmonic computation.

        **Examples:**

        Compute the non-divergent component of the vector wind:

        >>> upsi, vpsi = w.nondivergentcomponent()

        Compute the non-divergent component of the vector wind and apply
        spectral truncation at triangular T13:

        >>> upsiT13, vpsiT13 = w.nondivergentcomponent(truncation=13)

        """
        upsi, vpsi = self.api.nondivergentcomponent(truncation=truncation)
        upsi = self._metadata(upsi, id='upsi', units='m s**-1',
                long_name='non_divergent_eastward_wind')
        vpsi = self._metadata(vpsi, id='vpsi', units='m s**-1',
                long_name='non_divergent_northward_wind')
        return upsi, vpsi

    def gradient(self, chi, truncation=None):
        """Computes the vector gradient of a scalar field on the sphere.

        Returns a 2-tuple of the zonal and meridional components of the
        vector gradient respectively.

        **Argument:**

        *chi*
            A scalar field. It must have the same latitude and longitude
            dimensions as the vector wind components that initialized
            the VectorWind instance.

        **Optional argument:**

        *truncation*
            Truncation limit (triangular truncation) for the spherical
            harmonic computation.

        **Examples:**

        Compute the vector gradient of absolute vorticity:

        >>> avrt = w.absolutevorticity()
        >>> avrt_zonal, avrt_meridional = w.gradient(avrt)

        Compute the vector gradient of absolute vorticity and apply
        spectral truncation at triangular T13:

        >>> avrt = w.absolutevorticity()
        >>> avrt_zonalT13, avrt_meridionalT13 = \
w.gradient(avrt, truncation=13)

        """
        # Check that the input is a cdms2 variable.
        if not cdms2.isVariable(chi):
            raise ValueError('scalar field must be a cdms2 variable')
        order = chi.getOrder()
        if 'x' not in order or 'y' not in order:
            raise ValueError('a latitude-longitude grid is required')
        # Assess how to re-order the inputs to be compatible with the
        # computation API.
        apiorder = 'yx' + ''.join([a for a in order if a not in 'xy'])
        chi = chi.reorder(apiorder)
        # Record the shape and axes in the API order.
        ishape = chi.shape
        axes = chi.getAxisList()
        # Re-order to the API order.
        chi = chi.reshape(chi.shape[:2] + (np.prod(chi.shape[2:]),))
        # Compute the gradient function.
        uchi, vchi = self.api.gradient(chi, truncation=truncation)
        uchi = uchi.reshape(ishape)
        vchi = vchi.reshape(ishape)
        # Add meta-data and ensure the shape and order of dimensions
        # is the same as input.
        uchi = cdms2.createVariable(uchi, axes=axes)
        vchi = cdms2.createVariable(vchi, axes=axes)
        uchi = uchi.reorder(order)
        vchi = vchi.reorder(order)
        uchi.id = '{0:s}_zonal'.format(chi.id)
        vchi.id = '{0:s}_meridional'.format(chi.id)
        uchi.long_name='zonal_gradient_of_{0:s}'.format(chi.id)
        vchi.long_name='meridional_gradient_of_{0:s}'.format(chi.id)
        return uchi, vchi


if __name__ == '__main__':
    pass

