# -*- coding:utf-8 -*-
import numpy as np
import scipy as sp
from scipy.fftpack import fft, fftfreq
from matplotlib import pyplot as plt
import math

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

def high_pass_sig_get():
    #file read
    Myo_f = open(Myo_filename + str(start_num) + "-" + str(index + 1) + ".txt", "r")
    Myo_fdata = Myo_f.read()
    Myo_f.close()

    Myo_wdata = np.array(Myo_fdata.split()) #\n \t \s split to array

    proces_time = Myo_wdata[0].astype(np.float64) #処理時間

    data = Myo_wdata[1:].astype(np.float64) #strings 2 float
    #data = data #-430 #arduino uno when conect to Vin & gnd
    #abs_data = np.absolute(data) #for signal mean

    rate = int(data.size // proces_time) #sampling rate   rate = int(Myo_wdata[0].astype(np.float64)//4)
    nyq = rate/2 #ナイキスト周波数
    j = 0

    f = open(Myo_analysis_filename + str(start_num) + "-" + str(index + 1) + ".txt", "w")

    #shift_size = 1 * rate #sec * rate
    while j < (Onset_vdata.size - 1):
        start_point = int(math.floor(Onset_vdata[j]*rate))
        end_point = int(math.floor(Onset_vdata[j+1]*rate))

        #high pass fir
        fe = 20.0 / nyq #[Hz]
        numtaps = 255 #フィルタ係数（タップの数（要奇数））
        co = spsig.firwin(numtaps, fe, pass_zero=False) #setting coefficient
        high_pass_sig = spsig.lfilter(co, 1, data[start_point:end_point])

def wave_shape_get(Myo_filename, sub_num, file_num):
    Myo_data1 = np.loadtxt(Myo_filename + str(file_num) + "ex_resample.txt")
    Myo_data2 = np.loadtxt(Myo_filename + str(file_num) + "fl_resample.txt")

    """
    proces_time2 = Myo_data2[0]
    rate2 = 3000#Myo_data2.size / proces_time2 #sampling rate   rate = int(Myo_wdata[0].astype(np.float64)//4)
    Onset_array2 = np.loadtxt(Onset_filename + "1.txt")
    start_p2 = int(round(Onset_array2[0] * rate2)) #10-44
    end_p2 = int(round(Onset_array2[40] * rate2))
    print "2 = ", rate2, "sec duration = ", Onset_array[5]-Onset_array[0]
    """

    start_p = 0 #Onset_array[0] * rate)) #12-40
    end_p = len(Myo_data1) #int(round(proces_time*rate))#Onset_array[40] * rate))

    plt.subplot(2,1,1)
    plt.plot(Myo_data1[start_p:end_p])

    start_p = 0 #Onset_array[0] * rate)) #12-40
    end_p = len(Myo_data2) #int(round(proces_time*rate))#Onset_array[40] * rate))

    plt.subplot(2,1,2)
    plt.plot(Myo_data2[start_p:end_p])

    plt.show()

if __name__ == "__main__":
    sub_num = 1
    file_num = 2

    filename_head = "../data/mainexperiment/" + str(sub_num) + "/"
    Myo_filename = filename_head + "myo/myo_file"
    #Onset_filename = filename_head + "analysis/onset_time/onset_"

    wave_shape_get(Myo_filename, sub_num, file_num) #生データの波形確認
    #p_spectrum_get(Myo_filename,Onset_filename) #パワースペクトル確認
