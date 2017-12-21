"""Compute Rossby wave source from the long-term mean flow.

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
S = eta * -1. * div - (uchi * etax + vchi * etay)
S.coord('longitude').attributes['circular'] = True

# Pick out the field for December at 200 hPa.
time_constraint = iris.Constraint(month='Dec')
add_month(S, 'time')
S_dec = S.extract(time_constraint)

# Plot Rossby wave source.
clevs = [-30, -25, -20, -15, -10, -5, 0, 5, 10, 15, 20, 25, 30]
ax = plt.subplot(111, projection=ccrs.PlateCarree(central_longitude=180))
fill = iplt.contourf(S_dec * 1e11, clevs, cmap=plt.cm.RdBu_r, extend='both')
ax.coastlines()
ax.gridlines()
plt.colorbar(fill, orientation='horizontal')
plt.title('Rossby Wave Source ($10^{-11}$s$^{-1}$)', fontsize=16)
plt.show()
