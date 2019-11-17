# -*- coding: utf-8 -*-
# coding: utf-8
#!/usr/bin/env python3

from processor import normalize, dtw, euc,fdtw
from pitch_extract import track_pitch
import numpy as np
from visualizer import timeseries
from recorder import Recorder
import database


def process(hum):
    hum_normalized = normalize(hum)
    data = database.load()
    l = {}
    for alias in data:
        original = data[alias]['pitches']
        if alias == "000":
            print("same")
        dtwdist, dtwpath = dtw(hum_normalized, original, euc, 14)
        # dist_metric = np.zeros((len(hum_normalized),len(original)))
        # dtwpath,dtwdist  = fdtw(original, hum_normalized, dist_metric)
        l[alias] = (dtwdist, dtwpath)

    minalias = "000"
    for alias in l:
        if alias == "000":
            print("same")
        if l[alias][0] < l[minalias][0]:
            minalias = alias
        print(alias, l[alias][0])

    print("Min distance:" + minalias + "  " + str(l[minalias][0]))


def main():
    # start recording -> 5 sec default
    # recorder = Recorder()
    # frames = recorder.start(5)
    # recorder.write_wav(frames, "input.wav")

    # load the hum and process
    # print("E:\zjufiles\junior 1\DAM\exp2\musicplayer\static\data\水樹奈々\7COLORS\000.mp3")
    hum = track_pitch("E:\zjufiles\junior 1\DAM\exp2\musicplayer\static\data\水樹奈々\BLUE\\011.wav")
    # hum = track_pitch("E:\zjufiles\junior 1\DAM\exp2\musicplayer\static\data\水樹奈々\\7COLORS\\000.wav")
    print(len(hum))
    timeseries(hum)
    hum = track_pitch("E:\zjufiles\junior 1\DAM\exp2\musicplayer\static\data\水樹奈々\Preserved_Roses\\088.wav",normalization=False)
    print(len(hum))
    timeseries(hum)

    # timeseries(hum)
    # count = 0
    # print(len(hum))
    # for i in range(len(hum)):
    #     j = i + 1
    #     while j < len(hum) and hum[j][2] - 3 < hum[i][2]:
    #         count += 1
    #         j+=1
    # print(count)
    # print(len(normalize(hum)))
    # process(hum)

    """
    print("hum vs original")
    x = normalize(x)
    dtwdist, dtwpath = dtw(x, z, euc, 14)
    print(dtwdist)

    y = normalize(track_pitch("notNearOriginal.wav"))
    print("hum vs non-original")
    dtwdist, dtwpath = dtw(x, y, euc, 14)
    print(dtwdist)
    """

if __name__ == "__main__":
    main()

