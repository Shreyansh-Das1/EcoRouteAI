import rasterio
from rasterio.transform import Affine

#Verifies the Boundary are same

with rasterio.open('Dataset\Processed Data\Labels.tif') as src:
    demShape = src.shape
    demCrs = src.crs
    demTransform = src.transform
    demBounds = src.bounds
    demRes = src.res
    print("Label Info:")
    print(f"  Shape: {demShape}")
    print(f"  CRS: {demCrs}")
    print(f"  Resolution: {demRes}")
    print(f"  Bounds: {demBounds}")
    print(f"  Transform:\n{demTransform}")


with rasterio.open(r'Dataset\Processed Data\2021\fused_stack.tif') as src:
    opt_shape = src.shape
    opt_crs = src.crs
    opt_transform = src.transform
    opt_bounds = src.bounds
    opt_res = src.res
    print("Fused Stack Info:")
    print(f"  Shape: {opt_shape}")
    print(f"  CRS: {opt_crs}")
    print(f"  Resolution: {opt_res}")
    print(f"  Bounds: {opt_bounds}")
    print(f"  Transform:\n{opt_transform}")


print(f"\nCRS: {demCrs == opt_crs}")
print(f"Bounds: {demBounds == opt_bounds}")
print(f"Top-left corner match: {demTransform.c == opt_transform.c and demTransform.f == opt_transform.f}")



'''Label Info:
  Shape: (1347, 2500)
  CRS: EPSG:32645
  Resolution: (28.418620505999982, 28.131303366740685)
  Bounds: BoundingBox(left=435261.994353, bottom=2610866.882561, right=506308.545618, top=2648759.748196)
  Transform:
| 28.42, 0.00, 435261.99|
| 0.00,-28.13, 2648759.75|
| 0.00, 0.00, 1.00|
Fused Stack Info:
  Shape: (1316, 2461)
  CRS: EPSG:32645
  Resolution: (28.79349362284501, 28.79349362284501)
  Bounds: BoundingBox(left=435431.20666596334, bottom=2610866.133013859, right=506291.9944717849, top=2648758.370621523)
  Transform:
| 28.79, 0.00, 435431.21|
| 0.00,-28.79, 2648758.37|
| 0.00, 0.00, 1.00|

CRS: True
Bounds: False
Top-left corner match: False'''