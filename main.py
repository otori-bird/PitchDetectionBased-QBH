# -*- coding: utf-8 -*-
# coding: utf-8
#!/usr/bin/env python3

from processor import *
from pitch_extract import track_pitch
import numpy as np
from visualizer import timeseries
from recorder import Recorder
from database import *
from inverted_index import *


def process(hum):
    hum_normalized = normalize_time(hum)
    data = load(pitches_json)
    l = {}
    for alias in data:
        compare_from_db = data[alias]['pitches']
        compare_from_db_normalized = normalize_time(compare_from_db)
        if alias == "000":
            print("same")
        dtwdist, dtwpath = dtw(hum_normalized, compare_from_db_normalized, euc, 14)
        # dist_metric = np.zeros((len(hum_normalized),len(original)))
        # dtwpath,dtwdist  = fdtw(original, hum_normalized, dist_metric)
        l[alias] = (dtwdist, dtwpath)
    a = sorted(l.items(),key=lambda x:x[1][0])
    print(a)


def main():
    # start recording -> 5 sec default
    # recorder = Recorder()
    # frames = recorder.start(5)
    # recorder.write_wav(frames, "input.wav")

    # load the hum and process
    # print("E:\zjufiles\junior 1\DAM\exp2\musicplayer\static\data\水樹奈々\7COLORS\000.mp3")
    # hum = track_pitch("E:\zjufiles\junior 1\DAM\exp2\musicplayer\static\data\水樹奈々\BLUE\\011.wav",normalization=True)
    # # hum = track_pitch("E:\zjufiles\junior 1\DAM\exp2\musicplayer\static\data\水樹奈々\\7COLORS\\000.wav")
    # print(len(hum))
    # timeseries(hum)
    # hum = track_pitch("E:\zjufiles\junior 1\DAM\exp2\musicplayer\static\data\水樹奈々\BLUE\\011.wav",normalization=False)
    # print(len(hum))
    # timeseries(hum)

    hum = track_pitch("./test/mine/exterminate.wav")
    process(hum)
    # store("E:\zjufiles\junior 1\DAM\exp2\musicplayer\static\data\水樹奈々\Exterminate\\030.wav",
    #       "test",store_path="./test2_pitches.json")
    # store_melody("./test2_pitches.json","./test2_melody.json")
    # store_inverted("./test2_melody.json","./test2_inverted.json")
    # store("./test/mine/exterminate.wav","test",store_path="./test_pitches.json")
    # store_melody("./test_pitches.json","./test_melody.json")
    # store_inverted("./test_melody.json","./test_inverted.json")


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

