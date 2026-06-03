import rasterio
from rasterio.warp import reproject,  Resampling

#Reducing resolution from 10x10 to 30x30m

with rasterio.open("fusedAOI.tif") as src:

    with rasterio.open(r"Dataset\DEM\DEM_32645.tif") as dem:
        targTrans = dem.transform
        targCRS = dem.crs
        targHght = dem.height
        targWdth = dem.width

    profile = src.profile.copy()
    profile.update({
        "crs":targCRS,
        "transform":targTrans,
        "width": targWdth,
        "height": targHght
    })

    with rasterio.open("downsampledFused.tif","w",**profile) as dst:
        for i in range(1, src.count+1):
            reproject(
                source = rasterio.band(src,i),
                destination=rasterio.band(dst,i),
                src_transform=src.transform,
                src_crs= src.crs,
                dst_transform= targTrans,
                dst_crs= targCRS,
                resampling=Resampling.average
            )
print(f"{targHght} x {targWdth}")