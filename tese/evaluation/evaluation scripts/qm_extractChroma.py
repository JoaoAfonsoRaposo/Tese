
import librosa
import csv
import sys
from mutagen.mp3 import MP3


def main(audioFilePath):
    sampling_rate = 40960
    first_frame = 0.2
    hop_size = 8192

    audio = MP3(audioFilePath)
    audio_length = audio.info.length-first_frame
    print("chroma extractor (audio length):", audio_length)

    y, sr = librosa.load(audioFilePath, offset=first_frame,duration=audio_length, sr=sampling_rate)
    chroma_list = librosa.feature.chroma_cqt(y=y, sr=hop_size*3, hop_length=hop_size, fmin=62)
    print("chroma extractor (chromaList shape):", chroma_list.shape)

    timestamp = first_frame
    time_btw_frames = hop_size/sampling_rate
    nr_of_frames = chroma_list.shape[1]

    out_file = open("qm_chromaValues.csv", 'w')

    for i in range(nr_of_frames):
        chroma_vector = []
        for j in range(0, 12):
            chroma_vector.append(chroma_list[j][i])
        chroma_vector.append(timestamp)
        row = str(chroma_vector[0])
        for chroma_value in chroma_vector[1:]:
            row += ", "
            row += str(chroma_value)
        row += "\n"
        out_file.write(row)
        timestamp += time_btw_frames
    out_file.close()

if __name__ == "__main__":
    main(sys.argv[1])
