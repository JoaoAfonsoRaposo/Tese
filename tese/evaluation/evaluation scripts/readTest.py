import numpy as np

path_csv = "qm_features.csv"
arr = np.loadtxt(path_csv, delimiter=',')
print(arr.shape)
