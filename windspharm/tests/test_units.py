"""Test the unit handling of the iris and xarray interfaces."""

import numpy as np
import pytest

try:
    import iris.coords
    import iris.cube

    import windspharm.iris
except ImportError:
    iris = None

try:
    import xarray as xr

    import windspharm.xarray
except ImportError:
    xr = None


def create_data(package: str, wind_units: str):
    """Create data for use by test functions."""
    data = np.zeros((7, 12), dtype="f4")
    lats = np.arange(-90, 91, 30, dtype="f4")
    lons = np.arange(0, 360, 30, dtype="f4")
    if package == "iris":
        result = iris.cube.Cube(
            data,
            units=wind_units,
            dim_coords_and_dims=(
                (iris.coords.DimCoord(lats, "latitude", units="degrees_north"), 0),
                (
                    iris.coords.DimCoord(
                        lons, "longitude", units="degrees_east", circular=True
                    ),
                    1,
                ),
            ),
        )
    elif package == "xarray":
        result = xr.DataArray(
            data,
            dims=("latitude", "longitude"),
            coords={
                "latitude": (("latitude",), lats, {"units": "degrees_north"}),
                "longitude": (("longitude",), lons, {"units": "degrees_easth"}),
            },
            attrs={"units": wind_units},
        )
    return result


@pytest.mark.skipif("iris is None")
@pytest.mark.parametrize("units", ["knots", "miles per hour"])
def test_iris_convert_units(units):
    """Test that iris will convert speed units to m/s."""
    cube = create_data("iris", units)
    vec_wind = windspharm.iris.VectorWind(cube, cube)
    assert np.any(vec_wind.u() != cube)
    assert np.any(vec_wind.v() != cube)


@pytest.mark.skipif("xr is None")
@pytest.mark.parametrize("units", ["knots", "mph"])
def test_xr_warns_units(units):
    """Test that XArray warns for non-m/s wind units."""
    data = create_data("xarray", units)
    with pytest.warns(UserWarning):
        vec_wind = windspharm.xarray.VectorWind(data, data)


@pytest.mark.skipif("xr is None")
@pytest.mark.parametrize("units", ["m/s", "m / s", "m s**-1", "m s^-1", "m s ** -1"])
@pytest.mark.filterwarnings("error:Winds should have units of m/s")
def test_xr_unit_recognition(units):
    """Test that XArray doesn't warn for different spellings of m/s."""
    data = create_data("xarray", units)
    vec_wind = windspharm.xarray.VectorWind(data, data)


@pytest.mark.parametrize(
    "package",
    [
        pytest.param("iris", marks=pytest.mark.skipif("iris is None")),
        pytest.param("xarray", marks=pytest.mark.skipif("xr is None")),
    ],
)
@pytest.mark.parametrize("units", ["K", "mg/kg"])
def test_gradient_units(package, units):
    """Test the units of the gradient.

    They should be the units of the input per meter.
    """
    scalar_data = create_data(package, units)
    wind_data = create_data(package, "m/s")
    vec_wind = getattr(windspharm, package).VectorWind(wind_data, wind_data)
    grad_components = vec_wind.gradient(scalar_data)
    for component in grad_components:
        if package == "iris":
            new_units = component.units
        else:
            new_units = component.attrs["units"]
        assert new_units != units
        assert new_units == "{:s} / m".format(units)
