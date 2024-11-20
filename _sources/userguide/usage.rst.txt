.. default-role:: py:obj

Basic usage
===========

This section describes the basic usage of the **VectorWind** objects in a generic way that is applicable to all interfaces.


Importing a **VectorWind** object
---------------------------------

The **VectorWind** objects are stored in interface specific modules: **windspharm.<interface>.VectorWind**. To import the standard interface::

    from windspharm.standard import VectorWind

the iris interface::

    from windspharm.iris import VectorWind

and the xarray interface::

    from windspharm.xarray import VectorWind


Creating a **VectorWind** object
--------------------------------

Creating a **VectorWind** object from eastward and northward wind components *u* and *v* can be as simple as::

    w = VectorWind(u, v)

In the case of the `windspharm.standard.VectorWind` interface there is a keyword argument *gridtype* which should be set to either *'regular'* for equally spaced grids or *'gaussian'* for Gaussian grids (the default is *'regular'*)::

    w = VectorWind(u, v, gridtype='gaussian')


Computing with **VectorWind**
-----------------------------

To perform a computation you call one of the methods of the **VectorWind** object.
For example, to compute the vorticity and divergence::

    vrt, div = w.vrtdiv()

All the computation methods take an optional *truncation* keyword argument which can be used to truncate the spectral coefficients before doing the computation.

It is also possible to compute gradients of scalar fields, which is useful for many applications. For example, to compute the gradients of absolute vorticity::

    absvrt = w.absolutevorticity()
    absvrt_u, absvrt_v = w.gradient(absvrt)

.. note::

   Some of the quantities can be computed separately or part of another computation e.g. **vorticity()** and **divergence()** or **vrtdiv()**. If you only want one of the results then you can call the single version, but if you want both the method that computes both at once will always be faster than calling both single versions.
