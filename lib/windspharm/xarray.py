"""Spherical harmonic vector wind computations (`xarray` interface)."""
# Copyright (c) 2016-2017 Andrew Dawson
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

try:
    import xarray as xr
except ImportError:
    import xray as xr

from . import standard
from ._common import get_apiorder, inspect_gridtype, to3d


class VectorWind(object):
    """Vector wind computations (`xarray` interface)."""

    def __init__(self, u, v, rsphere=6.3712e6):
        """Initialize a VectorWind instance.

        **Arguments:**

        *u*, *v*
            Zonal and meridional components of the vector wind
            respectively. Both components should be `~xarray.DataArray`
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

            from windspharm.xray import VectorWind
            w = VectorWind(u, v)

        """
        if not isinstance(u, xr.DataArray) or not isinstance(v, xr.DataArray):
            raise TypeError('u and v must be xarray.DataArray instances')
        # Check that the dimension coordinates have the same names and values.
        ucoords = [u.coords[name].values for name in u.dims]
        vcoords = [v.coords[name].values for name in v.dims]
        if (u.dims != v.dims):
            msg = 'u and v must have the same dimension coordinates'
            raise ValueError(msg)
        if not all([(uc == vc).all() for uc, vc in zip(ucoords, vcoords)]):
            msg = 'u and v must have the same dimension coordinate values'
            raise ValueError(msg)
        # Find the latitude and longitude coordinates and reverse the latitude
        # dimension if necessary.
        lat, lat_dim = _find_latitude_coordinate(u)
        lon, lon_dim = _find_longitude_coordinate(u)
        if lat.values[0] < lat.values[1]:
            u = _reverse(u, lat_dim)
            v = _reverse(v, lat_dim)
            lat, lat_dim = _find_latitude_coordinate(u)
        # Determine the gridtype of the input.
        gridtype = inspect_gridtype(lat.values)
        # Determine how the DataArrays should be reordered to conform to the
        # windspharm.standard API.
        apiorder, _ = get_apiorder(u.ndim, lat_dim, lon_dim)
        apiorder = [u.dims[i] for i in apiorder]
        self._reorder = u.dims
        u = u.copy().transpose(*apiorder)
        v = v.copy().transpose(*apiorder)
        # Reshape the raw data and input into the API.
        self._ishape = u.shape
        self._coords = [u.coords[name] for name in u.dims]
        u = to3d(u.values)
        v = to3d(v.values)
        self._api = standard.VectorWind(u, v, gridtype=gridtype,
                                        rsphere=rsphere)

    def _metadata(self, var, name, **attributes):
        var = var.reshape(self._ishape)
        var = xr.DataArray(var, coords=self._coords, name=name)
        var = var.transpose(*self._reorder)
        for attr, value in attributes.items():
            var.attrs[attr] = value
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
        u = self._metadata(self._api.u, 'u',
                           units='m s**-1',
                           standard_name='eastward_wind',
                           long_name='eastward_component_of_wind')
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
        v = self._metadata(self._api.v, 'v',
                           units='m s**-1',
                           standard_name='northward_wind',
                           long_name='northward_component_of_wind')
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
        m = self._metadata(m, 'speed',
                           units='m s**-1',
                           standard_name='wind_speed',
                           long_name='wind_speed')
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
        vrt = self._metadata(vrt, 'vorticity',
                             units='s**-1',
                             standard_name='atmosphere_relative_vorticity',
                             long_name='relative_vorticity')
        div = self._metadata(div, 'divergence',
                             units='s**-1',
                             standard_name='divergence_of_wind',
                             long_name='horizontal_divergence')
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
        vrt = self._metadata(vrt, 'vorticity',
                             units='s**-1',
                             standard_name='atmosphere_relative_vorticity',
                             long_name='relative_vorticity')
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
        div = self._metadata(div, 'divergence',
                             units='s**-1',
                             standard_name='divergence_of_wind',
                             long_name='horizontal_divergence')
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
            f, 'coriolis',
            units='s**-1',
            standard_name='coriolis_parameter',
            long_name='planetary_vorticity')
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
        avrt = self._metadata(avrt, 'absolute_vorticity',
                              units='s**-1',
                              standard_name='atmosphere_absolute_vorticity',
                              long_name='absolute_vorticity')
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
            sf, 'streamfunction',
            units='m**2 s**-1',
            standard_name='atmosphere_horizontal_streamfunction',
            long_name='streamfunction')
        vp = self._metadata(
            vp, 'velocity_potential',
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
            sf, 'streamfunction',
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
            vp, 'velocity_potential',
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
        uchi = self._metadata(uchi, 'u_chi',
                              units='m s**-1',
                              long_name='irrotational_eastward_wind')
        vchi = self._metadata(vchi, 'v_chi',
                              units='m s**-1',
                              long_name='irrotational_northward_wind')
        upsi = self._metadata(upsi, 'u_psi',
                              units='m s**-1',
                              long_name='non_divergent_eastward_wind')
        vpsi = self._metadata(vpsi, 'v_psi',
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
        uchi = self._metadata(uchi, 'u_chi',
                              units='m s**-1',
                              long_name='irrotational_eastward_wind')
        vchi = self._metadata(vchi, 'v_chi',
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
        upsi = self._metadata(upsi, 'u_psi',
                              units='m s**-1',
                              long_name='non_divergent_eastward_wind')
        vpsi = self._metadata(vpsi, 'v_psi',
                              units='m s**-1',
                              long_name='non_divergent_northward_wind')
        return upsi, vpsi

    def gradient(self, chi, truncation=None):
        """Computes the vector gradient of a scalar field on the sphere.

        **Argument:**

        *chi*
            A scalar field. It must be a `~xarray.DataArray` with the
            same latitude and longitude dimensions as the vector wind
            components that initialized the `VectorWind` instance.

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
        if not isinstance(chi, xr.DataArray):
            raise TypeError('scalar field must be an xarray.DataArray')
        name = chi.name
        lat, lat_dim = _find_latitude_coordinate(chi)
        lon, lon_dim = _find_longitude_coordinate(chi)
        if (lat.values[0] < lat.values[1]):
            # need to reverse latitude dimension
            chi = _reverse(chi, lat_dim)
            lat, lat_dim = _find_latitude_coordinate(chi)
        apiorder, _ = get_apiorder(chi.ndim, lat_dim, lon_dim)
        apiorder = [chi.dims[i] for i in apiorder]
        reorder = chi.dims
        chi = chi.copy().transpose(*apiorder)
        ishape = chi.shape
        coords = [chi.coords[n] for n in chi.dims]
        chi = to3d(chi.values)
        uchi, vchi = self._api.gradient(chi, truncation=truncation)
        uchi = uchi.reshape(ishape)
        vchi = vchi.reshape(ishape)
        uchi_name = 'zonal_gradient_of_{!s}'.format(name)
        vchi_name = 'meridional_gradient_of_{!s}'.format(name)
        uchi = xr.DataArray(uchi, coords=coords, name=uchi_name,
                            attrs={'long_name': uchi_name})
        vchi = xr.DataArray(vchi, coords=coords, name=vchi_name,
                            attrs={'long_name': vchi_name})
        uchi = uchi.transpose(*reorder)
        vchi = vchi.transpose(*reorder)
        return uchi, vchi

    def truncate(self, field, truncation=None):
        """Apply spectral truncation to a scalar field.

        This is useful to represent other fields in a way consistent
        with the output of other `VectorWind` methods.

        **Argument:**

        *field*
            A scalar field. It must be a `~xarray.DataArray` with the
            same latitude and longitude dimensions as the vector wind
            components that initialized the `VectorWind` instance.

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
        if not isinstance(field, xr.DataArray):
            raise TypeError('scalar field must be an xarray.Dataset')
        lat, lat_dim = _find_latitude_coordinate(field)
        lon, lon_dim = _find_longitude_coordinate(field)
        if (lat.values[0] < lat.values[1]):
            # need to reverse latitude dimension
            field = _reverse(field, lat_dim)
            lat, lat_dim = _find_latitude_coordinate(field)
        apiorder, _ = get_apiorder(field.ndim, lat_dim, lon_dim)
        apiorder = [field.dims[i] for i in apiorder]
        reorder = field.dims
        field = field.copy().transpose(*apiorder)
        ishape = field.shape
        fielddata = to3d(field.values)
        fieldtrunc = self._api.truncate(fielddata, truncation=truncation)
        field.values = fieldtrunc.reshape(ishape)
        field = field.transpose(*reorder)
        return field


def _reverse(array, dim):
    """Reverse an `xarray.DataArray` along a given dimension."""
    slicers = [slice(0, None)] * array.ndim
    slicers[dim] = slice(-1, None, -1)
    return array[tuple(slicers)]


def _find_coord_and_dim(array, predicate, name):
    """
    Find a dimension coordinate in an `xarray.DataArray` that satisfies
    a predicate function.

    """
    candidates = [coord
                  for coord in [array.coords[n] for n in array.dims]
                  if predicate(coord)]
    if not candidates:
        raise ValueError('cannot find a {!s} coordinate'.format(name))
    if len(candidates) > 1:
        msg = 'multiple {!s} coordinates are not allowed'
        raise ValueError(msg.format(name))
    coord = candidates[0]
    dim = array.dims.index(coord.name)
    return coord, dim


def _find_latitude_coordinate(array):
    """Find a latitude dimension coordinate in an `xarray.DataArray`."""
    return _find_coord_and_dim(
        array,
        lambda c: (c.name in ('latitude', 'lat') or
                   c.attrs.get('units') == 'degrees_north' or
                   c.attrs.get('axis') == 'Y'),
        'latitude')


def _find_longitude_coordinate(array):
    """Find a longitude dimension coordinate in an `xarray.DataArray`."""
    return _find_coord_and_dim(
        array,
        lambda c: (c.name in ('longitude', 'lon') or
                   c.attrs.get('units') == 'degrees_east' or
                   c.attrs.get('axis') == 'X'),
        'longitude')
