"""Compute Rossby wave source from the long-term mean flow.

This example uses the cdms interface.

"""
import cartopy.crs as ccrs
import cdms2
import matplotlib as mpl
mpl.rcParams['mathtext.default'] = 'regular'
import matplotlib.pyplot as plt
import numpy as np

from windspharm.cdms import VectorWind
from windspharm.examples import example_data_path


# Read zonal and meridional wind components from file using the cdms2 module
# from CDAT. The components are in separate files.
ncu = cdms2.open(example_data_path('uwnd_mean.nc'), 'r')
uwnd = ncu('uwnd')
ncu.close()
ncv = cdms2.open(example_data_path('vwnd_mean.nc'), 'r')
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
S = -eta * div - (uchi * etax + vchi * etay)

# Pick out the field for December and add a cyclic point (the cyclic point is
# for plotting purposes).
S_dec = S(time=slice(11, 12), longitude=(0, 360), squeeze=True)

# Plot Rossby wave source.
lons, lats = S_dec.getLongitude()[:], S_dec.getLatitude()[:]
ax = plt.axes(projection=ccrs.PlateCarree(central_longitude=180))
clevs = [-30, -25, -20, -15, -10, -5, 0, 5, 10, 15, 20, 25, 30]
fill = ax.contourf(lons, lats, S_dec.asma() * 1e11, clevs,
                   transform=ccrs.PlateCarree(), cmap=plt.cm.RdBu_r,
                   extend='both')
ax.coastlines()
ax.gridlines()
plt.colorbar(fill, orientation='horizontal')
plt.title('Rossby Wave Source ($10^{-11}$s$^{-1}$)', fontsize=16)
plt.show()
