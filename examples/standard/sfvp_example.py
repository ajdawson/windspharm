"""
Compute streamfunction and velocity potential from the long-term-mean
flow.

This example uses the standard interface.

"""
import numpy as np
import matplotlib as mpl
mpl.rcParams['mathtext.default'] = 'regular'
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap, addcyclic
from netCDF4 import Dataset

from windspharm.standard import VectorWind
from windspharm.tools import prep_data, recover_data, order_latdim


# Read zonal and meridional wind components from file using the netCDF4
# module. The components are defined on pressure levels and are in separate
# files.
ncu = Dataset('../../example_data/uwnd_mean.nc', 'r')
uwnd = ncu.variables['uwnd'][:]
lons = ncu.variables['longitude'][:]
lats = ncu.variables['latitude'][:]
ncu.close()
ncv = Dataset('../../example_data/vwnd_mean.nc', 'r')
vwnd = ncv.variables['vwnd'][:]
ncv.close()

# The standard interface requires that latitude and longitude be the leading
# dimensions of the input wind components, and that wind components must be
# either 2D or 3D arrays. The data read in is 4D and has latitude and
# longitude as the last dimensions. The bundled tools can make the process of
# re-shaping the data a lot easier to manage.
uwnd, uwnd_info = prep_data(uwnd, 'tzyx')
vwnd, vwnd_info = prep_data(vwnd, 'tzyx')

# It is also required that the latitude dimension is north-to-south. Again the
# bundled tools make this easy.
lats, uwnd, vwnd = order_latdim(lats, uwnd, vwnd)

# Create a VectorWind instance to handle the computation of streamfunction and
# velocity potential.
w = VectorWind(uwnd, vwnd)

# Compute the streamfunction and velocity potential. Also use the bundled
# tools to re-shape the outputs to the 4D shape of the wind components as they
# were read off files.
sf, vp = w.sfvp()
sf = recover_data(sf, uwnd_info)
vp = recover_data(vp, uwnd_info)

# Pick out the field for December at 200 hPa and add a cyclic point (the
# cyclic point is for plotting purposes).
sf_200, lons_c = addcyclic(sf[11, 9], lons)
vp_200, lons_c = addcyclic(vp[11, 9], lons)

# Plot streamfunction.
m = Basemap(projection='cyl', resolution='c', llcrnrlon=0, llcrnrlat=-90,
        urcrnrlon=360.01, urcrnrlat=90)
x, y = m(*np.meshgrid(lons_c, lats))
clevs = [-120, -100, -80, -60, -40, -20, 0, 20, 40, 60, 80, 100, 120]
m.contourf(x, y, sf_200*1e-06, clevs, cmap=plt.cm.RdBu_r,
        extend='both')
m.drawcoastlines()
m.drawparallels((-90, -60, -30, 0, 30, 60, 90), labels=[1,0,0,0])
m.drawmeridians((0, 60, 120, 180, 240, 300, 360), labels=[0,0,0,1])
plt.colorbar(orientation='horizontal')
plt.title('Streamfunction ($10^6$m$^2$s$^{-1}$)', fontsize=16)

# Plot velocity potential.
plt.figure()
clevs = [-10, -8, -6, -4, -2, 0, 2, 4, 6, 8, 10]
m.contourf(x, y, vp_200*1e-06, clevs, cmap=plt.cm.RdBu_r,
        extend='both')
m.drawcoastlines()
m.drawparallels((-90, -60, -30, 0, 30, 60, 90), labels=[1,0,0,0])
m.drawmeridians((0, 60, 120, 180, 240, 300, 360), labels=[0,0,0,1])
plt.colorbar(orientation='horizontal')
plt.title('Velocity Potential ($10^6$m$^2$s$^{-1}$)', fontsize=16)
plt.show()

