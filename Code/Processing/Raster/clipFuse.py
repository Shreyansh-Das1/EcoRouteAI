import rasterio
from rasterio.mask import mask
import numpy as np
from shapely.geometry import box
import geopandas as gpd

##Clip according to the aoi

aoi = gpd.read_file(r"Dataset\aoi_projected_EPSG32645.geojson")

with rasterio.open(r"Dataset\Fused Sentinel Data\Stacked\fused_stack.tif") as sample:
    clipped,transform = mask(sample, aoi.geometry, crop=True)
    meta = sample.meta.copy()



meta.update({
    "height": clipped.shape[1],
    "width": clipped.shape[2],
    "transform": transform
})
with rasterio.open("fusedAOI.tif", "w", **meta) as dst:
    dst.write(clipped)
