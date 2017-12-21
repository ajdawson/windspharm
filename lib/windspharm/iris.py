"""Spherical harmonic vector wind computations (`iris` interface)."""
# Copyright (c) 2012-2017 Andrew Dawson
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

from iris.cube import Cube
from iris.util import reverse

from . import standard
from ._common import get_apiorder, inspect_gridtype, to3d


class VectorWind(object):
    """Vector wind computations (`iris` interface)."""

    def __init__(self, u, v, rsphere=6.3712e6):
        """Initialize a VectorWind instance.

        **Arguments:**

        *u*, *v*
            Zonal and meridional components of the vector wind
            respectively. Both components should be `~iris.cube.Cube`
            instances. The components must have the same dimension
            coordinates and contain no missing values.

        **Optional argument:**

        *rsphere*
            The radius in metres of the sphere used in the spherical
            harmonic computations. Default is 6371200 m, the approximate
            mean spherical Earth radius.

        **Example:**

        Initialize a `VectorWind` instance with zonal and meridional
        components of the vector wind::

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
        # Reverse the latitude dimension if necessary.
        if (lat.points[0] < lat.points[1]):
            # need to reverse latitude dimension
            u = reverse(u, lat_dim)
            v = reverse(v, lat_dim)
            lat, lat_dim = _dim_coord_and_dim(u, 'latitude')
        # Determine the grid type of the input.
        gridtype = inspect_gridtype(lat.points)
        # Determine the ordering list (input to transpose) which will put the
        # latitude and longitude dimensions at the front of the cube's
        # dimensions, and the ordering list which will reverse this process.
        apiorder, self._reorder = get_apiorder(u.ndim, lat_dim, lon_dim)
        # Re-order the inputs (in-place, so we take a copy first) so latiutude
        # and longitude are at the front.
        u = u.copy()
        v = v.copy()
        u.transpose(apiorder)
        v.transpose(apiorder)
        # Records the current shape and dimension coordinates of the inputs.
        self._ishape = u.shape
        self._coords = u.dim_coords
        # Reshape the inputs so they are compatible with pyspharm.
        u = to3d(u.data)
        v = to3d(v.data)
        # Create a base VectorWind instance to do the computations.
        self._api = standard.VectorWind(u, v, gridtype=gridtype,
                                        rsphere=rsphere)

    def _metadata(self, var, **attributes):
        """Re-shape outputs and add meta-data."""
        var = var.reshape(self._ishape)
        var = Cube(
            var,
            dim_coords_and_dims=list(zip(self._coords, range(var.ndim))))
        var.transpose(self._reorder)
        for attribute, value in attributes.items():
            setattr(var, attribute, value)
        return var

    def u(self):
        """Zonal component of vector wind.

        **Returns:**

        *u*
            The zonal component of the wind.

        **Example:**

        Get the zonal component of the vector wind::

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

        **Returns:**

        *v*
            The meridional component of the wind.

        **Example:**

        Get the meridional component of the vector wind::

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

        **Returns:**

        *speed*
            The wind speed.

        **Example:**

        Get the magnitude of the vector wind::

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

        **Returns:**

        *vrt*, *div*
            The relative vorticity and divergence respectively.

        **See also:**

        `~VectorWind.vorticity`, `~VectorWind.divergence`.

        **Examples:**

        Compute the relative vorticity and divergence::

            vrt, div = w.vrtdiv()

        Compute the relative vorticity and divergence and apply spectral
        truncation at triangular T13::

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

        **Returns:**

        *vrt*
            The relative vorticity.

        **See also:**

        `~VectorWind.vrtdiv`, `~VectorWind.absolutevorticity`.

        **Examples:**

        Compute the relative vorticity::

            vrt = w.vorticity()

        Compute the relative vorticity and apply spectral truncation at
        triangular T13::

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

        **Returns:**

        *div*
            The divergence.

        **See also:**

        `~VectorWind.vrtdiv`.

        **Examples:**

        Compute the divergence::

            div = w.divergence()

        Compute the divergence and apply spectral truncation at
        triangular T13::

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

        **Returns:**

        *pvorticity*
            The planetary vorticity.

        **See also:**

        `~VectorWind.absolutevorticity`.

        **Example:**

        Compute planetary vorticity using default values::

            pvrt = w.planetaryvorticity()

        Override the default value for Earth's angular velocity::

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

        **Returns:**

        *avorticity*
            The absolute (relative + planetary) vorticity.

        **See also:**

        `~VectorWind.vorticity`, `~VectorWind.planetaryvorticity`.

        **Examples:**

        Compute absolute vorticity::

            avrt = w.absolutevorticity()

        Compute absolute vorticity and apply spectral truncation at
        triangular T13, also override the default value for Earth's
        angular velocity::

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

        **Returns:**

        *sf*, *vp*
            The streamfunction and velocity potential respectively.

        **See also:**

        `~VectorWind.streamfunction`, `~VectorWind.velocitypotential`.

        **Examples:**

        Compute streamfunction and velocity potential::

            sf, vp = w.sfvp()

        Compute streamfunction and velocity potential and apply spectral
        truncation at triangular T13::

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

        **Returns:**

        *sf*
            The streamfunction.

        **See also:**

        `~VectorWind.sfvp`.

        **Examples:**

        Compute streamfunction::

            sf = w.streamfunction()

        Compute streamfunction and apply spectral truncation at
        triangular T13::

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

        **Returns:**

        *vp*
            The velocity potential.

        **See also:**

        `~VectorWind.sfvp`.

        **Examples:**

        Compute velocity potential::

            vp = w.velocity potential()

        Compute velocity potential and apply spectral truncation at
        triangular T13::

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

        **Optional argument:**

        *truncation*
            Truncation limit (triangular truncation) for the spherical
            harmonic computation.

        **Returns:**

        *uchi*, *vchi*, *upsi*, *vpsi*
            Zonal and meridional components of irrotational and
            non-divergent wind components respectively.

        **See also:**

        `~VectorWind.irrotationalcomponent`,
        `~VectorWind.nondivergentcomponent`.

        **Examples:**

        Compute the irrotational and non-divergent components of the
        vector wind::

            uchi, vchi, upsi, vpsi = w.helmholtz()

        Compute the irrotational and non-divergent components of the
        vector wind and apply spectral truncation at triangular T13::

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

        .. note::

           If both the irrotational and non-divergent components are
           required then `~VectorWind.helmholtz` should be used instead.

        **Optional argument:**

        *truncation*
            Truncation limit (triangular truncation) for the spherical
            harmonic computation.

        **Returns:**

        *uchi*, *vchi*
            The zonal and meridional components of the irrotational wind
            respectively.

        **See also:**

        `~VectorWind.helmholtz`.

        **Examples:**

        Compute the irrotational component of the vector wind::

            uchi, vchi = w.irrotationalcomponent()

        Compute the irrotational component of the vector wind and apply
        spectral truncation at triangular T13::

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

        .. note::

           If both the non-divergent and irrotational components are
           required then `~VectorWind.helmholtz` should be used instead.

        **Optional argument:**

        *truncation*
            Truncation limit (triangular truncation) for the spherical
            harmonic computation.

        **Returns:**

        *upsi*, *vpsi*
            The zonal and meridional components of the non-divergent
            wind respectively.

        **See also:**

        `~VectorWind.helmholtz`.

        **Examples:**

        Compute the non-divergent component of the vector wind::

            upsi, vpsi = w.nondivergentcomponent()

        Compute the non-divergent component of the vector wind and apply
        spectral truncation at triangular T13::

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

        **Argument:**

        *chi*
            A scalar field. It must be a `~iris.cube.Cube`
            with the same latitude and longitude dimensions as the
            vector wind components that initialized the `VectorWind`
            instance.

        **Optional argument:**

        *truncation*
            Truncation limit (triangular truncation) for the spherical
            harmonic computation.

        **Returns:**

        *uchi*, *vchi*
            The zonal and meridional components of the vector gradient
            respectively.

        **Examples:**

        Compute the vector gradient of absolute vorticity::

            avrt = w.absolutevorticity()
            avrt_zonal, avrt_meridional = w.gradient(avrt)

        Compute the vector gradient of absolute vorticity and apply
        spectral truncation at triangular T13::

            avrt = w.absolutevorticity()
            avrt_zonalT13, avrt_meridionalT13 = w.gradient(avrt, truncation=13)

        """
        if type(chi) is not Cube:
            raise TypeError('scalar field must be an iris cube')
        name = chi.name()
        lat, lat_dim = _dim_coord_and_dim(chi, 'latitude')
        lon, lon_dim = _dim_coord_and_dim(chi, 'longitude')
        if (lat.points[0] < lat.points[1]):
            # need to reverse latitude dimension
            chi = reverse(chi, lat_dim)
            lat, lat_dim = _dim_coord_and_dim(chi, 'latitude')
        apiorder, reorder = get_apiorder(chi.ndim, lat_dim, lon_dim)
        chi = chi.copy()
        chi.transpose(apiorder)
        ishape = chi.shape
        coords = chi.dim_coords
        chi = to3d(chi.data)
        uchi, vchi = self._api.gradient(chi, truncation=truncation)
        uchi = uchi.reshape(ishape)
        vchi = vchi.reshape(ishape)
        uchi = Cube(
            uchi,
            dim_coords_and_dims=list(zip(coords, range(uchi.ndim))))
        vchi = Cube(
            vchi,
            dim_coords_and_dims=list(zip(coords, range(vchi.ndim))))
        uchi.transpose(reorder)
        vchi.transpose(reorder)
        uchi.long_name = 'zonal_gradient_of_{!s}'.format(name)
        vchi.long_name = 'meridional_gradient_of_{!s}'.format(name)
        return uchi, vchi

    def truncate(self, field, truncation=None):
        """Apply spectral truncation to a scalar field.

        This is useful to represent other fields in a way consistent
        with the output of other `VectorWind` methods.

        **Argument:**

        *field*
            A scalar field. It must be a `~iris.cube.Cube`
            with the same latitude and longitude dimensions as the
            vector wind components that initialized the `VectorWind`
            instance.

        **Optional argument:**

        *truncation*
            Truncation limit (triangular truncation) for the spherical
            harmonic computation. If not specified it will default to
            *nlats - 1* where *nlats* is the number of latitudes.

        **Returns:**

        *truncated_field*
            The field with spectral truncation applied.

        **Examples:**

        Truncate a scalar field to the computational resolution of the
        `VectorWind` instance::

            scalar_field_truncated = w.truncate(scalar_field)

        Truncate a scalar field to T21::

            scalar_field_T21 = w.truncate(scalar_field, truncation=21)

        """
        if type(field) is not Cube:
            raise TypeError('scalar field must be an iris cube')
        lat, lat_dim = _dim_coord_and_dim(field, 'latitude')
        lon, lon_dim = _dim_coord_and_dim(field, 'longitude')
        if (lat.points[0] < lat.points[1]):
            # need to reverse latitude dimension
            field = reverse(field, lat_dim)
            lat, lat_dim = _dim_coord_and_dim(field, 'latitude')
        apiorder, reorder = get_apiorder(field.ndim, lat_dim, lon_dim)
        field = field.copy()
        field.transpose(apiorder)
        ishape = field.shape
        fielddata = to3d(field.data)
        fieldtrunc = self._api.truncate(fielddata, truncation=truncation)
        field.data = fieldtrunc.reshape(ishape)
        field.transpose(reorder)
        return field


def _dim_coord_and_dim(cube, coord):
    """
    Retrieve a given dimension coordinate from a `~iris.cube.Cube` and
    the dimension number it corresponds to.

    """
    coords = [c for c in cube.dim_coords if coord in c.name()]
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
