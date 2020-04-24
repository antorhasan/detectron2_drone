import numpy as np 
import pyproj
from rasterio.crs import CRS

crs = CRS.from_dict(init='epsg:32612')

in_proj = pyproj.Proj(init="epsg:{}".format(crs.to_epsg()))
out_proj = pyproj.Proj(init="epsg:4326")

lons, lats = pyproj.transform(in_proj, out_proj, 232201.6144207, 2628399.6197516)
lons = round(lons,6)
lats = round(lats,6)

print(180+lons,lats)