import rasterio
import numpy as np

#Fusing 2021 Data


with rasterio.open(r"Dataset\Processed Data\2021\Sar\VH.tiff") as src:
    vh = src.read(1)
    profile = src.profile

with rasterio.open(r"Dataset\Processed Data\2021\Sar\VV.tiff") as src:
    vv = src.read(1)

with rasterio.open(r"Dataset\Processed Data\2021\Opt\B2.tiff") as src:
    b = src.read(1)

with rasterio.open(r"Dataset\Processed Data\2021\Opt\B3.tiff") as src:
    g = src.read(1)

with rasterio.open(r"Dataset\Processed Data\2021\Opt\B4.tiff") as src:
    r = src.read(1)

with rasterio.open(r"Dataset\Processed Data\2021\Opt\B8.tiff") as src:
    nir = src.read(1)


fused_stack = np.stack([vv,vh,b,g,r,nir])

profile.update(count=6)

with rasterio.open(r"Dataset\Processed Data\2021\fused_stack.tif", "w", **profile) as dst:
    dst.write(fused_stack)