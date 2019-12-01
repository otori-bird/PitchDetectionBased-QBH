# -*- coding: utf-8 -*-
# coding: utf-8

import os
import subprocess
from pydub import AudioSegment
from processor import normalize
from math import sin,pi


def track_pitch(inputFilename:str,sr=44100,normalization=True):
    # if inputFilename.endswith(".mp3"):
    #     print(os.getcwd())
    #     file = open(inputFilename[:-4]+".wav","wb")
    #     file.close()
    #     sound = AudioSegment.from_mp3(inputFilename)
    #     sound.export(inputFilename[:-4]+".wav", format="wav")
    #     inputFilename = inputFilename[:-4]+".wav"

    #Load the Aubiopitch from command and save the data onto a file
    status,result = subprocess.getstatusoutput("aubiopitch -i \"" + inputFilename+ "\" -r " + str(sr) +" -l 0.8 > temp.txt")
    if status != 0:
        print(status)
        print(result)
        return False
    #Use the file to read the frequencies next
    with open("temp.txt","r",encoding="utf-8") as file:
        all_frequency = file.read().split()
    all_frequency = [float(i) for i in all_frequency]
    
    #delete the temp file beacuse it is not needed anymore
    # os.system("rm temp.txt")
    #Pitch obtained in the form of [Time,Frequency]. Ignore time for now
    useful_frequency = []
    for i in range(0, len(all_frequency),2):
        if all_frequency[i+1] < 100 or all_frequency[i+1]>2000:
            continue
        useful_frequency.append((all_frequency[i],all_frequency[i+1]))

    if normalization:
        useful_frequency = normalize(useful_frequency)
        #Pitches is the list of pitches after averaging
        pitches = []

        #temp to hold the current clusture
        temp = []

        #prev_pitch is the centre of the clusture
        prev_pitch = useful_frequency[0][1]
        prev_time = 0

        for (time,pitch) in useful_frequency:
            # pitch is compared with the prev_pitch or centre and a minimum deviation of 15hz
            # 15hz is just trail stuff. Need to see if anything good comes with differed values
            if abs(pitch - prev_pitch) < 0.05 and abs(time - prev_time) < 0.5:
                # add the pitch in the clusture
                temp += [pitch]
                # Update the prev_pitch/centre
                prev_pitch = sum(temp)/float(len(temp))
                prev_time = time
            else:
                # make sure temp(clusture) is big enough to be a valid clusture(size = 10)
                if len(temp) > 10:
                    # add the centre and lenth of clusture in the list
                    # pitch pitch_times start_time end_time
                    pitches += [(prev_pitch, len(temp), prev_time, time)]
                # Update temp(new clusture) and prev_pitch accordingly
                temp = []
                prev_pitch = pitch
                prev_time = time

    else:
        # Pitches is the list of pitches after averaging
        pitches = []

        # temp to hold the current clusture
        temp = []

        # prev_pitch is the centre of the clusture
        prev_pitch = useful_frequency[0][1]
        prev_time = 0

        for (time, pitch) in useful_frequency:
            # pitch is compared with the prev_pitch or centre and a minimum deviation of 15hz
            # 15hz is just trail stuff. Need to see if anything good comes with differed values
            if abs(pitch - prev_pitch) < 20 and abs(time - prev_time) < 0.5:
                # add the pitch in the clusture
                temp += [pitch]
                # Update the prev_pitch/centre
                prev_pitch = sum(temp) / float(len(temp))
                prev_time = time
            else:
                # make sure temp(clusture) is big enough to be a valid clusture(size = 10)
                if len(temp) > 10:
                    # add the centre and lenth of clusture in the list
                    # pitch pitch_times start_time end_time
                    pitches += [(prev_pitch, len(temp), prev_time, time)]
                # Update temp(new clusture) and prev_pitch accordingly
                temp = []
                prev_pitch = pitch
                prev_time = time
    return pitches


def main():
    track_pitch("E:\zjufiles\junior 1\DAM\exp2\musicplayer\static\data\水樹奈々\\7COLORS\\000.wav")
    pass


if __name__ == "__main__":
    main()
