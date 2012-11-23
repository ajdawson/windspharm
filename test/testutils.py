"""Utilities for constructing tests."""
import numpy as np
import numpy.ma as ma
try:
    import cdms2
    has_cdms = True
except ImportError:
    has_cdms = False
try:
    import iris
    has_iris = True
except ImportError:
    has_iris = False


def _read_test_data():
    """Read reference solutions from file."""
    exact = dict()
    for varid in ('psi', 'chi', 'vrt', 'div', 'uchi', 'vchi', 'upsi', 'vpsi',
            'chigradu', 'chigradv', 'uwnd', 'vwnd'):
        try:
            exact[varid] = np.load('data/{0:s}.ref.npy'.format(varid)).squeeze()
        except IOError:
            raise IOError('required data files not found')
    return exact


def generate_test_data(interface):
    """Generate reference solutions."""
    reference = _read_test_data()
    if interface.lower() in ('iris', 'cdms'):
        lons = np.arange(0, 360, 2.5)
        lats = np.linspace(90, -90, 73)
        if interface.lower() == 'cdms':
            lons = cdms2.createAxis(lons, id='longitude')
            lons.designateLongitude()
            lats = cdms2.createAxis(lats, id='latitude')
            lats.designateLatitude()
            for varid in reference.keys():
                v = cdms2.createVariable(reference[varid],
                                         axes=[lats,lons],
                                         id=varid)
                reference[varid] = v
        else:
            lons = iris.coords.DimCoord(lons,
                                        standard_name='longitude',
                                        units='degrees_east')
            lats = iris.coords.DimCoord(lats,
                                        standard_name='latitude',
                                        units='degrees_north')
            for varid in reference.keys():
                v = iris.cube.Cube(reference[varid],
                                   dim_coords_and_dims=zip((lats,lons),(0,1)),
                                   long_name=varid)
                reference[varid] = v
    return reference


def error(A1, A2):
    """Compute the error between two arrays.

    Computes RMSD normalized by the range of A2.

    """
    try:
        # get data from cdms2 variables
        A1 = A1.asma()
        A2 = A2.asma()
    except AttributeError:
        # might be iris cubes...
        try:
            A1type = type(A1.data)
            if A1type not in (np.ndarray, ma.core.MaskedArray):
                pass
            else:
                A1 = A1.data
        except AttributeError:
            pass
        try:
            A2type = type(A2.data)
            if A2type not in (np.ndarray, ma.core.MaskedArray):
                pass
            else:
                A2 = A2.data
        except AttributeError:
            pass
    return (np.sqrt((A1 - A2)**2).mean()) / (np.max(A2) - np.min(A2))


def identify(name):
    print '[{!s}] '.format(name)


if __name__ == '__main__':
    pass

