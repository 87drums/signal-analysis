# --- coding:utf-8 ---

import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
from scipy.fftpack import fft, fftfreq
from scipy import hamming
import math #math.floor(x) 小数点以下切り捨て

def SR_check(Midi_filename, file_num):
    #MIDI読み込み
    filename = Midi_filename + str(file_num) + ".txt"
    Midi_data = np.loadtxt(filename, dtype = "int")

    Midi_duration = np.array([])
    omit_tap = 1

    index = omit_tap
    while index <= Midi_data[:,0].size - omit_tap - 1:
        Midi_duration = np.append(Midi_duration, Midi_data[index][0] - Midi_data[index - 1][0])
        index += 1

    return (Midi_data[Midi_data[:,0].size-1][0] - Midi_data[0][0]) / 1000.0, np.var(Midi_duration), np.max(Midi_duration)/1000.0, np.min(Midi_duration)/1000.0, np.var(Midi_data[omit_tap:-omit_tap,1]), np.max(Midi_data[omit_tap:-omit_tap,1]), np.min(Midi_data[omit_tap:-omit_tap,1])

if __name__ == "__main__":
    time = []

    #書き出しファイル名
    TRY_TIME_OUTPUT_FILENAME = "../data/mainexperiment/result/try_time.txt"
    time_f = open(TRY_TIME_OUTPUT_FILENAME, "w")

    #被験者ナンバー
    start_sub_num = 1
    end_sub_num = 6

    #ファイルナンバー
    start_file_num = 1
    end_file_num = 3

    sub_num = start_sub_num
    while sub_num <= end_sub_num:
        #読み込みファイル名指定
        print "subject = ", sub_num
        filename_head = "../data/mainexperiment/" + str(sub_num) + "/"
        Midi_filename = filename_head + "midi/midi_file"

        file_num = start_file_num
        while file_num <= end_file_num:
            print "file = ", file_num
            try_time, var_time, time_max, time_min, var_vol, vol_max, vol_min = SR_check(Midi_filename, file_num)
            time_f.write(str(try_time) + "\t")
            time_f.write(str(var_time/1000.0) + "\t" + str(time_max) + "\t" + str(time_min) + "\t")
            time_f.write(str(var_vol) + "\t" + str(vol_max) + "\t" + str(vol_min) + "\n")

            file_num += 1
        sub_num += 1
    time_f.close()
