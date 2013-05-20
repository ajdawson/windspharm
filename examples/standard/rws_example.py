"""Compute Rossby wave source from the long-term mean flow.

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
from windspharm.examples import example_data_path


# Read zonal and meridional wind components from file using the cdms2 module
# from CDAT. The components are defined on pressure levels and are in separate
# files.
ncu = Dataset(example_data_path('uwnd_mean.nc'), 'r')
uwnd = ncu.variables['uwnd'][:]
lons = ncu.variables['longitude'][:]
lats = ncu.variables['latitude'][:]
ncu.close()
ncv = Dataset(example_data_path('vwnd_mean.nc'), 'r')
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

# Create a VectorWind instance to handle the computations.
w = VectorWind(uwnd, vwnd)

# Compute components of rossby wave source: absolute vorticity, divergence,
# irrotational (divergent) wind components, gradients of absolute vorticity.
eta = w.absolutevorticity()
div = w.divergence()
uchi, vchi = w.irrotationalcomponent()
etax, etay = w.gradient(eta)

# Combine the components to form the Rossby wave source term. Re-shape the
# Rossby wave source array to the 4D shape of the wind components as they were
# read off files.
S = -eta * div - uchi * etax + vchi * etay
S = recover_data(S, uwnd_info)

# Pick out the field for December at 200 hPa and add a cyclic point (the
# cyclic point is for plotting purposes).
S_200, lons_c = addcyclic(S[11, 9], lons)

# Plot Rossby wave source.
m = Basemap(projection='cyl', resolution='c', llcrnrlon=0, llcrnrlat=-90,
        urcrnrlon=360.01, urcrnrlat=90)
x, y = m(*np.meshgrid(lons_c, lats))
clevs = [-30, -25, -20, -15, -10, -5, 0, 5, 10, 15, 20, 25, 30]
m.contourf(x, y, S_200*1e11, clevs, cmap=plt.cm.RdBu_r,
        extend='both')
m.drawcoastlines()
m.drawparallels((-90, -60, -30, 0, 30, 60, 90), labels=[1,0,0,0])
m.drawmeridians((0, 60, 120, 180, 240, 300, 360), labels=[0,0,0,1])
plt.colorbar(orientation='horizontal')
plt.title('Rossby Wave Source ($10^{-11}$s$^{-1}$)', fontsize=16)
plt.show()

