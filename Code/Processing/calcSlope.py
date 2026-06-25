import rasterio
import numpy as np


elevationPath = r"Dataset\DEM\DEM_32645.tif"
slopePath = r"Dataset\DEM\slope.tif"

#Calculating the slope

with rasterio.open(elevationPath) as src:
    data = src.read(1).astype('float32')
    res = src.res[0]
    profile = src.profile
    nodata = src.nodata
    x, y = np.gradient(data,res)
    slopeRad = np.arctan(np.sqrt(x**2 + y**2))
    slopeDeg = np.degrees(slopeRad)

    if nodata is not None:
        slopeDeg[data == nodata] = nodata

    profile.update(dtype='float32', compress='lzw')
    with rasterio.open(slopePath, 'w', **profile) as dst:
        dst.write(slopeDeg, 1)

with rasterio.open(slopePath) as src:
    print("Shape:", src.shape)
    print("Bounds: ", src.bounds)
    data=src.read(1)
    valid = data[data != src.nodata]
    print("Slope Range(Degrees): ", valid.min(), "/", valid.max())