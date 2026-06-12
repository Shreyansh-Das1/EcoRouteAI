#To normalise the fused stacks
import rasterio
import numpy as np

with rasterio.open(r"Dataset\Processed Data\2021\Fused\fusedSC.tif") as src:
    prof= src.profile
    fused = src.read()
    optical_stack = fused[2:]
    sar_stack = fused[:2]
    # Normalize 
optical_norm = np.clip(optical_stack / 10000.0, 0, 1)

sar_db = 10 * np.log10(sar_stack + 1e-6)
sar_norm = np.zeros_like(sar_db)
for c in range(sar_db.shape[0]):
    mn, mx = sar_db[c].min(), sar_db[c].max()
    sar_norm[c] = (sar_db[c] - mn) / (mx - mn + 1e-8)
    #Normalised Raster
fusednorm = np.concatenate((sar_norm, optical_norm), axis = 0)

with rasterio.open(r"Dataset\Processed Data\2021\fusedSCN.tif", "w", **prof) as dst:
    dst.write(fusednorm)