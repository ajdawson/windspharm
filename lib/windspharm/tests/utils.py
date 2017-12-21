"""Utilities for constructing tests."""
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

import numpy as np
try:
    from iris.cube import Cube
except ImportError:
    pass
try:
    import xarray as xr
except ImportError:
    try:
        import xray as xr
    except ImportError:
        pass


def __tomasked(*args):
    """Convert cdms2 variables or iris cubes to masked arrays.

    The conversion is safe, so if non-variables/cubes are passed they
    are just returned.

    """
    def __asma(a):
        try:
            if isinstance(a, Cube):
                # Retrieve the data from the cube.
                a = a.data
        except NameError:
            pass
        try:
            # Retrieve data from cdms variable.
            a = a.asma()
        except AttributeError:
            # The input is already an array or masked array, either extracted
            # from an iris cube, or was like that to begin with.
            pass
        try:
            if isinstance(a, xr.DataArray):
                a = a.values
        except NameError:
            pass
        return a
    return [__asma(a) for a in args]


def error(a, b):
    """Compute the error between two arrays.

    Computes RMSD normalized by the range of the second input.

    """
    a, b = __tomasked(a, b)
    return (np.sqrt((a - b)**2).mean()) / (np.max(b) - np.min(b))


if __name__ == '__main__':
    pass
