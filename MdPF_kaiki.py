# -*- coding:utf-8 -*-
import numpy as np
from matplotlib import pyplot as plt

def MdPF_kaiki(filename, onset_filename):
    myo_f = np.loadtxt(filename)
    onset_f = np.loadtxt(onset_filename)

    z = np.polyfit(onset_f[2:], myo_f[1:], 1)

    p = np.poly1d(z)
    print "傾き ＝ " + str(p.c[0])

    plt.hold(True)
    plt.scatter(onset_f[2:], myo_f[1:])

    ax = range(600)
    ay = p(ax)

    plt.plot(ax, ay)

    plt.show()


if __name__ == "__main__":
    filename = "../data/preexperiment/20170622 myo_pre/analysis/MdPF/myo_MdPF1-2.txt"
    onset_filename = "../data/preexperiment/20170622 myo_pre/analysis/onset_time/onset_1.txt"

    MdPF_kaiki(filename, onset_filename)
