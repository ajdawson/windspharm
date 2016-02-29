.. default-role:: py:obj

**windspharm** interfaces
=========================

`windspharm` uses different interfaces to work with different kinds of input data.
Descriptions of each interface are below, and are summarised in the following table:

.. tabularcolumns:: |L|L|

=========  ========================================
Interface  Description
=========  ========================================
iris       Data contained in an `iris` cube.
xarray     Data contained in an `xarray.DataArray`.
cdms       Data stored in a `cdms2` variable.
standard   Other data, stored in a `numpy.ndarray`.
=========  ========================================

Iris interface
--------------

The iris interface works with `~iris.cube.Cube` objects, which are the data containers used by the iris data analysis package.
The meta-data, including coordinate dimensions, associated with iris Cube objects is understood by the `windspharm.iris.VectorWind` interface.
The outputs of `windspharm.iris.VectorWind` methods are also contained in `~iris.cube.Cube` objects, meaning they can be used with tools in the iris package, and easily written to a file.

xarray interface
----------------

The xarray interface works with `~xarray.DataArray` objects.
The coordinate metadata of `~xarray.DataArray` is interpreted by the `windspharm.xarray.VectorWind` interface, and the outputs of the `windspharm.xarray.VectorWind` methods are contained in `~xarray.DataArray` objects allowing their use with othe tools from the `xarray` package.

cdms interface
--------------

The `windspharm.cdms.VectorWind` interface works with `cdms2` variables, which are the core data container used by UVCDAT_. A `cdms2` variable has meta-data associated with it, including dimensions, which are understood by the `windspharm.cdms.VectorWind` interface. The outputs of `windspharm.cdms.VectorWind` methods are `cdms2` variables with meta-data, which can be written straight to a netCDF file using `cdms2`, or used with other parts of the UVCDAT_ framework.

standard interface
------------------

The standard interface works with `numpy` arrays, which makes the standard interface the general purpose interface. Any data that can be stored in a `numpy.ndarray` can be analysed with the `windspharm.standard.VectorWind` interface.

.. _UVCDAT: http://uvcdat.llnl.gov
