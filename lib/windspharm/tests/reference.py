"""Reference solutions for testing the `windspharm` package."""
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
import os

import numpy as np
try:
    import cdms2
except ImportError:
    pass
try:
    from iris.cube import Cube
    from iris.coords import DimCoord
except ImportError:
    pass


def test_data_path():
    return os.path.join(os.path.abspath(os.path.dirname(__file__)), 'data')


def __read_reference_solutions():
    """Read reference solutions from file."""
    exact = dict()
    for varid in ('psi', 'chi', 'vrt', 'div', 'uchi', 'vchi', 'upsi', 'vpsi',
                  'chigradu', 'chigradv', 'uwnd', 'vwnd', 'vrt_trunc'):
        try:
            filename = os.path.join(test_data_path(),
                                    '{!s}.ref.npy'.format(varid))
            exact[varid] = np.load(filename).squeeze()
        except IOError:
            raise IOError('required data file not found')
    return exact


def reference_solutions(container_type, gridtype):
    """Generate reference solutions in the required container."""
    container_type = container_type.lower()
    if container_type not in ('standard', 'iris', 'cdms'):
        raise ValueError("unknown container type: "
                         "'{!s}'".format(container_type))
    reference = __read_reference_solutions()
    if container_type == 'standard':
        # Reference solution already in numpy arrays.
        return reference
    # Generate coordinate dimensions for meta-data interfaces.
    lons = np.arange(0, 360, 2.5)
    lats = np.linspace(90, -90, 73)
    if container_type == 'cdms':
        # Solution in cdms2 variables.
        try:
            londim = cdms2.createAxis(lons, id='longitude')
            londim.designateLongitude()
            latdim = cdms2.createAxis(lats, id='latitude')
            latdim.designateLatitude()
            for name in reference.keys():
                reference[name] = cdms2.createVariable(reference[name],
                                                       axes=[latdim, londim],
                                                       id=name)
        except NameError:
            raise ValueError("cannot use container 'cdms' without cdms2")
    elif container_type == 'iris':
        # Solution in iris cubes.
        try:
            londim = DimCoord(lons,
                              standard_name='longitude',
                              units='degrees_east')
            latdim = DimCoord(lats,
                              standard_name='latitude',
                              units='degrees_north')
            coords = zip((latdim, londim), (0, 1))
            for name in reference.keys():
                reference[name] = Cube(reference[name],
                                       dim_coords_and_dims=coords,
                                       long_name=name)
        except NameError:
            raise ValueError("cannot use container 'iris' without iris")
    return reference


if __name__ == '__main__':
    pass
