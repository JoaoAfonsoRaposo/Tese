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
    sr = 44100
    mfcc_sr = 22050
    chroma_sr = 40960
    cqt_sr = 40960
    first_frame = 0
    flag_gcca = 0
    
    audio = MP3(audioFilePath)
    audio_length = audio.info.length - first_frame
    print("audio length: ", audio_length)
    
    if (len(args) > 3):
        flag_gcca = 1
           
    if (flag_gcca == 0):
        path_csv = "../extractedFeatures/features.csv"

    if (featureType == "chroma"):
        if (flag_gcca == 1):
            path_csv = "../extractedFeatures/qm_featuresChroma.csv"  
            hopSize = int(chroma_sr/5)

        else:
            hopSize = int(chroma_sr/10)
        y, sr = librosa.load(audioFilePath, offset=first_frame, duration=audio_length, sr=chroma_sr)
        feature_list = librosa.feature.chroma_cqt(y=y, sr=chroma_sr, hop_length=hopSize, fmin=62, n_chroma=12, n_octaves=8, cqt_mode='hybrid')

        #print("chroma extractor (chromaList shape):", feature_list.shape)
        #basis, lengths = librosa.filters.constant_q(sr,
                                        #fmin=62,
                                        #n_bins=96,
                                        #bins_per_octave=12)
        #print("basis shape: ", basis.shape[1])
        np.savetxt(path_csv, feature_list, delimiter=',')
        
    elif (featureType == "cqt"):
        if (flag_gcca == 1):
            path_csv = "../extractedFeatures/qm_featuresCQT.csv"
        hopSize = int(cqt_sr/5)
        y, sr = librosa.load(audioFilePath, offset=first_frame, duration=audio_length, sr=cqt_sr)
        feature_list = librosa.core.cqt(y=y, sr=cqt_sr, hop_length=hopSize, n_bins=64, bins_per_octave=8, fmin=62, window="hamm", res_type='polyphase')
        
        print("cqt extractor (cqtList shape):", feature_list.shape)
        basis, lengths = librosa.filters.constant_q(sr,
                                        fmin=62,
                                        n_bins=64,
                                        bins_per_octave=8)
        print("basis shape: ", basis.shape[1])
        np.savetxt(path_csv+"raw", feature_list, delimiter=',')
        print(feature_list[10][10])
        print(feature_list[50][50])
        npFeatureList = np.abs(feature_list)
        print(npFeatureList[10][10])
        print(npFeatureList[50][50])
        print("feature", feature_list.shape)
        print("featureabs", npFeatureList.shape)
        pca = PCA(n_components=20)
        X = normalize(npFeatureList, norm='max', axis=1)
        X = np.transpose(X)
        X = pca.fit_transform(X)
        X = np.transpose(X)
        np.savetxt(path_csv, X, delimiter=',')
    
    elif (featureType == "mfcc"):
        if (flag_gcca == 1):
            path_csv = "../extractedFeatures/qm_featuresMFCC.csv"
        hopSize = 8820
        y, sr = librosa.load(audioFilePath, offset=first_frame, duration=audio_length, sr=sr)
        feature_list = librosa.feature.mfcc(y=y, sr=mfcc_sr, hop_length=hopSize, n_fft=1024)
        print("mfcc extractor (mfccList shape):", feature_list.shape)
        #mean_mfcc = normalize(feature_list, norm='max', axis=1)
        np.savetxt(path_csv, mean_mfcc, delimiter=',')
        print(feature_list.shape)
        
    else:
        print("no such feature type")
    
    
if __name__ == "__main__":
    main(sys.argv)
