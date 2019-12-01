import os
import json
import numpy as np
import hashedindex
from collections import Counter

# storage_json = "./normalized_storage.json"
pitches_json = "pitches.json"
melody_json = "melody.json"


def store_melody(pitches_path,melody_path):
    with open(pitches_path,"r") as f:
        song_info = json.load(f)
    with open(melody_path, "w") as f:
        f.close()
    if song_info is not None:
        indicies_len = []
        aliases = []
        all_indicies = {}
        for alias in song_info:
            pitches = song_info[alias]['pitches']
            # print("alias:"+alias)
            indicies = {}
            all_indicies[alias] = indicies
            indicies['wavefile'] = song_info[alias]['wavefile']
            indicies['index'] = []
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
                        t0 = pitches[i][2]
                        t1 = pitches[k][2] - pitches[i][3]
                        t2 = pitches[j][2] - pitches[k][3]
                        indicies['index'].append((t0,f1,t1,f2,t2,f3))
                    j += 1
            print("alias:"+alias)
            # print(indicies[:10])
            aliases += [alias]
            indicies_len += [len(indicies["index"])]
        with open(melody_path, "w") as f:
            f.write(json.dumps(all_indicies, indent=4))
        # print(np.mean(indicies_len))
        # print(np.median(indicies_len))
        # print(np.min(indicies_len))
        # print(np.max(indicies_len))
        # print("min alias:" + aliases[indicies_len.index(np.min(indicies_len))])
        # print("max alias:" + aliases[indicies_len.index(np.max(indicies_len))])
        # with open(indicies.json,"w") as f:
        #     f.write(json.dumps(indicies))


def store_inverted(melody_path,inverted_path):
    with open(melody_path,"r") as f:
        all_indices = json.load(f)
    hash_index = hashedindex.HashedIndex()
    for alias in all_indices:
        indices = all_indices[alias]["index"]
        wavefile = all_indices[alias]["wavefile"]
        for index in indices:
            # f1 = ((index[0] + 0.025) // 0.05) * 0.05
            f1 = int((index[0]*100 + 2.5) // 5 * 5)
            t1 = int(((index[1]*100 + 5) // 10) * 10)
            f2 = int((index[2]*100 + 2.5) // 5 * 5)
            t2 = int(((index[3]*100 + 5) // 10) * 10)
            f3 = int((index[4]*100 + 2.5) // 5 * 5)
            hash_index.add_term_occurrence((f1,t1,f2,t2,f3),wavefile)
    inverted = {}
    items = hash_index.items()
    for key in items:
        counters = items[key].items()
        inverted[str(key)] = {}
        for file,times in counters:
            inverted[str(key)][file] = times
    with open(inverted_path,"w",encoding="utf-8") as f:
        f.write(json.dumps(inverted,indent=4))


if __name__ == "__main__":
    # store_melody(pitches_json,melody_json)
    # store_inverted(melody_json,"./inverted.json")
    hash_index = hashedindex.HashedIndex()
    with open("./inverted.json","r") as f:
        inverted_index = json.load(f)
    with open("./test_melody.json","r") as f:
        test_indices = json.load(f)
    for alias in test_indices:
        indices = test_indices[alias]["index"]
        wavefile = test_indices[alias]["wavefile"]
        allcounter = {}
        skip = 0
        for index in indices:
            f1 = int((index[0]*100 + 2.5) // 5 * 5)
            t1 = int(((index[1]*100 + 5) // 10) * 10)
            f2 = int((index[2]*100 + 2.5) // 5 * 5)
            t2 = int(((index[3]*100 + 5) // 10) * 10)
            f3 = int((index[4]*100 + 2.5) // 5 * 5)
            # if str((f1,t1,f2,t2,f3)) in inverted_index:
            #     song_counters = inverted_index[str((f1,t1,f2,t2,f3))]
            # else:
            mismatch_f = 3
            mismatch_t = 10
            flag = 0
            for i in range(-mismatch_f,mismatch_f+1):
                for j in range(-mismatch_t,mismatch_t+1):
                    for k in range(-mismatch_f,mismatch_f+1):
                        for m in range(-mismatch_t,mismatch_t+1):
                            for n in range(-mismatch_f,mismatch_f+1):
                                if str((f1+i*5, t1+j*10, f2+k*5, t2+m*10, f3+n*5)) in inverted_index:
                                    # song_counters = hash_index.get_documents((f1+i*5, t1+j*10, f2+k*5, t2+m*10, f3+n*5))
                                    song_counters = inverted_index[str((f1+i*5, t1+j*10, f2+k*5, t2+m*10, f3+n*5))]
                                    for song in song_counters:
                                        if song not in allcounter:
                                            allcounter[song] = song_counters[song]
                                        else:
                                            allcounter[song] += song_counters[song]
                                    flag = 1
                    #                     break
                    #             if flag == 1:
                    #                 break
                    #         if flag == 1:
                    #             break
                    #     if flag == 1:
                    #         break
                    # if flag == 1:
                    #     break
            if flag == 0:
                skip += 1
                continue
        ranks = sorted(allcounter.items(), key=lambda x: x[1], reverse=True)
        print(ranks)
        print(skip/len(indices))
