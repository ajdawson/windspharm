"""
Compute streamfunction and velocity potential from the long-term-mean
flow.

This example uses the metadata interface.

"""
import numpy as np
import matplotlib as mpl
mpl.rcParams['mathtext.default'] = 'regular'
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import cdms2

from windspharm.cdms import VectorWind
from windspharm.examples import example_data_path


# Read zonal and meridional wind components from file using the cdms2 module
# from CDAT. The components are defined on pressure levels and are in separate
# files.
ncu = cdms2.open(example_data_path('uwnd_mean.nc'), 'r')
uwnd = ncu('uwnd')
ncu.close()
ncv = cdms2.open(example_data_path('vwnd_mean.nc'), 'r')
vwnd = ncv('vwnd')
ncv.close()

# Create a VectorWind instance to handle the computation of streamfunction and
# velocity potential.
w = VectorWind(uwnd, vwnd)

# Compute the streamfunction and velocity potential.
sf, vp = w.sfvp()

# Pick out the field for December at 200 hPa and add a cyclic point (the
# cyclic point is for plotting purposes).
sf_200 = sf(time=slice(11,12), level=200, longitude=(0,360), squeeze=True)
vp_200 = vp(time=slice(11,12), level=200, longitude=(0,360), squeeze=True)

# Plot streamfunction.
m = Basemap(projection='cyl', resolution='c', llcrnrlon=0, llcrnrlat=-90,
        urcrnrlon=360.01, urcrnrlat=90)
lons, lats = sf_200.getLongitude()[:], sf_200.getLatitude()[:]
x, y = m(*np.meshgrid(lons, lats))
clevs = [-120, -100, -80, -60, -40, -20, 0, 20, 40, 60, 80, 100, 120]
m.contourf(x, y, sf_200.asma()*1e-06, clevs, cmap=plt.cm.RdBu_r,
        extend='both')
m.drawcoastlines()
m.drawparallels((-90, -60, -30, 0, 30, 60, 90), labels=[1,0,0,0])
m.drawmeridians((0, 60, 120, 180, 240, 300, 360), labels=[0,0,0,1])
plt.colorbar(orientation='horizontal')
plt.title('Streamfunction ($10^6$m$^2$s$^{-1}$)', fontsize=16)

# Plot velocity potential.
plt.figure()
clevs = [-10, -8, -6, -4, -2, 0, 2, 4, 6, 8, 10]
m.contourf(x, y, vp_200.asma()*1e-06, clevs, cmap=plt.cm.RdBu_r,
        extend='both')
m.drawcoastlines()
m.drawparallels((-90, -60, -30, 0, 30, 60, 90), labels=[1,0,0,0])
m.drawmeridians((0, 60, 120, 180, 240, 300, 360), labels=[0,0,0,1])
plt.colorbar(orientation='horizontal')
plt.title('Velocity Potential ($10^6$m$^2$s$^{-1}$)', fontsize=16)
plt.show()

