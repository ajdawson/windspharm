Overview
========

`windspharm` is designed to simplify the computation of quantities that are composed of derivatives/integrals of a vector wind field defined on a sphere.
`windspharm` works by expressing the vector field in the form of spherical harmonics.
In the spherical harmonic basis many operations that are hard to compute in the spatial representation, such as the Laplacian operator, become trivial.
This allows one to compute such quantities both quickly and accurately.

The down-side of using a spherical harmonic representation is that the input and output fields must all be defined over the whole globe.
The spherical harmonic representation is simply not defined for non-global fields.


Computations with **windspharm**
--------------------------------

`windspharm` uses **VectorWind** objects to do computations.
A **VectorWind** object is an object that is initialized with the components of a global vector wind field (eastward and northward components), that provides many methods for returning quantities of interest.
The typical usage pattern for `windspharm` is:

1. Import the appropriate **VectorWind** object for the type of data being worked with.

2. Create a **VectorWind** instance using eastward and northward wind components.

3. Call methods of the **VectorWind** instance to compute and return quantities of interest.

The following table describes the methods that are common to the **VectorWind** objects in all interfaces:

.. tabularcolumns:: |L|L|

========================  ====================================================
Method                      Description
========================  ====================================================
 *magnitude*              Magnitude of the vector wind (the wind speed).

 *vrtdiv*                 Relative vorticity and divergence.

 *vorticity*              Relative vorticity.

 *divergence*             Divergence.

 *planetaryvorticity*     Planetary vorticity (Coriolis parameter).

 *absolutevorticity*      Absolute (planetary + relative) vorticity.

 *sfvp*                   Streamfunction and velocity potential.

 *streamfunction*         Streamfunction.

 *velocitypotential*      Velocity potential.

 *helmholtz*              Helmholtz decomposition, irrotational and
                          non-divergent components of the vector wind.

 *irrotationalcomponent*  Irrotational component of the vector wind (the
                          component associated with divergence/velocity
                          potential.

 *nondivergentcomponent*  Non-divergent component of the vector wind (the
                          component associated with vorticity/streamfunction).

 *gradient*               The vector components of the gradient of a scalar
                          field.
 *truncate*               Apply triangular truncation to a scalar field.
========================  ====================================================
