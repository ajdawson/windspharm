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

In the standard interface it is required that latitude and longitude are the leading dimensions of our input wind components. A second requirement is that the input wind components must be 2D or 3D. Since the downloaded wind components are 4D and in the order (time, level, latitude, longitude) they must be reordered and reshaped to conform to the specifications. This is most easily achieved using the tools contained in the :py:mod:`windspharm.tools` module:

.. code-block:: python

   from windspharm.tools import prep_data, order_latdim

   # Use the prep_data function to reorder dimensions and reshape to
   # 3D. We tell the function the order of the dimensions in the input.
   # The info outputs will be used later to process the streamfunction
   # and velocity potential fields.
   uwnd, uinfo = prep_data(uwnd, 'tzyx')
   vwnd, vinfo = prep_data(vwnd, 'tzyx')

   # Ensure that the latitude dimension is north-to-south. The
   # order_latdim function checks this and reverses the order if
   # necessary.
   lat, uwnd, vwnd = order_latdim(lat, uwnd, vwnd)


Computing Streamfunction and Velocity Potential
-----------------------------------------------

The prepared wind components can now be used to initialize a :py:class:`windspharm.standard.VectorWind` instance. This can then be used to compute the streamfunction and velocity potential (amongst other things) from the input wind components:

.. code-block:: python

   from windspharm.standard import VectorWind
   from windspharm.tools import recover_data

   # The NCEP/NCAR reanalysis is on an evenly-spaced (regular) grid.
   w = VectorWind(uwnd, vwnd, gridtype='regular')

   # Compute streamfunction and velocity potential.
   sf, vp = w.sfvp()

   # Use the recover_data function to reshape/reorder the outputs.
   # They will then have the dimensionality of the original inputs
   # (time, level, latitude, longitude).
   sf = recover_data(sf, uinfo)
   vp = recover_data(vp, uinfo)


Plotting the Results
--------------------

We'll now use :py:mod:`matplotlib` along with the :py:mod:`mpl_toolkits.basemap` toolkit to plot streamfunction and velocity potential for December at 200 hPa:

.. code-block:: python

   import numpy as np
   import matplotlib as mpl
   mpl.rcParams['mathtext.default'] = 'regular'
   import matplotlib.pyplot as plt
   from mpl_toolkits.basemap import Basemap, addcyclic

   # Pick the field for December at 200hPa and add a cyclic point.
   # The cyclic point is added only for plotting purposes.
   sf_d_200, lon_c = addcyclic(sf[11, 9], lon)
   vp_d_200, lon_c = addcyclic(vp[11, 9], lon)

   # Create a Basemap object to handle map projections and use it to
   # convert geophysical coordinates to map projection coordinates.
   m = Basemap(projection='cyl', resolution='c', llcrnrlon=0,
           llcrnrlat=-90, urcrnrlon=360.01, urcrnrlat=90)
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

