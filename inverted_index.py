import os
import json
import numpy as np

storage_json = "storage.json"
indicies_json = "indicies_json"


with open(storage_json,"r") as f:
    song_info = json.load(f)
print(len(song_info["088"]["pitches"]))
print(len(song_info["011"]["pitches"]))
if song_info is not None:
    indicies_len = []
    aliases = []
    for alias in song_info:
        pitches = song_info[alias]['pitches']
        # print("alias:"+alias)
        indicies = []
        for i in range(len(pitches)):
            j = i + 1
            f1 = pitches[i][0]
            # time lag < 3s
            while j < len(pitches) and pitches[j][2] - pitches[i][2] < 3:
                if j == i + 1:
                    j += 1
                    continue
                f3 = pitches[j][0]
                for k in range(i+1,j):
                    f2 = pitches[k][0]
                    if (f1 < f2 and f2 < f3) or (f1 > f2 and f2 > f3):
                        continue
                    t1 = pitches[k][2] - pitches[i][3]
                    t2 = pitches[j][2] - pitches[k][3]
                    indicies.append((f1,t1,f2,t2,f3))
                j += 1
        print("alias:"+alias)
        print(indicies[:10])
        aliases += [alias]
        indicies_len += [len(indicies)]

    print(np.mean(indicies_len))
    print(np.median(indicies_len))
    print(np.min(indicies_len))
    print(np.max(indicies_len))
    print("min alias:" + aliases[indicies_len.index(np.min(indicies_len))])
    print("max alias:" + aliases[indicies_len.index(np.max(indicies_len))])
    # with open(indicies_json,"w") as f:
