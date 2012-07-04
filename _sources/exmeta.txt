Metadata Interface Example
==========================

The following is a simple example of using the `metadata` interface of :py:mod:`windspharm` to compute the streamfunction and velocity potential associated with a global wind field.


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

Once the data is downloaded we'll read it using :py:mod:`cdms2`:

.. code-block:: python

   import cdms2

   ncin = cdms2.open(u_local, 'r')
   uwnd = ncin('uwnd')
   ncin.close()
   ncin = cdms2.open(v_local, 'r')
   vwnd = ncin('vwnd')
   ncin.close()

Unlike the `standard` interface, no further preparation of the data is required since the `metadata` interface has all it needs to prepare the data automatically.


Computing Streamfunction and Velocity Potential
-----------------------------------------------

The wind components can now be used to initialize a :py:class:`windspharm.metadata.VectorWind` instance. This can then be used to compute the streamfunction and velocity potential (amongst other things) from the input wind components:

.. code-block:: python

   from windspharm.metadata import VectorWind

   w = VectorWind(uwnd, vwnd)

   # Compute streamfunction and velocity potential.
   sf, vp = w.sfvp()


Plotting the Results
--------------------

We'll now use :py:mod:`matplotlib` along with the :py:mod:`mpl_toolkits.basemap` toolkit to plot streamfunction and velocity potential:

.. code-block:: python

   import matplotlib as mpl
   mpl.rcParams['mathtext.default'] = 'regular'
   import matplotlib.pyplot as plt
   from mpl_toolkits.basemap import Basemap

   # Pick the field for December at 200hPa and add a cyclic point.
   sf_d_200 = sf(time=slice(11,12), level=200, longitude=(0,360), squeeze=True)
   vp_d_200 = vp(time=slice(11,12), level=200, longitude=(0,360), squeeze=True)

   # Create a Basemap object to handle map projections and use it to
   # convert geophysical coordinates to map projection coordinates.
   m = Basemap(projection='cyl', resolution='c', llcrnrlon=0,
           llcrnrlat=-90, urcrnrlon=360.01, urcrnclat=90)
   lon, lat = sf_d_200.getLongitude()[:], sf_d_200.getLatitude()[:]
   x, y = m(*np.meshgrid(lon, lat))

   # Plot streamfunction.
   plt.figure()
   clevs = [-120, -100, -80, -60, -40, -20, 0, 20, 40, 60, 80, 100, 120]
   m.contourf(x, y, sf_d_200.asma()*1e-06, clevs, cmap=plt.cm.RdBu_r,
           extend='both')
   m.drawcoastlines()
   m.drawparallels((-90, -60, -30, 0, 30, 60, 90), labels=[1,0,0,0])
   m.drawmeridians((0, 60, 120, 180, 240, 300, 360), labels=[0,0,0,1])
   plt.colorbar(orientation='horizontal')
   plt.title('Streamfunction ($10^6$m$^2$s$^{-1}$)', fontsize=16)
   plt.savefig('example_standard_0.png')

   # Plot velocity potential.
   plt.figure()
   clevs = [-10, -8, -6, -4, -2, 0, 2, 4, 6, 8, 10]
   m.contourf(x, y, vp_d_200.asma()*1e-06, clevs, cmap=plt.cm.RdBu_r,
           extend='both')
   m.drawcoastlines()
   m.drawparallels((-90, -60, -30, 0, 30, 60, 90), labels=[1,0,0,0])
   m.drawmeridians((0, 60, 120, 180, 240, 300, 360), labels=[0,0,0,1])
   plt.colorbar(orientation='horizontal')
   plt.title('Velocity Potential ($10^6$m$^2$s$^{-1}$)', fontsize=16)
   
   plt.show()

This produces the following:

.. image:: example_metadata_0.png
   :scale: 75 %
   :alt: December-mean streamfunction at 200 hPa

.. image:: example_metadata_1.png
   :scale: 75 %
   :alt: December-mean velocity potential at 200 hPa

