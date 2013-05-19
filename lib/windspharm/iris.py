"""
Spherical harmonic vector wind computations (:py:mod:`iris` meta-data
interface).

"""
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
from iris.cube import Cube
from iris.util import reverse
from spharm import gaussian_lats_wts

from . import standard


class VectorWind(object):
    """
    Vector wind computations (meta-data enabled :py:mod:`iris`
    interface).

    """

    def __init__(self, u, v):
        """Initialize a VectorWind instance.

        **Arguments:**

        *u*, *v*
            Zonal and meridional components of the vector wind
            respectively. Both components should be instances of
            :py:class:`iris.cube.Cube`. The components must have the
            same dimension coordinates and contain no missing values.

        **Example:**

        Initialize a :py:class:`~windspharm.iris.VectorWind` instance
        with zonal and meridional components of the vector wind:

            from windspharm.iris import VectorWind
            w = VectorWind(u, v)

        """
        # Make sure inputs are Iris cubes.
        if type(u) is not Cube or type(v) is not Cube:
            raise TypeError('u and v must be iris cubes')
        # Get the coordinates of each component and make sure they are the
        # same.
        ucoords = u.dim_coords
        vcoords = v.dim_coords
        if ucoords != vcoords:
            raise ValueError('u and v must have the same dimensions')
        # Extract the latitude and longitude dimension coordinates.
        lat, lat_dim = _dim_coord_and_dim(u, 'latitude')
        lon, lon_dim = _dim_coord_and_dim(v, 'longitude')
        # Determine the ordering list (input to transpose) which will put the
        # latitude and longitude dimensions at the front of the cube's
        # dimensions, and the ordering list which will reverse this process.
        apiorder, self._reorder = self._get_apiorder_reorder(
            u, lat_dim, lon_dim)
        # Re-order the inputs (in-place, so we take a copy first) so latiutude
        # and longitude are at the front.
        u = u.copy()
        v = v.copy()
        u.transpose(apiorder)
        v.transpose(apiorder)
        # Reverse the latitude dimension if necessary.
        if (lat.points[0] < lat.points[1]):
            # need to reverse latitude dimension
            u = reverse(u, lat_dim)
            v = reverse(v, lat_dim)
        # Determine the grid type of the input.
        gridtype = self._gridtype(lat.points)
        # Records the current shape and dimension coordinates of the inputs.
        self._ishape = u.shape
        self._coords = u.dim_coords
        # Reshape the inputs so they are compatible with pyspharm.
        u = u.data.reshape(u.shape[:2] + (np.prod(u.shape[2:]),))
        v = v.data.reshape(v.shape[:2] + (np.prod(v.shape[2:]),))
        # Create a base VectorWind instance to do the computations.
        self._api = standard.VectorWind(u, v, gridtype=gridtype)

    def _gridtype(self, latitudes):
        """Determine the type of a latitude dimension."""
        # Define a tolerance value for differences, this value must be much
        # smaller than expected grid spacings.
        tolerance = 0.001
        # Get the number of latitude points in the dimension.
        nlat = len(latitudes)
        diffs = np.abs(np.diff(latitudes))
        equally_spaced = (np.abs(diffs - diffs[0]) < tolerance).all()
        if not equally_spaced:
            # The latitudes are not equally-spaced, which suggests they might
            # be gaussian. Construct sample gaussian latitudes and check if
            # the two match.
            gauss_reference, wts = gaussian_lats_wts(nlat)
            difference = np.abs(latitudes - gaussian_reference)
            if (d > tolerance).any():
                raise ValueError('latitudes are unequally-spaced '
                                 'but are not gaussian')
            gridtype = 'gaussian'
        else:
            # The latitudes are equally-spaced. Construct reference global
            # equally spaced latitudes and check that the two match.
            if nlat % 2:
                # Odd number of latitudes includes the poles.
                equal_reference = np.linspace(90, -90, nlat)
            else:
                # Even number of latitudes doesn't include the poles.
                delta_latitude = 180. / nlat
                equal_reference = np.linspace(90 - 0.5 * delta_latitude,
                                              -90 + 0.5 * delta_latitude,
                                              nlat)
            difference = np.abs(latitudes - equal_reference)
            if (difference > tolerance).any():
                raise ValueError('equally-spaced latitudes are '
                                 'invalid (non-global?)')
            gridtype = 'regular'
        return gridtype

    def _get_apiorder_reorder(self, cube, latitude, longitude):
        """
        Create an ordering list to move latitude and longitude to the
        front of a cube's dimensions. Also compute the ordering list
        required to reverse this action.

        """
        # Remove the latitude and longitude dimensions from an initial list.
        apiorder = range(cube.ndim)
        apiorder.remove(latitude)
        apiorder.remove(longitude)
        # Insert latitude and longitude at the front.
        apiorder.insert(0, latitude)
        apiorder.insert(1, longitude)
        reorder = [apiorder.index(i) for i in range(cube.ndim)]
        return apiorder, reorder

    def _metadata(self, var, **attributes):
        """Re-shape outputs and add meta-data."""
        var = var.reshape(self._ishape)
        var = Cube(var,
                   dim_coords_and_dims=zip(self._coords, range(var.ndim)))
        var.transpose(self._reorder)
        for attribute, value in attributes.items():
            setattr(var, attribute, value)
        return var

    def u(self):
        """Zonal component of vector wind.

        **Example:**

            u = w.u()

        """
        u = self._api.u
        u = self._metadata(u,
                           standard_name='eastward_wind',
                           units='m s**-1',
                           long_name='eastward component of wind')
        return u

    def v(self):
        """Meridional component of vector wind.

        **Example:**

            v = w.v()

        """
        v = self._api.v
        v = self._metadata(v,
                           standard_name='northward_wind',
                           units='m s**-1',
                           long_name='northward component of wind')
        return v

    def magnitude(self):
        """Wind speed (magnitude of vector wind).

        **Example:**

            spd = w.magnitude()

        """
        m = self._api.magnitude()
        m = self._metadata(m,
                           standard_name='wind_speed',
                           units='m s**-1',
                           long_name='wind speed')
        return m

    def vrtdiv(self, truncation=None):
        """Relative vorticity and horizontal divergence.

        **Optional argument:**

        *truncation*
            Truncation limit (triangular truncation) for the spherical
            harmonic computation.

        **Examples:**

        Compute the relative vorticity and divergence:

            vrt, div = w.vrtdiv()

        Compute the relative vorticity and divergence and apply spectral
        truncation at triangular T13:

            vrtT13, divT13 = w.vrtdiv(truncation=13)

        """
        vrt, div = self._api.vrtdiv(truncation=truncation)
        vrt = self._metadata(vrt,
                             units='s**-1',
                             standard_name='atmosphere_relative_vorticity',
                             long_name='relative vorticity')
        div = self._metadata(div,
                             units='s**-1',
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

            vrt = w.vorticity()

        Compute the relative vorticity and apply spectral truncation at
        triangular T13:

            vrtT13 = w.vorticity(truncation=13)

        """
        vrt = self._api.vorticity(truncation=truncation)
        vrt = self._metadata(vrt,
                             units='s**-1',
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

            div = w.divergence()

        Compute the divergence and apply spectral truncation at
        triangular T13:

            divT13 = w.divergence(truncation=13)

        """
        div = self._api.divergence(truncation=truncation)
        div = self._metadata(div,
                             units='s**-1',
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

            pvrt = w.planetaryvorticity()

        Override the default value for Earth's angular velocity:

            pvrt = w.planetaryvorticity(omega=7.2921150)

        """
        f = self._api.planetaryvorticity(omega=omega)
        f = self._metadata(
            f,
            units='s**-1',
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

            avrt = w.absolutevorticity()

        Compute absolute vorticity and apply spectral truncation at
        triangular T13, also override the default value for Earth's
        angular velocity:

            avrt = w.absolutevorticity(omega=7.2921150, truncation=13)

        """
        avrt = self._api.absolutevorticity(omega=omega, truncation=truncation)
        avrt = self._metadata(avrt,
                              units='s**-1',
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

            sf, vp = w.sfvp()

        Compute streamfunction and velocity potential and apply spectral
        truncation at triangular T13:

            sfT13, vpT13 = w.sfvp(truncation=13)

        """
        sf, vp = self._api.sfvp(truncation=truncation)
        sf = self._metadata(
            sf,
            units='m**2 s**-1',
            standard_name='atmosphere_horizontal_streamfunction',
            long_name='streamfunction')
        vp = self._metadata(
            vp,
            units='m**2 s**-1',
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

            sf = w.streamfunction()

        Compute streamfunction and apply spectral truncation at
        triangular T13:

            sfT13 = w.streamfunction(truncation=13)

        """
        sf = self._api.streamfunction(truncation=truncation)
        sf = self._metadata(
            sf,
            units='m**2 s**-1',
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

            vp = w.velocity potential()

        Compute velocity potential and apply spectral truncation at
        triangular T13:

            vpT13 = w.velocity potential(truncation=13)

        """
        vp = self._api.velocitypotential(truncation=truncation)
        vp = self._metadata(
            vp,
            units='m**2 s**-1',
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

            uchi, vchi, upsi, vpsi = w.helmholtz()

        Compute the irrotational and non-divergent components of the
        vector wind and apply spectral truncation at triangular T13:

            uchiT13, vchiT13, upsiT13, vpsiT13 = w.helmholtz(truncation=13)

        """
        uchi, vchi, upsi, vpsi = self._api.helmholtz(truncation=truncation)
        uchi = self._metadata(uchi,
                              units='m s**-1',
                              long_name='irrotational_eastward_wind')
        vchi = self._metadata(vchi,
                              units='m s**-1',
                              long_name='irrotational_northward_wind')
        upsi = self._metadata(upsi,
                              units='m s**-1',
                              long_name='non_divergent_eastward_wind')
        vpsi = self._metadata(vpsi,
                              units='m s**-1',
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

            uchi, vchi = w.irrotationalcomponent()

        Compute the irrotational component of the vector wind and apply
        spectral truncation at triangular T13:

            uchiT13, vchiT13 = w.irrotationalcomponent(truncation=13)

        """
        uchi, vchi = self._api.irrotationalcomponent(truncation=truncation)
        uchi = self._metadata(uchi,
                              units='m s**-1',
                              long_name='irrotational_eastward_wind')
        vchi = self._metadata(vchi,
                              units='m s**-1',
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

            upsi, vpsi = w.nondivergentcomponent()

        Compute the non-divergent component of the vector wind and apply
        spectral truncation at triangular T13:

            upsiT13, vpsiT13 = w.nondivergentcomponent(truncation=13)

        """
        upsi, vpsi = self._api.nondivergentcomponent(truncation=truncation)
        upsi = self._metadata(upsi,
                              units='m s**-1',
                              long_name='non_divergent_eastward_wind')
        vpsi = self._metadata(vpsi,
                              units='m s**-1',
                              long_name='non_divergent_northward_wind')
        return upsi, vpsi

    def gradient(self, chi, truncation=None):
        """Computes the vector gradient of a scalar field on the sphere.

        Returns a 2-tuple of the zonal and meridional components of the
        vector gradient respectively.

        **Argument:**

        *chi*
            A scalar field. It must be an :py:class:`iris.cube.Cube`
            with the same latitude and longitude dimensions as the
            vector wind components that initialized the
            :py:class:`~windspharm.iris.VectorWind` instance.

        **Optional argument:**

        *truncation*
            Truncation limit (triangular truncation) for the spherical
            harmonic computation.

        **Examples:**

        Compute the vector gradient of absolute vorticity:

            avrt = w.absolutevorticity()
            avrt_zonal, avrt_meridional = w.gradient(avrt)

        Compute the vector gradient of absolute vorticity and apply
        spectral truncation at triangular T13:

            avrt = w.absolutevorticity()
            avrt_zonalT13, avrt_meridionalT13 = w.gradient(avrt, truncation=13)

        """
        if type(chi) is not Cube:
            raise TypeError('scalar field must be an iris cube')
        name = chi.name()
        lat, lat_dim = _dim_coord_and_dim(chi, 'latitude')
        lon, lon_dim = _dim_coord_and_dim(chi, 'longitude')
        apiorder, reorder = self._get_apiorder_reorder(chi, lat_dim, lon_dim)
        chi = chi.copy()
        chi.transpose(apiorder)
        ishape = chi.shape
        coords = chi.dim_coords
        chi = chi.data.reshape(chi.shape[:2] + (np.prod(chi.shape[2:]),))
        uchi, vchi = self._api.gradient(chi, truncation=truncation)
        uchi = uchi.reshape(ishape)
        vchi = vchi.reshape(ishape)
        uchi = Cube(uchi,
                    dim_coords_and_dims=zip(coords, range(uchi.ndim)))
        vchi = Cube(vchi,
                    dim_coords_and_dims=zip(coords, range(vchi.ndim)))
        uchi.transpose(reorder)
        vchi.transpose(reorder)
        uchi.long_name = 'zonal_gradient_of_{!s}'.format(name)
        vchi.long_name = 'meridional_gradient_of_{!s}'.format(name)
        return uchi, vchi


def _dim_coord_and_dim(cube, coord):
    """
    Retrieve a given dimension coordinate from an
    ::py:class:`iris.cube.Cube` and the dimension number it corresponds
    to.

    """
    coords = filter(lambda c: coord in c.name(), cube.dim_coords)
    if len(coords) > 1:
        raise ValueError('multiple {!s} coordinates not '
                         'allowed: {!r}'.format(coord, cube))
    try:
        c = coords[0]
    except IndexError:
        raise ValueError('cannot get {!s} coordinate '
                         'from cube {!r}'.format(coord, cube))
    c_dim = cube.coord_dims(c)
    if len(c_dim) != 1:
        raise ValueError('multiple dimensions with {!s} coordinate '
                         'not allowed: {!r}'.format(coord, cube))
    c_dim = c_dim[0]
    return c, c_dim
