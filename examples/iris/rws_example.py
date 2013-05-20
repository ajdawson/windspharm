"""Compute Rossby wave source from the long-term mean flow.

This example uses the iris interface.

"""
import warnings

import numpy as np
import matplotlib as mpl
mpl.rcParams['mathtext.default'] = 'regular'
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap, addcyclic
import iris
from iris.coord_categorisation import add_month

from windspharm.iris import VectorWind
from windspharm.examples import example_data_path


# Read zonal and meridional wind components from file using the iris module.
# The components are in separate files. We catch warnings here because the
# files are not completely CF compliant.
with warnings.catch_warnings():
    warnings.simplefilter('ignore', UserWarning)
    uwnd = iris.load_cube(example_data_path('uwnd_mean.nc'))
    vwnd = iris.load_cube(example_data_path('vwnd_mean.nc'))

# Create a VectorWind instance to handle the computations.
w = VectorWind(uwnd, vwnd)

# Compute components of rossby wave source: absolute vorticity, divergence,
# irrotational (divergent) wind components, gradients of absolute vorticity.
eta = w.absolutevorticity()
div = w.divergence()
uchi, vchi = w.irrotationalcomponent()
etax, etay = w.gradient(eta)
etax.units = 'm**-1 s**-1'
etay.units = 'm**-1 s**-1'

# Combine the components to form the Rossby wave source term.
S = eta * -1. * div - uchi * etax + vchi * etay

# Pick out the field for December at 200 hPa.
time_constraint = iris.Constraint(month='Dec')
add_month(S, 'time')
S_dec = S.extract(time_constraint)

# Plot Rossby wave source.
m = Basemap(projection='cyl', resolution='c', llcrnrlon=0, llcrnrlat=-90,
            urcrnrlon=360.01, urcrnrlat=90)
lons, lats = S_dec.coord('longitude'), S_dec.coord('latitude')
S_dec, lonsc = addcyclic(S_dec.data, lons.points)
x, y = m(*np.meshgrid(lonsc, lats.points))
clevs = [-30, -25, -20, -15, -10, -5, 0, 5, 10, 15, 20, 25, 30]
m.contourf(x, y, S_dec*1e11, clevs, cmap=plt.cm.RdBu_r, extend='both')
m.drawcoastlines()
m.drawparallels((-90, -60, -30, 0, 30, 60, 90), labels=[1,0,0,0])
m.drawmeridians((0, 60, 120, 180, 240, 300, 360), labels=[0,0,0,1])
plt.colorbar(orientation='horizontal')
plt.title('Rossby Wave Source ($10^{-11}$s$^{-1}$)', fontsize=16)
plt.show()

