import numpy as np
import rasterio

with rasterio.open(r"Dataset\Processed Data\2021\fusedSCN.tif") as src:
    fused_stack = src.read()

with rasterio.open(r"Dataset\Processed Data\2021\Labels.tif") as src:
    labels = src.read(1)


#Adding padding
padding  = ((0,0),(110,110),(49,50))
paddedfused = np.pad(fused_stack, padding, mode = "reflect")
paddedlabel = np.pad(labels, ((110,110),(49,50)), mode="reflect")

label_map = {10:0, 20:1, 30:2, 40:3, 50:4, 60:5, 80: 6, 90:7}
labels_remapped = np.zeros_like(paddedlabel)
for orig, new in label_map.items():
    labels_remapped[paddedlabel == orig] = new

print("Label classes:", np.unique(labels_remapped))

z = input("press enter to continue")

TILE = 512
STRIDE = 128

H, W = paddedfused.shape[1], paddedfused.shape[2]
tile_id = 1

for i in range(0, H - TILE + 1, STRIDE):
    for j in range(0, W - TILE + 1, STRIDE):

        fused_tile = paddedfused[:, i:i+TILE, j:j+TILE]
        label_tile = labels_remapped[i:i+TILE, j:j+TILE]

        name = f"{tile_id:03d}"

        np.save(
            rf"Dataset\Processed Data\2021\Training\fusedTiles\{name}.npy",
            fused_tile
        )

        np.save(
            rf"Dataset\Processed Data\2021\Training\labelTiles\{name}.npy",
            label_tile
        )

        tile_id += 1

print(f"Generated {tile_id-1} tiles")

''' For 2026 Data
TILE = 128
H, W = paddedfused.shape[1], paddedfused.shape[2]
tile_id = 1
for i in range(0, H - TILE + 1, TILE):
    for j in range(0, W - TILE + 1, TILE):
        name = f"{tile_id:04d}"
        np.save(rf"Dataset\Processed Data\Training\fusedTiles\{name}.npy", paddedfused[:, i:i+TILE, j:j+TILE])
        np.save(fr"Dataset\Processed Data\Training\labelsTiles\{name}.npy",labels_remapped[i:i+TILE, j:j+TILE])
        tile_id += 1
'''
print(f"Tiles saved: {tile_id - 1}")