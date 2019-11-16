#!/usr/bin/env python3

import json
import sys
from pitch_extract import track_pitch
from processor import normalize
import os


def load():
    data = {}
    try:
        with open("storage.json","r") as f:
            temp = f.read()
            if temp == "" or temp is None:
                data = {}
            else:
                f.seek(0)
                data = json.load(f)
    except FileNotFoundError:
        open("storage.json", "w").write('')
        return {}
    return data

def store(wavefile, alias,sr=44100):
    print("extracting pitches...")
    data = load()
    data[alias] = {}
    if data[alias]:
        return

    d = {}
    d['wavefile'] = wavefile
    d['pitches'] = track_pitch(wavefile,sr)
    if d['pitches'] == False:
        return
    d['pitches'] = normalize(d['pitches'])
    data[alias] = d
    datastr = json.dumps(data, indent=4)
    with open("storage.json", "w") as f:
        f.write(datastr)

def main():
    # argv = sys.argv[1:]
    # store(argv[0], argv[1])
    # store("data/slow.wav","slowwave",8000)
    for root,dirs,files in os.walk("E:\zjufiles\junior 1\DAM\exp2\musicplayer\static\data\水樹奈々"):
        for file in files:
            if  file.endswith(".wav"):
                store(os.path.join(root,file),file[:-4])

if __name__ == "__main__":
    main()

