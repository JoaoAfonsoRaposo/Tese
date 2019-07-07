import numpy as np
import librosa
import csv
import sys
from mutagen.mp3 import MP3
from sklearn.decomposition import PCA

def main(audioFilePath, featureType):
    sampling_rate = 40960
    first_frame = 0
    
    chromaCQT_hopSize = 4096
    #chromaCQT_framesize = 15872
    
    mfcc_hopSize = 8820
    mfcc_frameSize = 26460
    
    nfft= 13230
    
    
    audio = MP3(audioFilePath)
    audio_length = audio.info.length - first_frame
    print(featureType + " extractor (audio length):", audio_length)
    #if (featureType == "chroma"):
        #sampling_rate = 40960
    y, sr = librosa.load(audioFilePath, offset=first_frame, duration=audio_length, sr=sampling_rate)
    if (featureType == "chroma"):
        #feature_list = librosa.feature.chroma_cqt(y=y, sr=sampling_rate, hop_length=chromaCQT_hopSize, n_chroma=12, n_octaves= 8, fmin=62)
        feature_list = librosa.core.cqt(y=y, sr=sampling_rate, hop_length=chromaCQT_hopSize, n_bins=96, fmin=62, bins_per_octave=12, window = 'hamm')
        print("chroma extractor (chromaList shape):", feature_list.shape)
        path_csv = "qm_featuresChroma.csv"
    elif (featureType == "mfcc"):
        feature_list = librosa.feature.mfcc(y=y, sr=sr, hop_length=mfcc_hopSize, n_fft=nfft)
        print("mfcc extractor (mfccList shape):", feature_list.shape)
        path_csv = "qm_featuresMFCC.csv"
    else:
        print("no such feature type")
        
    npFeatureList = np.abs(feature_list)
    pca = PCA(n_components=20)
    X = np.transpose(pca.fit_transform(np.transpose(npFeatureList)))
    np.savetxt(path_csv, X, delimiter=',')

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
