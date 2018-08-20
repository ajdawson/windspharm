"""Common functionality shared across interfaces."""
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

import numpy as np
from spharm import gaussian_lats_wts


def get_apiorder(ndim, latitude_dim, longitude_dim):
    """
    Get the dimension ordering for a transpose to the required API
    dimension ordering.

    **Arguments:**

    *ndim*
        Total number of dimensions to consider.

    *latitude_dim*
        Index of the latitude dimension.

    *longitude_dim*
        Index of the longitude dimension.

    **Returns:**

    *apiorder*
        A list of indices corresponding to the order required to
        conform to the specified API order.

    *reorder*
        The inverse indices corresponding to *apiorder*.

    """
    apiorder = list(range(ndim))
    apiorder.remove(latitude_dim)
    apiorder.remove(longitude_dim)
    apiorder.insert(0, latitude_dim)
    apiorder.insert(1, longitude_dim)
    reorder = [apiorder.index(i) for i in range(ndim)]
    return apiorder, reorder


def inspect_gridtype(latitudes):
    """
    Determine a grid type by examining the points of a latitude
    dimension.

    Raises a ValueError if the grid type cannot be determined.

    **Argument:**

    *latitudes*
        An iterable of latitude point values.

    **Returns:**

    *gridtype*
        Either 'gaussian' for a Gaussian grid or 'regular' for an
        equally-spaced grid.

    """
    # Define a tolerance value for differences, this value must be much
    # smaller than expected grid spacings.
    tolerance = 5e-4
    # Get the number of latitude points in the dimension.
    nlat = len(latitudes)
    diffs = np.abs(np.diff(latitudes))
    equally_spaced = (np.abs(diffs - diffs[0]) < tolerance).all()
    if not equally_spaced:
        # The latitudes are not equally-spaced, which suggests they might
        # be gaussian. Construct sample gaussian latitudes and check if
        # the two match.
        gauss_reference, wts = gaussian_lats_wts(nlat)
        difference = np.abs(latitudes - gauss_reference)
        if (difference > tolerance).any():
            raise ValueError('latitudes are neither equally-spaced '
                             'or Gaussian')
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
            raise ValueError('equally-spaced latitudes are invalid '
                             '(they may be non-global)')
        gridtype = 'regular'
    return gridtype


def to3d(array):
    new_shape = array.shape[:2] + (np.prod(array.shape[2:], dtype=np.int),)
    return array.reshape(new_shape)
