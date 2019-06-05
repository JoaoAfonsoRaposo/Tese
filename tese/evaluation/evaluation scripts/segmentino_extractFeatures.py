#simple chroma extractor: reads audio file and writes chroma features and timestamps for eacch frame on a file (chromaValues.csv)

import librosa
import csv
import sys
import numpy as np
from mutagen.mp3 import MP3


def main(audioFilePath):
    sampling_rate = 44100
    first_frame = 0.0
    hop_size = 2048

    audio = MP3(audioFilePath)
    audio_length = audio.info.length-first_frame
    print("chroma extractor (audio length):", audio_length)

    y, sr = librosa.load(audioFilePath, offset=first_frame,duration=audio_length, sr=sampling_rate)
    chroma_list = librosa.feature.chroma_cqt(y=y, sr=hop_size*8, hop_length=hop_size)
    print("chroma extractor (chromaList shape):", chroma_list.shape)
    
    npChromaList = np.asarray(chroma_list)
    path_csv = "segmentino_chromas.csv"
    np.savetxt(path_csv, npChromaList, delimiter=',')

if __name__ == "__main__":
    main(sys.argv[1])
