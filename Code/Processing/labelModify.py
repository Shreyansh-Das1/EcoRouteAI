import rasterio
from rasterio.merge import merge

tile1 = rasterio.open(r"Dataset\Labels\E084_Map.tif")
tile2 = rasterio.open(r"Dataset\Labels\E087_Map.tif")

mosaic, outTrans = merge([tile1,tile2]) #merges tiles in accordance with their Metadata 

opMetaData = tile1.meta.copy()

opMetaData.update({
        "driver": "GTiff",
    "height": mosaic.shape[1],
    "width": mosaic.shape[2],
    "transform": outTrans
})

with rasterio.open("MergedLabels.tif", "w", **opMetaData) as dst:
    dst.write(mosaic)
