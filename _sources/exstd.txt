Standard Interface Example
==========================

The following is a simple example of using the `standard` interface of :py:mod:`windspharm` to compute the streamfunction and velocity potential associated with a global wind field.


Getting The Example Data
------------------------

This example uses the 1981-2010 monthly long-term means of zonal (eastward) and meridional (northward) wind. These data are freely available from the `NCEP/NCAR Reanalysis Project <http://www.esrl.noaa.gov/psd/data/gridded/data.ncep.reanalysis.html>`_. The following Python code can be used to download the data in NetCDF format:

.. code-block:: python

   import os
   import urllib2

   base_path = os.path.join('ftp://ftp.cdc.noaa.gov', 'Datasets',
            'ncep.reanalysis.derived', 'pressure')
   u_remote = os.path.join(base_path, 'uwnd.mon.1981-2010.ltm.nc')
   v_remote = os.path.join(base_path, 'vwnd.mon.1981-2010.ltm.nc')
   u_local = 'uwnd.mon.ltm.nc'
   v_local = 'vwnd.mon.ltm.nc'
   for local, remote in zip((u_local, v_local), (u_remote, v_remote)):
       ncremote = urllib2.urlopen(remote)
       nclocal = open(local, 'wb')
       nclocal.write(ncremote.read())
       nclocal.close()
       ncremote.close()


Reading and Preparing the Example Data
--------------------------------------

Once the data is downloaded we'll read it in Python using :py:mod:`netCDF4`:

.. code-block:: python

   from netCDF4 import Dataset

   ncin = Dataset(u_local)
   lon, lat = ncin.variables['lon'][:], ncin.variables['lat'][:]
   uwnd = ncin.variables['uwnd']
   ncin.close()
   ncin = Dataset(v_local)
   vwnd = ncin.variables['vwnd'][:]
   ncin.close()

In the standard interface it is required that latitude and longitude are the leading dimensions of our input wind components. A second requirement is that the input wind components must be 2D or 3D. Since the downloaded wind components are 4D and in the order (time, level, latitude, longitude) they must be reordered and reshaped to conform to the specifications. Tools from :py:mod:`numpy` are used to achieve this:

.. code-block:: python

   import numpy as np

   # Roll the longitude dimension to the front followed by the
   # latitude dimension. This results in arrays with dimensions
   # (latitude, longitude, time, level).
   ndim = uwnd.ndim
   uwnd = np.rollaxis(np.rollaxis(uwnd, ndim-1), ndim-1)
   vwnd = np.rollaxis(np.rollaxis(vwnd, ndim-1), ndim-1)
   
   # Combine the time and level dimensions by reshaping the arrays.
   shp = uwnd.shape
   uwnd = uwnd.reshape(shp[:2]+(np.prod(shp[2:]),))
   vwnd = vwnd.reshape(shp[:2]+(np.prod(shp[2:]),))

A final requirement is the latitude dimension must be ordered from north to south. The NCEP/NCAR data is already ordered in this way. It is probably best to check your input data though:

.. code-block:: python

   if lat[0] < lat[-1]:
       lat = lat[::-1]
       uwnd = uwnd[::-1]
       vwnd = vwnd[::-1]


Computing Streamfunction and Velocity Potential
-----------------------------------------------

The prepared wind components can now be used to initialize a :py:class:`windspharm.standard.VectorWind` instance. This can then be used to compute the streamfunction and velocity potential (amongst other things) from the input wind components:

.. code-block:: python

   from windspharm.standard import VectorWind

   # The NCEP/NCAR reanalysis is on an evenly-spaced (regular) grid.
   w = VectorWind(uwnd, vwnd, gridtype='regular')

   # Compute streamfunction and velocity potential.
   sf, vp = w.sfvp()

   # Reshape streamfunction and velocity potential so that time and
   # level are separate dimensions once again. They will have dimensions
   # of (latitude, longitude, time, level)
   sf = sf.reshape(shp)
   vp = vp.reshape(shp)

   # Pick the field for December at 200hPa and add a cyclic point.
   sf_d_200 = addcyclic(sf[..., 11, 9], lon)
   vp_d_200 = addcyclic(vp[..., 11, 9], lon)


Plotting the Results
--------------------

We'll now use :py:mod:`matplotlib` along with the :py:mod:`mpl_toolkits.basemap` toolkit to plot streamfunction and velocity potential:

.. code-block:: python

   import matplotlib as mpl
   mpl.rcParams['mathtext.default'] = 'regular'
   import matplotlib.pyplot as plt
   from mpl_toolkits.basemap import Basemap, addcyclic

   # Create a Basemap object to handle map projections and use it to
   # convert geophysical coordinates to map projection coordinates.
   m = Basemap(projection='cyl', resolution='c', llcrnrlon=0,
           llcrnrlat=-90, urcrnrlon=360.01, urcrnclat=90)
   x, y = m(*np.meshgrid(lon_c, lat))

   # Plot streamfunction.
   plt.figure()
   clevs = [-120, -100, -80, -60, -40, -20, 0, 20, 40, 60, 80, 100, 120]
   m.contourf(x, y, sf_d_200*1e-06, clevs, cmap=plt.cm.RdBu_r, extend='both')
   m.drawcoastlines()
   m.drawparallels((-90, -60, -30, 0, 30, 60, 90), labels=[1,0,0,0])
   m.drawmeridians((0, 60, 120, 180, 240, 300, 360), labels=[0,0,0,1])
   plt.colorbar(orientation='horizontal')
   plt.title('Streamfunction ($10^6$m$^2$s$^{-1}$)', fontsize=16)
   plt.savefig('example_standard_0.png')

   # Plot velocity potential.
   plt.figure()
   clevs = [-10, -8, -6, -4, -2, 0, 2, 4, 6, 8, 10]
   m.contourf(x, y, vp_d_200*1e-06, clevs, cmap=plt.cm.RdBu_r, extend='both')
   m.drawcoastlines()
   m.drawparallels((-90, -60, -30, 0, 30, 60, 90), labels=[1,0,0,0])
   m.drawmeridians((0, 60, 120, 180, 240, 300, 360), labels=[0,0,0,1])
   plt.colorbar(orientation='horizontal')
   plt.title('Velocity Potential ($10^6$m$^2$s$^{-1}$)', fontsize=16)
   
   plt.show()

This produces the following:

.. image:: example_standard_0.png
   :scale: 75 %
   :alt: December-mean streamfunction at 200 hPa

.. image:: example_standard_1.png
   :scale: 75 %
   :alt: December-mean velocity potential at 200 hPa

