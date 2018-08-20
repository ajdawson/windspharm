"""Reference solutions for testing the `windspharm` package."""
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
import os

import numpy as np
from spharm import gaussian_lats_wts


def test_data_path():
    return os.path.join(os.path.abspath(os.path.dirname(__file__)), 'data')


def __read_reference_solutions(gridtype):
    """Read reference solutions from file."""
    exact = dict()
    for varid in ('psi', 'chi', 'vrt', 'div', 'uchi', 'vchi', 'upsi', 'vpsi',
                  'chigradu', 'chigradv', 'uwnd', 'vwnd', 'vrt_trunc'):
        try:
            filename = os.path.join(test_data_path(), gridtype,
                                    '{!s}.ref.npy'.format(varid))
            exact[varid] = np.load(filename).squeeze()
        except IOError:
            msg = 'required data file not found: {!s}'
            raise IOError(msg.format(filename))
    return exact


def _wrap_cdms(reference, lats, lons):
    try:
        import cdms2
    except ImportError:
        raise ValueError("cannot use container 'cdms' without cdms2")
    londim = cdms2.createAxis(lons, id='longitude')
    londim.designateLongitude()
    latdim = cdms2.createAxis(lats, id='latitude')
    latdim.designateLatitude()
    for name in reference.keys():
        reference[name] = cdms2.createVariable(reference[name],
                                               axes=[latdim, londim],
                                               id=name)


def _wrap_iris(reference, lats, lons):
    try:
        from iris.cube import Cube
        from iris.coords import DimCoord
    except ImportError:
        raise ValueError("cannot use container 'iris' without iris")

    londim = DimCoord(lons,
                      standard_name='longitude',
                      units='degrees_east')
    latdim = DimCoord(lats,
                      standard_name='latitude',
                      units='degrees_north')
    coords = list(zip((latdim, londim), (0, 1)))
    for name in reference.keys():
        reference[name] = Cube(reference[name],
                               dim_coords_and_dims=coords,
                               long_name=name)


def _wrap_xarray(reference, lats, lons):
    try:
        import xarray as xr
    except ImportError:
        try:
            import xray as xr
        except ImportError:
            raise ValueError("cannot use container 'xarray' without xarray")
    londim = xr.IndexVariable('longitude', lons,
                              attrs={'standard_name': 'longitude',
                                     'units': 'degrees_east'})
    latdim = xr.IndexVariable('latitude', lats,
                              attrs={'standard_name': 'latitude',
                                     'units': 'degrees_north'})
    for name in reference.keys():
        reference[name] = xr.DataArray(reference[name],
                                       coords=[latdim, londim],
                                       attrs={'long_name': name})


def _get_wrapper(container_type):
    if container_type == 'cdms':
        return _wrap_cdms
    elif container_type == 'iris':
        return _wrap_iris
    elif container_type == 'xarray':
        return _wrap_xarray
    else:
        raise ValueError('invalid container type: {!s}'.format(container_type))


def reference_solutions(container_type, gridtype):
    """Generate reference solutions in the required container."""
    container_type = container_type.lower()
    if container_type not in ('standard', 'iris', 'cdms', 'xarray'):
        raise ValueError("unknown container type: "
                         "'{!s}'".format(container_type))
    reference = __read_reference_solutions(gridtype)
    if container_type == 'standard':
        # Reference solution already in numpy arrays.
        return reference
    # Generate coordinate dimensions for meta-data interfaces.
    if gridtype == 'gaussian':
        lats, _ = gaussian_lats_wts(72)
    else:
        lats = np.linspace(90, -90, 73)
    lons = np.arange(0, 360, 2.5)
    _get_wrapper(container_type)(reference, lats, lons)
    return reference


if __name__ == '__main__':
    pass
