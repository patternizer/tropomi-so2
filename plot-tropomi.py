import xarray as xr
from affine import Affine
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
from mpl_toolkits.axes_grid1 import make_axes_locatable
import matplotlib.ticker as mticker
from matplotlib.colors import LogNorm
import matplotlib.cm as cm
import cmocean
import rioxarray
from pyproj import Transformer

# SETTTINGS

crs = ccrs.PlateCarree()
fontsize = 12
iceland = [-26, -12, 62, 68]

# WEBCAM: "https://www.ruv.is/frett/2021/03/20/beint-vefstreymi-fra-eldstodvunum"
# TROPOMI SO2: "https://meeo-s5p.s3.amazonaws.com/index.html/dgnvS8QLPqo8TV9wQEBYRWd/KGaXspd7fAcwVwqb5a46zt8ajC3EGu/Lzih8BBpyiptv6KhFtpgbnthqN1xojbMNa81g1pkWpod7/AxWMXkSahEcwPLpQFPbfR2a7SD1PgM3E5F25c68mX7c4Ycs722Z3/FmBNgUfk77cmeoPrpr1zZKTwgwZYdCRdSb61i2ozfKdbZqLf2cFwsUZs/NtKnFFuLVYxUXRnvKPV1M73Ps5bC9vGDF3eUBxuBxbMz7VXen4n7NNeRn3Wm?t=items&ip=5"

orbitfile = r'S5P_NRTI_L2__SO2____20210320T151109_20210320T151609_17794_01_020104_20210320T155341_PRODUCT_qa_value_4326.tif'
ds = xr.open_rasterio(orbitfile)
transform = Affine.from_gdal(*ds.attrs['transform'])
timestamp = orbitfile[20:33]
rds = rioxarray.open_rasterio(orbitfile, masked=True, overview_level=0)
rds = rds.to_dataset('band')
rds = rds.rename({1: 'so2'})
#rds = rds.squeeze().drop("spatial_ref").drop("band")
#rds.name = "so2"
#df = rds.to_dataframe().reset_index()

transformer = Transformer.from_crs(rds.rio.crs, "epsg:4326", always_xy=True)
x_coords, y_coords = np.meshgrid( rds.coords[rds.rio.x_dim], rds.coords[rds.rio.y_dim] )
lon, lat = transformer.transform(x_coords, y_coords)

lat_min = 10*int(np.floor(lat.min()/10))
lat_max = 10*int(np.ceil(lat.max()/10))
lon_min = 10*int(np.floor(lon.min()/10))
lon_max = 10*int(np.ceil(lon.max()/10))

fig=plt.figure(figsize=(15, 10))
ax = plt.axes(projection=crs)
ax.coastlines(resolution='10m')
ax.set_title('S5P/TROPOMI L2 SO2: '+timestamp, fontsize=fontsize, pad=20.0, fontweight = 'bold')
img = ax.pcolormesh(rds.x, rds.y, rds.so2/100, cmap=plt.cm.magma, transform=crs)
cbar = fig.colorbar(img, ax=ax, orientation='horizontal', extend='neither', fraction=0.04, pad=0.1, shrink=0.5)
cbar.set_label(r'$SO_{2}$ (relative units)', fontsize=fontsize)
cbar.ax.tick_params(labelsize=fontsize)
gl = ax.gridlines(crs=crs, draw_labels=True, alpha=0.5)
xgrid = np.arange(lon_min, lon_max, 10)
ygrid = np.arange(lat_min, lat_max, 10)
gl.xlocator = mticker.FixedLocator(xgrid.tolist())
gl.ylocator = mticker.FixedLocator(ygrid.tolist())
gl.xformatter = LONGITUDE_FORMATTER
gl.yformatter = LATITUDE_FORMATTER
gl.xlabel_style = {'size': fontsize}
gl.ylabel_style = {'size': fontsize}
plt.savefig('tropomi-so2-rio.png')

# PLOT RASTER

import rasterio
from rasterio.plot import show
from rasterio.mask import mask
raster = rasterio.open(orbitfile)
NoData = raster.nodatavals == np.nan
bbox = raster.bounds
extent = [bbox[0],bbox[2],bbox[1],bbox[3]]

Z = raster.read(1)/255

fig=plt.figure(figsize=(15, 10))
ax = plt.axes(projection=crs)
ax.coastlines(resolution='10m')
ax.set_title('S5P/TROPOMI L2 SO2: '+timestamp, fontsize=fontsize, pad=20.0, fontweight = 'bold')
color = plt.cm.magma
#color.set_bad('lightgrey')
#img = plt.imshow(raster.read(1), cmap = color, extent = extent, norm=LogNorm(), transform=crs)
img = plt.imshow(Z, cmap = color, extent = extent, alpha=1.0, transform=crs)
cbar = fig.colorbar(img, ax=ax, orientation='horizontal', extend='neither', fraction=0.04, pad=0.1, shrink=0.5)
cbar.set_label(r'$SO_{2}$ (relative units)', fontsize=fontsize)
cbar.ax.tick_params(labelsize=fontsize)

ax.set_extent(iceland, crs=crs)    
gl = ax.gridlines(crs=crs, draw_labels=True, alpha=0.5)
xgrid = np.arange(iceland[0],iceland[1], 1)
ygrid = np.arange(iceland[2],iceland[3], 1)
gl.xlocator = mticker.FixedLocator(xgrid.tolist())
gl.ylocator = mticker.FixedLocator(ygrid.tolist())
gl.xformatter = LONGITUDE_FORMATTER
gl.yformatter = LATITUDE_FORMATTER
gl.xlines = True
gl.ylines = True
gl.xlabel_style = {'size': fontsize}
gl.ylabel_style = {'size': fontsize}
plt.savefig('tropomi-so2-rasterio.png')



