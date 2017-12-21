"""
Compute streamfunction and velocity potential from the long-term-mean
flow.

This example uses the cdms interface.

Additional requirements for this example:

* cdms2 (http://uvcdat.llnl.gov/)
* matplotlib (http://matplotlib.org/)
* cartopy (http://scitools.org.uk/cartopy/)

"""
import cartopy.crs as ccrs
import cdms2
import matplotlib as mpl
import matplotlib.pyplot as plt

from windspharm.cdms import VectorWind
from windspharm.examples import example_data_path

mpl.rcParams['mathtext.default'] = 'regular'


# Read zonal and meridional wind components from file using the cdms2 module
# from CDAT. The components are in separate files.
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

# Pick out the field for December and add a cyclic point (the cyclic point is
# for plotting purposes).
sf_dec = sf(time=slice(11, 12), longitude=(0, 360), squeeze=True)
vp_dec = vp(time=slice(11, 12), longitude=(0, 360), squeeze=True)

# Plot streamfunction.
ax1 = plt.axes(projection=ccrs.PlateCarree(central_longitude=180))
lons, lats = sf_dec.getLongitude()[:], sf_dec.getLatitude()[:]
clevs = [-120, -100, -80, -60, -40, -20, 0, 20, 40, 60, 80, 100, 120]
fill_sf = ax1.contourf(lons, lats, sf_dec.asma() * 1e-06, clevs,
                       transform=ccrs.PlateCarree(), cmap=plt.cm.RdBu_r,
                       extend='both')
ax1.coastlines()
ax1.gridlines()
plt.colorbar(fill_sf, orientation='horizontal')
plt.title('Streamfunction ($10^6$m$^2$s$^{-1}$)', fontsize=16)

# Plot velocity potential.
plt.figure()
ax2 = plt.axes(projection=ccrs.PlateCarree(central_longitude=180))
clevs = [-10, -8, -6, -4, -2, 0, 2, 4, 6, 8, 10]
fill_vp = ax2.contourf(lons, lats, vp_dec.asma() * 1e-06, clevs,
                       transform=ccrs.PlateCarree(), cmap=plt.cm.RdBu_r,
                       extend='both')
ax2.coastlines()
ax2.gridlines()
plt.colorbar(fill_vp, orientation='horizontal')
plt.title('Velocity Potential ($10^6$m$^2$s$^{-1}$)', fontsize=16)
plt.show()
