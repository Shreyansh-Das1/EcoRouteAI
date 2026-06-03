import numpy as np
import rasterio
import os

with rasterio.open(r"Dataset\Processed Data\downsampledFused.tif") as src:
    fused_stack = src.read()

with rasterio.open(r"Dataset\Processed Data\Labels.tif") as src:
    labels = src.read(1)

optical_stack = fused_stack[2:]
sar_stack = fused_stack[:2]


# Normalize 
optical_norm = np.clip(optical_stack / 10000.0, 0, 1)

sar_db = 10 * np.log10(sar_stack + 1e-6)
sar_norm = np.zeros_like(sar_db)
for c in range(sar_db.shape[0]):
    mn, mx = sar_db[c].min(), sar_db[c].max()
    sar_norm[c] = (sar_db[c] - mn) / (mx - mn + 1e-8)

#Normalised Raster
fusednormed = np.concatenate((sar_norm, optical_norm), axis = 0)

#Adding padding
padding  = ((0,0),(110,110),(49,50))
paddedfused = np.pad(fusednormed, padding, mode = "reflect")
paddedlabel = np.pad(labels, ((110,110),(49,50)), mode="reflect")

label_map = {10:1, 20:2, 30:3, 40:4, 50:5, 60:6, 80: 7, 90:8}
labels_remapped = np.zeros_like(paddedlabel)
for orig, new in label_map.items():
    labels_remapped[paddedlabel == orig] = new

print("Label classes:", np.unique(labels_remapped))

z = input("press enter to continue")

# Tile 
os.makedirs(r"Dataset\Processed Data\Training\fusedTiles",     exist_ok=True)
os.makedirs(r"Dataset\Processed Data\Training\labelsTiles",  exist_ok=True)

TILE = 128
H, W = paddedfused.shape[1], paddedfused.shape[2]
tile_id = 1
for i in range(0, H - TILE + 1, TILE):
    for j in range(0, W - TILE + 1, TILE):
        name = f"{tile_id:04d}"
        np.save(rf"Dataset\Processed Data\Training\fusedTiles\{name}.npy", paddedfused[:, i:i+TILE, j:j+TILE])
        np.save(fr"Dataset\Processed Data\Training\labelsTiles\{name}.npy",labels_remapped[i:i+TILE, j:j+TILE])
        tile_id += 1

print(f"Tiles saved: {tile_id - 1}")