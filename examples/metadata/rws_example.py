"""Compute Rossby wave source from the long-term mean flow.

This example uses the metadata interface.

"""
import numpy as np
import matplotlib as mpl
mpl.rcParams['mathtext.default'] = 'regular'
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import cdms2

from windspharm.metadata import VectorWind


# Read zonal and meridional wind components from file using the cdms2 module
# from CDAT. The components are defined on pressure levels and are in separate
# files.
ncu = cdms2.open('../../example_data/uwnd_mean.nc', 'r')
uwnd = ncu('uwnd')
ncu.close()
ncv = cdms2.open('../../example_data/vwnd_mean.nc', 'r')
vwnd = ncv('vwnd')
ncv.close()

# Create a VectorWind instance to handle the computations.
w = VectorWind(uwnd, vwnd)

# Compute components of rossby wave source: absolute vorticity, divergence,
# irrotational (divergent) wind components, gradients of absolute vorticity.
eta = w.absolutevorticity()
div = w.divergence()
uchi, vchi = w.irrotationalcomponent()
etax, etay = w.gradient(eta)

# Combine the components to form the Rossby wave source term.
S = -eta * div - uchi * etax + vchi * etay

# Pick out the field for December at 200 hPa and add a cyclic point (the
# cyclic point is for plotting purposes).
S_200 = S(time=slice(11,12), level=200, longitude=(0,360), squeeze=True)

# Plot Rossby wave source.
m = Basemap(projection='cyl', resolution='c', llcrnrlon=0, llcrnrlat=-90,
        urcrnrlon=360.01, urcrnrlat=90)
lons, lats = S_200.getLongitude()[:], S_200.getLatitude()[:]
x, y = m(*np.meshgrid(lons, lats))
clevs = [-30, -25, -20, -15, -10, -5, 0, 5, 10, 15, 20, 25, 30]
m.contourf(x, y, S_200.asma()*1e11, clevs, cmap=plt.cm.RdBu_r,
        extend='both')
m.drawcoastlines()
m.drawparallels((-90, -60, -30, 0, 30, 60, 90), labels=[1,0,0,0])
m.drawmeridians((0, 60, 120, 180, 240, 300, 360), labels=[0,0,0,1])
plt.colorbar(orientation='horizontal')
plt.title('Rossby Wave Source ($10^{-11}$s$^{-1}$)', fontsize=16)
plt.show()

