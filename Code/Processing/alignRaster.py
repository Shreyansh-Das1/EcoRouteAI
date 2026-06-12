import rasterio
from rasterio.warp import reproject
#to align rasters

with rasterio.open(r"Dataset\Processed Data\2021\Fused\fusedS.tif") as src: 
    with rasterio.open(r"Dataset\Processed Data\2021\Labels.tif") as ref:
        profile = ref.profile.copy()
        profile.update(dtype = "float32", count=src.count)

        with rasterio.open(r"Dataset\Processed Data\2021\fusedSC.tif","w", **profile) as dst:
            for band in range(1, src.count + 1):
                reproject(
                    source=rasterio.band(src, band),
                    destination=rasterio.band(dst, band),
                    src_transform=src.transform,
                    src_crs=src.crs,
                    dst_transform=ref.transform,
                    dst_crs=ref.crs
                )

