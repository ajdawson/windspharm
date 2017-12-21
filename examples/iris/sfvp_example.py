"""
Compute streamfunction and velocity potential from the long-term-mean
flow.

This example uses the iris interface.

Additional requirements for this example:

* iris (http://scitools.org.uk/iris/)
* matplotlib (http://matplotlib.org/)
* cartopy (http://scitools.org.uk/cartopy/)

"""
import warnings

import cartopy.crs as ccrs
import iris
import iris.plot as iplt
from iris.coord_categorisation import add_month
import matplotlib as mpl
import matplotlib.pyplot as plt

from windspharm.iris import VectorWind
from windspharm.examples import example_data_path

mpl.rcParams['mathtext.default'] = 'regular'


# Read zonal and meridional wind components from file using the iris module.
# The components are in separate files. We catch warnings here because the
# files are not completely CF compliant.
with warnings.catch_warnings():
    warnings.simplefilter('ignore', UserWarning)
    uwnd = iris.load_cube(example_data_path('uwnd_mean.nc'))
    vwnd = iris.load_cube(example_data_path('vwnd_mean.nc'))
uwnd.coord('longitude').circular = True
vwnd.coord('longitude').circular = True

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
clevs = [-120, -100, -80, -60, -40, -20, 0, 20, 40, 60, 80, 100, 120]
ax = plt.subplot(111, projection=ccrs.PlateCarree(central_longitude=180))
fill_sf = iplt.contourf(sf_dec * 1e-06, clevs, cmap=plt.cm.RdBu_r,
                        extend='both')
ax.coastlines()
ax.gridlines()
plt.colorbar(fill_sf, orientation='horizontal')
plt.title('Streamfunction ($10^6$m$^2$s$^{-1}$)', fontsize=16)

# Plot velocity potential.
plt.figure()
clevs = [-10, -8, -6, -4, -2, 0, 2, 4, 6, 8, 10]
ax = plt.subplot(111, projection=ccrs.PlateCarree(central_longitude=180))
fill_vp = iplt.contourf(vp_dec * 1e-06, clevs, cmap=plt.cm.RdBu_r,
                        extend='both')
ax.coastlines()
ax.gridlines()
plt.colorbar(fill_vp, orientation='horizontal')
plt.title('Velocity Potential ($10^6$m$^2$s$^{-1}$)', fontsize=16)
plt.show()
