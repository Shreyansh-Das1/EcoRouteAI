import torch as trc
from torch.utils.data import DataLoader, Dataset
from pathlib import Path
import numpy as np

class LulcDataset(Dataset):
    def __init__(self, dir, transform =None):
        self.dir = Path(dir)
        self.transform = transform
        self.fused = sorted(list((self.dir / "Fused").glob("*.*")))
        self.labels = sorted(list((self.dir / "Labels").glob("*.*")))

    def __len__(self):
        return len(self.fused)
    
    def __getitem__(self, index):
        fusedpth = self.fused[index]
        labelpth = self.labels[index]

        fused = np.load(fusedpth)
        fused = trc.from_numpy(fused)

        label = np.load(labelpth)
        label = trc.from_numpy(label)

        return fused,label
        