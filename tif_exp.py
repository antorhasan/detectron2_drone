<<<<<<< HEAD
import rasterio
from rasterio.transform import Affine
import numpy as np

with rasterio.open('./odm_orthophoto_original.tif') as dataset:
    driver = dataset.profile['driver']
    dtype = dataset.profile['dtype']
    nodata = dataset.profile['nodata']
    width = dataset.profile['width']
    height = dataset.profile['height']
    count = dataset.profile['count']
    crs = dataset.profile['crs']
    transform = dataset.profile['transform']
    blockxsize = dataset.profile['blockxsize']
    blockysize = dataset.profile['blockysize']
    tiled = dataset.profile['tiled']
    compress = dataset.profile['compress']
    interleave = dataset.profile['interleave']
    img = dataset.read()
    img = np.asarray(img)
    #print(dataset.profile['transform'])
print(transform)
print(img.shape)
prct = .5

geo_up_left = transform*(0,0)
geo_down_right = transform*(width, height)

res = (geo_down_right[0]-geo_up_left[0])*prct
new_up_left = geo_up_left[0]+((geo_down_right[0]-geo_up_left[0])*(.5/2))


print(geo_up_left,geo_down_right)
print(new_up_left)
print(asd)

dim_1_str = int((img.shape[1]*prct)/2)
dim_2_str = int((img.shape[2]*prct)/2)

img = img[:,dim_1_str:dim_1_str+int(img.shape[1]*prct),dim_2_str:dim_2_str+int(img.shape[2]*prct)]
print(img.shape)

with rasterio.open(
    'new.tif',
    'w',
    driver=driver,
    height=dim_1_str,
    width=dim_2_str,
    count=4,
    dtype=dtype,
    crs=crs,
    transform=transform,
    blockxsize=blockxsize,
    blockysize=blockysize,
    tiled=tiled,
    compress=compress,
    interleave=interleave,
    nodata=nodata
) as dst:
=======
import rasterio
from rasterio.transform import Affine
import numpy as np

with rasterio.open('./odm_orthophoto_original.tif') as dataset:
    driver = dataset.profile['driver']
    dtype = dataset.profile['dtype']
    nodata = dataset.profile['nodata']
    width = dataset.profile['width']
    height = dataset.profile['height']
    count = dataset.profile['count']
    crs = dataset.profile['crs']
    transform = dataset.profile['transform']
    blockxsize = dataset.profile['blockxsize']
    blockysize = dataset.profile['blockysize']
    tiled = dataset.profile['tiled']
    compress = dataset.profile['compress']
    interleave = dataset.profile['interleave']
    img = dataset.read()
    img = np.asarray(img)
    #print(dataset.profile['transform'])
print(transform)
print(img.shape)
prct = .5

geo_up_left = transform*(0,0)
geo_down_right = transform*(width, height)

res = (geo_down_right[0]-geo_up_left[0])*prct
new_up_left = geo_up_left[0]+((geo_down_right[0]-geo_up_left[0])*(.5/2))


print(geo_up_left,geo_down_right)
print(new_up_left)
print(asd)

dim_1_str = int((img.shape[1]*prct)/2)
dim_2_str = int((img.shape[2]*prct)/2)

img = img[:,dim_1_str:dim_1_str+int(img.shape[1]*prct),dim_2_str:dim_2_str+int(img.shape[2]*prct)]
print(img.shape)

with rasterio.open(
    'new.tif',
    'w',
    driver=driver,
    height=dim_1_str,
    width=dim_2_str,
    count=4,
    dtype=dtype,
    crs=crs,
    transform=transform,
    blockxsize=blockxsize,
    blockysize=blockysize,
    tiled=tiled,
    compress=compress,
    interleave=interleave,
    nodata=nodata
) as dst:
>>>>>>> f0615e03475350f291b5d0d75a8d95e5c3256f78
    dst.write(img)