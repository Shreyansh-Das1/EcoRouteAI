import numpy as np
import os 

n = 1
stitched = []
row = []
dir = r"Dataset\Processed Data\Training\fusedTiles"
for i in range(1,241):
    file = f"{i:04d}.npy"
    path = os.path.join(dir, file)
    row.append(np.load(path))
    if(n%5 == 0):
        stitched.append(row.copy())
        row = []
    n +=1
np.save("stitchedAOI.npy", np.block(stitched))
    