"""
Tools for managing data for use with `~windspharm.standard.VectorWind`
(or indeed `spharm.Spharmt`).

"""
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

import numpy as np


def __order_dims(d, inorder):
    if 'x' not in inorder or 'y' not in inorder:
        raise ValueError('a latitude-longitude grid is required')
    lonpos = inorder.lower().find('x')
    latpos = inorder.lower().find('y')
    d = np.rollaxis(d, lonpos)
    if latpos < lonpos:
        latpos += 1
    d = np.rollaxis(d, latpos)
    outorder = inorder.replace('x', '')
    outorder = outorder.replace('y', '')
    outorder = 'yx' + outorder
    return d, outorder


def __reshape(d):
    out = d.reshape(d.shape[:2] + (np.prod(d.shape[2:], dtype=np.int),))
    return out, d.shape


def prep_data(data, dimorder):
    """
    Prepare data for input to `~windspharm.standard.VectorWind` (or to
    `spharm.Spharmt` method calls).

    Returns a dictionary of intermediate information that can be passed
    to `recover_data` or `get_recovery` to recover the original shape
    and order of the data.

    **Arguments:**

    *data*
        Data array. The array must be at least 2D.

    *dimorder*
        String specifying the order of dimensions in the data array. The
        characters 'x' and 'y' represent longitude and latitude
        respectively. Any other characters can be used to represent
        other dimensions.

    **Returns:**

    *pdata*
        *data* reshaped/reordered to (latitude, longitude, other).

    *info*
        A dictionary of information required to recover *data*.

    **See also:**

    `recover_data`, `get_recovery`.

    **Examples:**

    Prepare an array with dimensions (12, 17, 73, 144) where the
    dimensions are (time, level, latitude, longitude)::

        pdata, info = prep_data(data, 'tzyx')

    Prepare an array with dimensions (144, 16, 73, 21) where the first
    dimension is longitude and the third dimension is latitude. The
    characters used to represent the other dimensions are arbitrary::

        pdata, info = prep_data(data, 'xayb')

    """
    # Returns the prepared data and some data info to help data recovery.
    pdata, intorder = __order_dims(data, dimorder)
    pdata, intshape = __reshape(pdata)
    info = dict(intermediate_shape=intshape,
                intermediate_order=intorder,
                original_order=dimorder)
    return pdata, info


def recover_data(pdata, info):
    """
    Recover the shape and dimension order of an array output from
    `~windspharm.standard.VectorWind` methods (or from `spharm.Spharmt`
    methods).

    This function performs the opposite of `prep_data`.

    For recovering the shape of multiple variables, see `get_recovery`.

    **Arguments:**

    *pdata*
        Data array with either 2 or 3 dimensions. The first two
        dimensions are latitude and longitude respectively.

    *info*
        Information dictionary output from `prep_data`.

    **Returns:**

    *data*
        The data reshaped/reordered.

    **See also:**

    `prep_data`, `get_recovery`.

    **Example:**

    Recover the original input shape and dimension order of an array
    processed with `prep_data` or an output of
    `~windspharm.standard.VectorWind` or `sparm.Spharmt` method calls on
    such data::

        data = recover_data(pdata, info)

    """
    # Convert to intermediate shape (full dimensionality, windspharm order).
    data = pdata.reshape(info['intermediate_shape'])
    # Re-order dimensions correctly.
    rolldims = np.array([info['intermediate_order'].index(dim)
                         for dim in info['original_order'][::-1]])
    for i in range(len(rolldims)):
        # Roll the axis to the front.
        data = np.rollaxis(data, rolldims[i])
        rolldims = np.where(rolldims < rolldims[i], rolldims + 1, rolldims)
    return data


__recover_docstring_template = """Shape/dimension recovery.

Recovers variable shape/dimension according to:

{!s}

Returns a `list` of variables.

"""


def get_recovery(info):
    """
    Return a function that can be used to recover the shape and
    dimension order of multiple arrays output from
    `~windspharm.standard.VectorWind` methods (or from `spharm.Spharmt`
    methods) according to a single dictionary of recovery information.

    **Argument:**

    *info*
        Information dictionary output from `prep_data`.

    **Returns:**

    *recover*
        A function used to recover arrays.

    **See also:**

    `recover_data`, `prep_data`.

    **Example:**

    Generate a function to recover the original input shape and
    dimension order of arrays processed with `prep_data` and outputs of
    `~windspharm.standard.VectorWind` method calls on this data::

        u, info = prep_data(u, 'tzyx')
        v, info = prep_data(v, 'tzyx')
        w = VectorWind(u, v)
        sf, vp = w.sfvp()
        recover = get_recovery(info)
        u, v, sf, vp = recover(u, v, sf, vp)

    """
    def __recover(*args):
        return [recover_data(arg, info) for arg in args]
    info_nice = ["'{!s}': {!s}".format(key, value)
                 for key, value in info.items()]
    __recover.__name__ = 'recover'
    __recover.__doc__ = __recover_docstring_template.format(
        '\n'.join(info_nice))
    return __recover


def reverse_latdim(u, v, axis=0):
    """
    Reverse the order of the latitude dimension of zonal and meridional
    wind components.

    **Arguments:**

    *u*, *v*
        Zonal and meridional wind components respectively.

    **Optional argument:**

    *axis*
        Index of the latitude dimension. This dimension will be reversed
        in the input arrays. Defaults to 0 (the first dimension).

    **Returns:**

    *ur*, *vr*
        Zonal and meridional wind components with the latitude dimensions
        reversed. These are always copies of the input.

    **See also:**

    `order_latdim`.

    **Examples:**

    Reverse the dimension corresponding to latitude when it is the first
    dimension of the inputs::

        u, v = reverse_latdim(u, v)

    Reverse the dimension corresponding to latitude when it is the third
    dimension of the inputs::

        u, v = reverse_latdim(u, v, axis=2)

    """
    slicelist = [slice(0, None)] * u.ndim
    slicelist[axis] = slice(None, None, -1)
    u = u.copy()[slicelist]
    v = v.copy()[slicelist]
    return u, v


def order_latdim(latdim, u, v, axis=0):
    """Ensure the latitude dimension is north-to-south.

    Returns copies of the latitude dimension and wind components
    with the latitude dimension going from north to south. If the
    latitude dimension is already in this order then the output will
    just be copies of the input.

    **Arguments:**

    *latdim*
        Array of latitude values.

    *u*, *v*
        Zonal and meridional wind components respectively.

    **Keyword argument:**

    *axis*
        Index of the latitude dimension in the zonal and meridional wind
        components. Defaults to 0 (the first dimension).

    **Returns:**

    *latdimr*
        Possibly reversed *latdim*, always a copy of *latdim*.

    *ur*, *vr*
        Possibly reversed *u* and *v* respectively. Always copies of *u*
        and *v* respectively.

    **See also:**

    `reverse_latdim`.

    **Examples:**

    Order the latitude dimension when latitude is the first dimension of
    the wind components::

        latdim, u, v = order_latdim(latdim, u, v)

    Order the latitude dimension when latitude is the third dimension of
    the wind components::

        latdim, u, v = order_latdim(latdim, u, v, axis=2)

    """
    latdim = latdim.copy()
    if latdim[0] < latdim[-1]:
        latdim = latdim[::-1]
        # reverse_latdim() will make copies of u and v
        u, v = reverse_latdim(u, v, axis=axis)
    else:
        # we return copies from this function
        u, v = u.copy(), v.copy()
    return latdim, u, v
