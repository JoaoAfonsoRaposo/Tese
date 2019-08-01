import sys
import numpy as np

def main(featureType, album, song):
    print("album: ", str(int(album)+1))
    print("song: ", str(int(song)+1))
    base_path = "/afs/l2f/home/jar/Documents/tese/Tese/tese/evaluation/evaluation scripts/features"
    path = base_path + '/' + featureType + '/' + str(int(album)+1) + '/' + str(int(song)+1) + ".csv"
    arr = np.array([path])
    print(path)
    np.savetxt("/afs/l2f/home/jar/Documents/tese/Tese/tese/evaluation/evaluation scripts/features/path.txt", arr, fmt = "%s")



if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3])
