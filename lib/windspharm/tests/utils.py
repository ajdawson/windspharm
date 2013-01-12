"""Utilities for constructing tests."""
from __future__ import absolute_import
import numpy as np
try:
    import cdms2
except ImportError:
    pass
try:
    from iris.cube import Cube
except ImportError:
    pass


def __tomasked(*args):
    """Convert cdms2 variables or iris cubes to masked arrays.

    The conversion is safe, so if non-variables/cubes are passed they
    are just returned.

    """
    def __asma(a):
        try:
            if type(a) is Cube:
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
