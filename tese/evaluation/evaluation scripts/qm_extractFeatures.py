import numpy as np
import librosa
import csv
import sys
from mutagen.mp3 import MP3

def main(audioFilePath, featureType):
    sampling_rate = 40960
    first_frame = 0
    hop_size = 8192

    audio = MP3(audioFilePath)
    audio_length = audio.info.length - first_frame
    print(featureType + " extractor (audio length):", audio_length)

    y, sr = librosa.load(audioFilePath, offset=first_frame, duration=audio_length, sr=sampling_rate)
    
    if (featureType == "chroma"):
        feature_list = librosa.feature.chroma_cqt(y=y, sr=hop_size*3, hop_length=hop_size, fmin=62)
        print("chroma extractor (chromaList shape):", feature_list.shape)
    elif (featureType == "mfcc"):
        feature_list = librosa.feature.mfcc(y=y, sr=sr, hop_length=int(hop_size/2), n_fft=hop_size)
        print("mfcc extractor (mfccList shape):", feature_list.shape)
    else:
        print("no such feature type")
        
    npFeatureList = np.asarray(feature_list)
    path_csv = "qm_features.csv"
    np.savetxt(path_csv, npFeatureList, delimiter=',')
    

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
