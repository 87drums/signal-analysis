# -*- coding:utf-8 -*-
import numpy as np
import scipy as sp
from scipy.fftpack import fft, fftfreq
from matplotlib import pyplot as plt

def do_fft(sig):
    win = sp.hamming(sig.size)
    sig_spectrum = fft(sig * win)
    return abs(sig_spectrum[: sig.size / 2 + 1])

def spectrum_cut(freqList):
    # --- 周波数帯制限---
    #low cut
    List_count_low = 0
    for row in freqList:
        if row >= 5: #5Hz以下カット
            break
        List_count_low += 1
    List_count_low -= 1

    #high cut
    List_count_high = 0
    for row in freqList:
        if row >= 500: #500Hz以上カット
            break
        List_count_high += 1

    return List_count_low, List_count_high

def p_spectrum_get(Myo_filename,Onset_filename):
    Myo_data1 = np.loadtxt(Myo_filename + "-1_trim.txt")
    Myo_data2 = np.loadtxt(Myo_filename + "-2_trim.txt")

    proces_time = Myo_data1[0]
    rate1 = int(Myo_data1.size // proces_time) #sampling rate   rate = int(Myo_wdata[0].astype(np.float64)//4)
    rate2 = int(Myo_data2.size // proces_time)

    Onset_array = np.loadtxt(Onset_filename)

    #観測叩打定義
    hit = 10
    start_p1 = int(Onset_array[hit] * rate1)
    end_p1 = int(Onset_array[hit + 1] * rate1)
    start_p2 = int(Onset_array[hit] * rate2)
    end_p2 = int(Onset_array[hit + 1] * rate2)

    power_spectrum1 = do_fft(Myo_data1[start_p1:end_p1])
    power_spectrum2 = do_fft(Myo_data2[start_p2:end_p2])

    #power_spectrum1[:50] = 0

    freqList1 = fftfreq(Myo_data1[start_p1:end_p1].size, d=1.0/ rate1)  #周波数の分解能計算
    freqList2 = fftfreq(Myo_data2[start_p2:end_p2].size, d=1.0/ rate2)  #周波数の分解能計算

    List_count_low1, List_count_high1 = spectrum_cut(freqList1)
    List_count_low2, List_count_high2 = spectrum_cut(freqList2)

    plt.subplot(211)
    plt.plot(power_spectrum1[List_count_high1:List_count_high1+1])
    plt.xticks((List_count_low1,List_count_high1//2,List_count_high1), (freqList1[List_count_low1],freqList1[List_count_high1//2],freqList1[List_count_high1]))

    plt.subplot(212)
    plt.plot(power_spectrum2[:List_count_high2+1])
    plt.xticks((List_count_low2,List_count_high2//2,List_count_high2), (freqList2[List_count_low2],freqList2[List_count_high2//2],freqList2[List_count_high2]))

    plt.show()

def wave_shape_get(Myo_filename,Onset_filename):
    Myo_data1 = np.loadtxt(Myo_filename + "-1_trim.txt")
    Myo_data2 = np.loadtxt(Myo_filename + "-2_trim.txt")

    proces_time = Myo_data1[0]
    rate = int(Myo_data1.size // proces_time) #sampling rate   rate = int(Myo_wdata[0].astype(np.float64)//4)
    Onset_array = np.loadtxt(Onset_filename)
    start_p = int(Onset_array[0] * rate)
    end_p = int(Onset_array[1] * rate)

    plt.subplot(211)
    plt.plot(Myo_data1[start_p + 1:end_p + 1])

    plt.subplot(212)
    plt.plot(Myo_data2[start_p + 1:end_p + 1])

    plt.show()

if __name__ == "__main__":
    filename_head = "../data/main experiment/1/"
    Myo_filename = filename_head + "myo/myo_file1"
    Onset_filename = filename_head + "analysis/onset_1_trim.txt"

    #wave_shape_get(Myo_filename,Onset_filename) #生データの波形確認
    p_spectrum_get(Myo_filename,Onset_filename) #パワースペクトル確認
