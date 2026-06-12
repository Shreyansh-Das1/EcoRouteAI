import rasterio
import numpy as np

#Adding Georeferencing to the stacks

with rasterio.open(r"Dataset\Fused Sentinel Data\raw\S2.SAFE\B02.jp2") as src:
    srcCrs = src.crs
    srcTrans = src.transform
    print("Extracted CRS and transform")

with rasterio.open(r"Dataset\Fused Sentinel Data\Stacked\optical_stack.tif","r+") as dst:
    dst.crs = srcCrs
    dst.transform = srcTrans
    print("Added CRS and Transform")