import rasterio
from rasterio.warp import reproject, Resampling

src_path = "MergedLabels.tif"          # source labels
ref_path = "Dataset\downsampledFused.tif"           # reference raster
dst_path = "worldcover_aligned.tif"

with rasterio.open(src_path) as src:
    with rasterio.open(ref_path) as ref:

        profile = ref.profile.copy()

        # single band categorical raster
        profile.update({
            "count": 1,
            "dtype": src.dtypes[0],
            "nodata": 0
        })

        with rasterio.open(dst_path, "w", **profile) as dst:

            reproject(
                source=rasterio.band(src, 1),
                destination=rasterio.band(dst, 1),

                src_transform=src.transform,
                src_crs=src.crs,

                dst_transform=ref.transform,
                dst_crs=ref.crs,

                resampling=Resampling.mode
            )

