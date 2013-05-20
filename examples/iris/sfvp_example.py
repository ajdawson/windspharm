"""
Compute streamfunction and velocity potential from the long-term-mean
flow.

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

# Create a VectorWind instance to handle the computation of streamfunction and
# velocity potential.
w = VectorWind(uwnd, vwnd)

# Compute the streamfunction and velocity potential.
sf, vp = w.sfvp()

# Pick out the field for December.
time_constraint = iris.Constraint(month='Dec')
add_month(sf, 'time', name='month')
add_month(vp, 'time', name='month')
sf_dec = sf.extract(time_constraint)
vp_dec = vp.extract(time_constraint)

# Plot streamfunction.
m = Basemap(projection='cyl', resolution='c', llcrnrlon=0, llcrnrlat=-90,
            urcrnrlon=360.01, urcrnrlat=90)
lons, lats = sf_dec.coord('longitude'), sf_dec.coord('latitude')
sf_dec, lonsc = addcyclic(sf_dec.data, lons.points)
vp_dec, lonsc = addcyclic(vp_dec.data, lons.points)
x, y = m(*np.meshgrid(lonsc, lats.points))

clevs = [-120, -100, -80, -60, -40, -20, 0, 20, 40, 60, 80, 100, 120]
m.contourf(x, y, sf_dec*1e-06, clevs, cmap=plt.cm.RdBu_r, extend='both')
m.drawcoastlines()
m.drawparallels((-90, -60, -30, 0, 30, 60, 90), labels=[1,0,0,0])
m.drawmeridians((0, 60, 120, 180, 240, 300, 360), labels=[0,0,0,1])
plt.colorbar(orientation='horizontal')
plt.title('Streamfunction ($10^6$m$^2$s$^{-1}$)', fontsize=16)

# Plot velocity potential.
plt.figure()
clevs = [-10, -8, -6, -4, -2, 0, 2, 4, 6, 8, 10]
m.contourf(x, y, vp_dec*1e-06, clevs, cmap=plt.cm.RdBu_r, extend='both')
m.drawcoastlines()
m.drawparallels((-90, -60, -30, 0, 30, 60, 90), labels=[1,0,0,0])
m.drawmeridians((0, 60, 120, 180, 240, 300, 360), labels=[0,0,0,1])
plt.colorbar(orientation='horizontal')
plt.title('Velocity Potential ($10^6$m$^2$s$^{-1}$)', fontsize=16)
plt.show()
