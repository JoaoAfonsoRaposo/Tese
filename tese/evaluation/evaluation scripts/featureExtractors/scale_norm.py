import sys
import numpy as np
import sklearn.preprocessing as sk

def center(view):
    view_A = view
    view_B = view
    mean = np.mean(view_A, axis=1)
    view_B = sk.scale(view_B, with_std=False, axis=1)
    #print(view)
    #print('\n\n\n')
    #print(view_B)
    view_B = sk.normalize(view_B, axis=1, norm = 'l2')
    #print(view_B)

#def normalize(view):

def main(views):
    for view in views[1:]:
        view = np.loadtxt(view, delimiter=',')
        #view = view[:,0:10]
        view = center(view)
        #view = normalize(view)


#if __name__ == "__main__":
    #main(sys.argv)





#max(x.min(), x.max(), key=abs)
        
