"""Utilities for constructing tests."""
import numpy as np
try:
    import cdms2
except ImportError:
    pass


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
    if interface.lower() == 'metadata':
        # Create coordinate dimensions.
        lons = np.arange(0, 360, 2.5)
        lats = np.linspace(90, -90, 73)
        lons = cdms2.createAxis(lons, id='longitude')
        lons.designateLongitude()
        lats = cdms2.createAxis(lats, id='latitude')
        lats.designateLatitude()
        # Create variables.
        for varid in reference.keys():
            v = cdms2.createVariable(reference[varid], axes=[lats,lons],
                    id=varid)
            reference[varid] = v
    return reference


def error(A1, A2):
    """Compute the error between two arrays.

    Computes RMSD normalized by the range of A2.

    """
    try:
        A1 = A1.asma()
        A2 = A2.asma()
    except AttributeError:
        pass
    return (np.sqrt((A1 - A2)**2).mean()) / (np.max(A2) - np.min(A2))


def identify(name):
    print '[{0:s}] '.format(name)


if __name__ == '__main__':
    pass

