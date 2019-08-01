import numpy as np
import librosa
import csv
import sys
from sklearn.preprocessing import normalize
from sklearn.decomposition import PCA

from mutagen.mp3 import MP3

def main(args):
    audioFilePath = args[1]
    featureType = args[2]
      
    sampling_rate = 44100
    chroma_sr = 40960
    first_frame = 0

    
    if len(args) == 3:
        path_csv = "../extractedFeatures/features.csv"
        if (featureType == "chroma"):
            print("Using default hopSize = 4096")
            chroma_hopSize = int(args[3])
        elif (featureType == "mfcc"):
            print("Using default hopSize = 8820/8")
            mfcc_hopSize = int(8820/8)
            
    elif len(args) == 4:
        path_csv = "../extractedFeatures/features.csv"
        if (featureType == "chroma"):
            chroma_hopSize = int(args[3])
        elif (featureType == "mfcc"):
            mfcc_hopSize = int(8820/8)
            
    elif len(args) == 5 and args[4] == "gcca":
        chroma_hopSize = int(args[3])
        mfcc_hopSize = int(8820/8)
        print("\nGCCA!\n")
        if(featureType == "chroma"):
            path_csv = "../extractedFeatures/qm_featuresChroma.csv"
        elif(featureType == "mfcc"):
            path_csv = "../extractedFeatures/qm_featuresMFCC.csv"
            
    else:
        print("unexpected number of arguments!")
        sys.exit(0)
    
    audio = MP3(audioFilePath)
    audio_length = audio.info.length - first_frame
    print(featureType + " extractor (audio length):", audio_length)
    #if (featureType == "chroma"):
        #sampling_rate = 40960
    y, sr = librosa.load(audioFilePath, offset=first_frame, duration=audio_length, sr=sampling_rate)
    
    if (featureType == "chroma"):
        y, sr = librosa.load(audioFilePath, offset=first_frame, duration=audio_length, sr=chroma_sr)
        if (chroma_hopSize == 4096):
            feature_list = librosa.core.cqt(y=y, sr=chroma_sr, hop_length=chroma_hopSize, n_bins=96, bins_per_octave=12, fmin=62)
        elif (chroma_hopSize == 8192):
            feature_list = librosa.core.cqt(y=y, sr=chroma_sr, hop_length=chroma_hopSize, n_bins=64, bins_per_octave=8, fmin=62)
        else:
            print("Invalid chroma hopSize ", chroma_hopSize)
            sys.exit(0)
        print("chroma extractor (chromaList shape):", feature_list.shape)
        #basis, lengths = librosa.filters.constant_q(sr,
                                        #fmin=62,
                                        #n_bins=64,
                                        #bins_per_octave=8)
                
        npFeatureList = np.abs(feature_list)
        pca = PCA(n_components=20)
        X = normalize(npFeatureList, norm='max', axis=1)
        X = np.transpose(X)
        X = pca.fit_transform(X)
        X = np.transpose(X)
        np.savetxt(path_csv, X, delimiter=',')
        
    elif (featureType == "mfcc"):
        y, sr = librosa.load(audioFilePath, offset=first_frame, duration=audio_length, sr=sampling_rate)
        feature_list = librosa.feature.mfcc(y=y, sr=sampling_rate, hop_length=mfcc_hopSize, n_fft=2048)
        print("mfcc extractor (mfccList shape):", feature_list.shape)
        n_frames = len(feature_list[0])
        n_frames_final = n_frames//8
        n_coeff = 20
        mean_mfcc = np.zeros((n_coeff, n_frames_final+1))

        tmp_arr = np.zeros(n_coeff)
        index = 0
        i = 0
        iters = 0
        while (i < n_frames):
            for j in range(0, 20):
                tmp_arr[j] += feature_list[j][i]
            if (i%(index*8+12) == 0 and i!=0):
                tmp_arr = tmp_arr/12
                mean_mfcc[:,index] = tmp_arr
                tmp_arr = np.zeros(n_coeff)
                i-=4
            if (iters%12 == 0 and iters!=0):
                index+=1
            i+=1
            iters+=1
        print(mean_mfcc.shape)
        print(len(mean_mfcc[0]))
        mean_mfcc = normalize(mean_mfcc, norm='max', axis=1)
        np.savetxt(path_csv, mean_mfcc, delimiter=',')
        print(mean_mfcc.shape)
        
    else:
        print("no such feature type")
    
    
if __name__ == "__main__":
    main(sys.argv)
