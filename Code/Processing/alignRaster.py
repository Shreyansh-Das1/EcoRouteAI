import rasterio
from rasterio.warp import reproject, Resampling
#to align rasters

with rasterio.open(r"Dataset\Labels.tiff") as src: 
    with rasterio.open(r"Dataset\downsampledFused.tif") as ref:
        profile = ref.profile.copy()
        profile.update(dtype = "uint8", count=1)

        with rasterio.open("alignedLabels.tif","w", **profile) as dst:
            reproject(
                source = rasterio.band(src,1),
                destination = rasterio.band(dst,1),
                src_transform = src.transform,
                src_crs =src.crs,
                dst_transform = ref.transform,
                dst_crs = ref.crs,
                resampling=Resampling.nearest
            )

