import rasterio
import numpy as np

with rasterio.open(r"Dataset\Processed Data\slope.tif") as src:
    slope = src.read(1)
    profile= src.profile

with rasterio.open(r"Dataset\Processed Data\Labels.tif") as src:
    label = src.read(1)

labelCost= {10:8, 20:2, 30:2, 40:5, 50:1, 60:10, 80: 9999}

mapfunc = np.vectorize(lambda x: labelCost.get(x,9999))
costLabels = mapfunc(label)

slope_mapping = [(slope <= 5, 1),((slope > 5) & (slope <= 10), 3),
    ((slope > 10) & (slope <= 15), 6),
    ((slope > 15) & (slope <= 25), 9),(slope > 25, 9999)
]

slope_conditions = [pair[0] for pair in slope_mapping]
slope_choices = [pair[1] for pair in slope_mapping]

costSlope = np.select(slope_conditions, slope_choices, default=9999)

labelWt = 0.6
slopeWt= 0.4

combined = (costLabels*labelWt) + (costSlope*slopeWt)
combined = np.where((costLabels == 9999) | (costSlope == 9999), 9999, combined)

with rasterio.open(r"Dataset\Processed Data\CostSurface.tif", "w", **profile) as dst:
    dst.write(combined,1)