import numpy as np 
import pyproj
import rasterio
from rasterio.crs import CRS

with rasterio.open('./data/odm_orthophoto.tif') as map_layer:
    pixels2coords = map_layer.xy(0, 0)  #input px, py
    crs = map_layer.crs

x, y = pixels2coords

in_proj = pyproj.Proj(init="epsg:{}".format(crs.to_epsg()))
out_proj = pyproj.Proj(init="epsg:4326")

lons, lats = pyproj.transform(in_proj, out_proj, x, y)
lons = round(lons,6)
lats = round(lats,6)

print(lons, lats)