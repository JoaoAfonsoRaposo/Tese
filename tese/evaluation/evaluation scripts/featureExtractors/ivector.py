import numpy as np
import bob.bio.gmm.algorithm.IVector as IV
from glob import glob

ivec = IV(20,number_of_gaussians=20)
#ivector = bob.bio.gmm.algorithm.IVector(20)
path = "../features/mfcc/1/*"

fnames = glob(path)
arrays = [np.loadtxt(f, delimiter=",") for f in fnames]
#training = np.concatenate(arrays, axis=1)
training = np.array(arrays)

train = np.array([training])

print(training.shape)
print(training.dtype)

ivec.train_projector(train, 'projector')
