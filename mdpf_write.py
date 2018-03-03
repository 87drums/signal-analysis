# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt

import scipy.signal as spsig
from scipy.fftpack import fft, fftfreq
from scipy import hamming

import matplotlib.pyplot as plt

import sys

#fft by hamming window
def do_fft(sig):
    win = hamming(sig.size)
    sig_spectrum = fft(sig * win)
    return abs(sig_spectrum[: (int)(sig.size / 2) + 1])

#MdPF calc
def MdPF_calc(Myo_Frames, Midi_Frames, omit_tap):
    MdPF_Frames = []

    rate = 1000 #sampling rate
    nyq = rate/2 #ナイキスト周波数

    i = omit_tap + 1

    while i <= len(Midi_Frames) - omit_tap - 1:
        start_point = Midi_Frames[i - 1][0] - Midi_Frames[omit_tap][0]
        end_point = Midi_Frames[i][0] - Midi_Frames[omit_tap][0]

        #high pass fir
        fe = 20.0 / nyq #[Hz]
        numtaps = 255 #フィルタ係数（タップの数（要奇数））
        co = spsig.firwin(numtaps, fe, pass_zero=False) #setting coefficient

        try:
            high_pass_sig = spsig.lfilter(co, 1, Myo_Frames[start_point:end_point])
        except:
            print(start_point, end_point, Myo_Frames[start_point:end_point], len(Myo_Frames))
            #sys.exit()

        power_spectrum = do_fft(high_pass_sig)
        freqList = fftfreq(high_pass_sig.size, d = 1.0 / rate)  #周波数の分解能計算

        # --- 表示周波数帯制限 ---
        #low cut
        List_count_low = 0
        for row in freqList:
            if (row > 20) or (row < 0): #20Hz以上
                List_count_low -= 1
                break
            List_count_low += 1

        #high cut
        List_count_high = 0
        for row in freqList:
            if (row > 500) or (row < 0): #500Hz以下
                List_count_high -= 1
                break
            List_count_high += 1

        spectrum_sum = np.sum(power_spectrum[List_count_low:List_count_high])

        find_mid = 0
        index = List_count_low

        while find_mid < spectrum_sum / 2:
            find_mid += power_spectrum[index]
            index += 1
        low_mid_f = index - 1

        find_mid = 0
        index = List_count_high

        while find_mid < spectrum_sum / 2:
            find_mid += power_spectrum[index]
            index -= 1
        hi_mid_f = index + 1

        MdPF_Frames.append((freqList[low_mid_f] + freqList[hi_mid_f]) / 2)

        i += 1
    return MdPF_Frames

def MdPF_write(MdPF_OUTPUT_FILENAME, MdPF_OUTPUT_FIGNAME, MdPF_Frames):
    f = open(MdPF_OUTPUT_FILENAME, "w")
    for row in MdPF_Frames:
        f.write(str(row))
        f.write("\n")
    f.close()

    plt.title(MdPF_OUTPUT_FILENAME)
    plt.plot(MdPF_Frames)

    plt.show()
    #plt.savefig(MdPF_OUTPUT_FIGNAME)
    plt.cla()

if __name__ == "__main__":
    #前後の省略叩打数
    omit_tap = 40
    MdPF_Frames = []

    #被験者ナンバー
    start_sub_num = 1
    end_sub_num = 1

    #ファイルナンバー
    start_file_num = 1
    end_file_num = 3

    sub_num = start_sub_num
    while sub_num <= end_sub_num:
        #読み込みファイル名指定
        print("subject = ", sub_num)
        filename_head = "../data/mainexperiment/" + str(sub_num) + "/"
        Myo_filename = filename_head + "myo/myo_file"
        Midi_filename = filename_head + "midi/midi_file"

        file_num = start_file_num
        while file_num <= end_file_num:
            print("file = ", file_num)
            #書き出しファイル名
            MdPF_OUTPUT_FILENAME1 = filename_head + "analysis/mdpf/mdpf_file" + str(file_num) + "ex_1kHz.txt"
            MdPF_OUTPUT_FILENAME2 = filename_head + "analysis/mdpf/mdpf_file" + str(file_num) + "fl_1kHz.txt"
            MdPF_OUTPUT_FIGNAME1 = "../data/mainexperiment/figure/mdpf/" + str(sub_num) + "mdpf_file" + str(file_num) + "ex_1kHz.png"
            MdPF_OUTPUT_FIGNAME2 = "../data/mainexperiment/figure/mdpf/" + str(sub_num) + "mdpf_file" + str(file_num) + "fl_1kHz.png"
            #Myo読み込み
            filename1 = Myo_filename + str(file_num) + "ex_resample.txt"
            filename2 = Myo_filename + str(file_num) + "fl_resample.txt"
            Myo_data1 = np.loadtxt(filename1, dtype = "float64")
            Myo_data2 = np.loadtxt(filename2, dtype = "float64")

            #MIDI読み込み
            filename = Midi_filename + str(file_num) + ".txt"
            Midi_data = np.loadtxt(filename, dtype = "int")

            MdPF_Frames1 = MdPF_calc(Myo_data1, Midi_data, omit_tap)
            MdPF_Frames2 = MdPF_calc(Myo_data2, Midi_data, omit_tap)

            MdPF_write(MdPF_OUTPUT_FILENAME1, MdPF_OUTPUT_FIGNAME1, MdPF_Frames1)
            MdPF_write(MdPF_OUTPUT_FILENAME2, MdPF_OUTPUT_FIGNAME2, MdPF_Frames2)

            file_num += 1
        sub_num += 1
