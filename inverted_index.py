import os
import json


storage_json = "storage.json"
indicies_json = "indicies_json"

with open(storage_json,"r") as f:
    song_info = json.load(f)
if song_info is not None:
    for alias in song_info:

        pitches = alias['pitches']
        count = 0
        for i in range(len(pitches)):
            j = i + 1
            while j < len(pitches) and pitches[j][2] - 3 < pitches[i][2]:
                count += 1
                j += 1
                f1 = pitches

        print(count)
    # with open(indicies_json,"w") as f:
