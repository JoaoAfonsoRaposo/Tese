import sys
import numpy as np

def main(args):
    
    path_mfcc = "/afs/l2f/home/jar/Documents/tese/Tese/tese/evaluation/evaluation scripts/extractedFeatures/3features.csv"
    path_chroma = "/afs/l2f/home/jar/Documents/tese/Tese/tese/evaluation/evaluation scripts/extractedFeatures/2features.csv"
    path_cqt = "/afs/l2f/home/jar/Documents/tese/Tese/tese/evaluation/evaluation scripts/extractedFeatures/1features.csv"
    paths = {"1": path_cqt, "2": path_chroma, "3": path_mfcc}
    views = []
    
    for feature in args[1:]:
        for key in paths:
            if (feature == key):
                path = paths[feature]
                view = np.loadtxt(path, delimiter=',')
                views.append(view)
    
    min_frames = len(views[0][0])
    for view in views:
        if len(view[0]) < min_frames:
            min_frames = len(view[0])
            
            
    print(min_frames)
    for i in range(0, len(views)):
        counter = 0
        while (len(views[i][0]) > min_frames):
            counter += 1
            views[i] = np.delete(views[i], (0), axis=1)
        print(counter, "frames were removed")
        
    for view in views:
        #print(view[3,0:70])
        print(view.shape)
        
    arr_concatenate = np.concatenate(np.array(views), axis=0)
    
    path_csv = "../extractedFeatures/features.csv"
    np.savetxt(path_csv, arr_concatenate, delimiter=',')
    
    
    
if __name__ == "__main__":
    main(sys.argv)
