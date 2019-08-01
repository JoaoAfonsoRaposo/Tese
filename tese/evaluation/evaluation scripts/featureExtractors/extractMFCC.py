import numpy as np
import librosa
import csv
import sys
from sklearn.preprocessing import normalize
from sklearn.decomposition import PCA

from mutagen.mp3 import MP3

def main(audioFilePath):
    sampling_rate = 44100
    first_frame = 0
    
   
    mfcc_hopSize = int(8820/8)
    
    
    audio = MP3(audioFilePath)
    audio_length = audio.info.length - first_frame
    print("mfcc extractor (audio length):", audio_length)
    y, sr = librosa.load(audioFilePath, offset=first_frame, duration=audio_length, sr=sampling_rate)
    feature_list = librosa.feature.mfcc(y=y, sr=sr, hop_length=mfcc_hopSize, n_fft=2048)
    print("mfcc extractor (mfccList shape):", feature_list.shape)
    path_csv = "qm_featuresMFCC.csv"
    
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

    #print(mean_mfcc[10][11])
    #print(feature_list[10][89])
    #print(feature_list[10][90])
    #print(feature_list[10][91])
    #print(feature_list[10][92])
    #print(feature_list[10][93])
    #print(feature_list[10][94])
    #print(feature_list[10][95])
    #print(feature_list[10][96])
    #print(feature_list[10][97])
    #print(feature_list[10][98])
    #print(feature_list[10][99])
    #print(feature_list[10][100])

    
    #print((feature_list[10][89]+feature_list[10][90]+feature_list[10][91]+feature_list[10][92]+feature_list[10][93]+feature_list[10][94]+feature_list[10][95]+feature_list[10][96]+feature_list[10][97]+feature_list[10][98]+feature_list[10][99]+feature_list[10][100])/12)
    
    #print(mean_mfcc.shape)
    np.savetxt(path_csv, mean_mfcc, delimiter=',')


if __name__ == "__main__":
    main(sys.argv[1])
