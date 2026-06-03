import rasterio
import numpy as np
import os 
bands = []
path = r"Dataset\Processed Data\2021\Opt"
for b in ["B02.tiff","B03.tiff","B04.tiff","B08.tiff"]:
    pth = os.path.join(path, b)
    with rasterio.open(pth) as src:
        bands.append(src.read(1))
        profile = src.profile

optical_stack = np.stack(bands)
print(optical_stack.shape)

profile.update(count=4)

with rasterio.open(r"Dataset\Processed Data\2021\Opt\optical_stack.tif","w",**profile) as dst:
    dst.write(optical_stack)