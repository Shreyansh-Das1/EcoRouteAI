import numpy as np
import rasterio
import numpy as np
import matplotlib.pyplot as plt

img = np.load("stitchedAOI.npy")

print(img.shape)

# Display first band
plt.figure(figsize=(10, 10))
plt.imshow(img[0], cmap="gray")
plt.colorbar()
plt.title("Band 1")
plt.show()
'''
with rasterio.open(r"Dataset\Processed Data\downsampledFused") as src:
    fused_stack = src.read()
print(fused_stack.shape)

with rasterio.open(r"Dataset\Processed Data\Labels.tif") as f:
    labels = f.read(1)

unique, counts = np.unique(labels, return_counts=True)
for cls, cnt in zip(unique, counts):
    pct = cnt / labels.size * 100
    print(f"Class {cls}: {cnt} pixels ({pct:.1f}%)")'''