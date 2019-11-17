#!/usr/bin/env python3
import matplotlib.pyplot as plt
from matplotlib import collections as matcollect
import numpy as np
import itertools

def timeseries(pitches,normalized=None):
    pitchdata = []
    normalized_data=[]
    pitchtime = []
    for i in range(0,len(pitches)):
        pitchdata += [pitches[i][0]] * pitches[i][1]
        # normalized_data += [normalized[i][0]] * normalized[i][1]
        # delta = (pitches[i][3] - pitches[i][2]) / pitches[i][1]
        # pitchtime += [(pitches[i][2] + pitches[i][3])/2]* pitches[i][1]
        # pitchtime += [pitches[i][2] + j*delta for j in range(pitches[i][1])]
        pitchtime += [(pitches[i][2] + pitches[i][3])/2]* pitches[i][1]
    # plt.subplot(2,1,1)
    plt.plot(pitchtime,pitchdata)
    # plt.subplot(2,1,2)
    # plt.plot(pitchtime,normalized_data)
    plt.show()


def main():
    pass

if __name__ == "__main__":
    main()

