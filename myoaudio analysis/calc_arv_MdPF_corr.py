# --- coding:utf-8 ---

import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
from scipy.fftpack import fft, fftfreq
from scipy import hamming
import csv
import math #math.floor(x) 小数点以下切り捨て

import struct
import scipy.signal

def do_fft(sig):
    win = hamming(sig.size)
    sig_spectrum = fft(sig * win)
    return abs(sig_spectrum[: sig.size / 2 + 1])

def MdPF_ex(Myo_filename, Myo_analysis_filename, start_num, end_num):
    while start_num <= end_num:

        for index in range(2):
            #file read
            Myo_f = open(Myo_filename + str(start_num) + "-" + str(index + 1) + "_trim.txt", "r")
            Myo_fdata = Myo_f.read()
            Myo_f.close()

            Myo_wdata = np.array(Myo_fdata.split()) #\n \t \s split to array

            proces_time = Myo_wdata[0].astype(np.float64) #処理時間

            data = Myo_wdata[1:].astype(np.int16) #strings 2 float
            rate = int(data.size // proces_time) #sampling rate   rate = int(Myo_wdata[0].astype(np.float64)//4)

            nyq = rate / 2.0  # ナイキスト周波数

            # フィルタの設計
            # ナイキスト周波数が1になるように正規化
            fe1 = 5.0 / nyq      # カットオフ周波数1
            fe2 = 500.0 / nyq      # カットオフ周波数2
            numtaps = 255           # フィルタ係数（タップ）の数（要奇数）

            #    b = scipy.signal.firwin(numtaps, fe1)                         # Low-pass
            #    b = scipy.signal.firwin(numtaps, fe2, pass_zero=False)        # High-pass
            b = scipy.signal.firwin(numtaps, [fe1, fe2], pass_zero=False) # Band-pass
            #    b = scipy.signal.firwin(numtaps, [fe1, fe2])                  # Band-stop

            data_lowpass = scipy.signal.lfilter(b, 1, data)

            abs_data_lowpass = np.absolute(data_lowpass)

            time_sum = 0
            time_slide = 0.25 #0.3sずつスライド

            f_arv = open(Myo_analysis_filename + "arv" + str(start_num) + "-" + str(index + 1) + ".txt", "w")
            f_MdPF = open(Myo_analysis_filename + "MdPF" + str(start_num) + "-" + str(index + 1) + ".txt", "w")

            #shift_size = 1 * rate #sec * rate
            while proces_time > time_sum:
                start_point = int(math.floor(time_sum * rate))#int(math.floor(Onset_vdata[j]*rate))
                end_point = int(math.floor((time_sum + time_slide) * rate))#int(math.floor(Onset_vdata[j+1]*rate))

                #arv
                data_ave = np.average(abs_data_lowpass[start_point:end_point])

                f_arv.write(str(data_ave))
                f_arv.write("\n")

                #MdPF
                power_spectrum = do_fft(data_lowpass[start_point:end_point])

                freqList = fftfreq(data_lowpass[start_point:end_point].size, d = 1.0 / rate)  #周波数の分解能計算

                spectrum_sum = np.sum(power_spectrum)

                find_mid = 0
                i = 0

                while find_mid <= spectrum_sum/2:
                    find_mid += power_spectrum[i]
                    i += 1
                mid_f = i - 1

                f_MdPF.write(str(freqList[mid_f]))
                f_MdPF.write("\n")

                time_sum += time_slide

            f_arv.close()
            f_MdPF.close()

            data_arv = np.array(open(Myo_analysis_filename + "arv" + str(start_num) + "-" + str(index + 1) + ".txt", "r").read().split()).astype(np.float64)
            data_MdPF = np.array(open(Myo_analysis_filename + "MdPF" + str(start_num) + "-" + str(index + 1) + ".txt", "r").read().split()).astype(np.float64)

            f_arv_MdPF_corr = open(Myo_analysis_filename + "arv_MdPF_corr" + str(start_num) + "-" + str(index + 1) + ".txt", "w")
            f_arv_smooth = open(Myo_analysis_filename + "arv_smooth" + str(start_num) + "-" + str(index + 1) + ".txt", "w")

            """
            #データの長さが同じか確認
            if(data_arv.size == data_MdPF.size):
                print "same"
            else:
                print "different"
            """

            current_time = 0
            time_section = 2 #計算範囲秒数指定
            rate = 1 / time_slide #サンプリングレート
            while current_time < (data_arv.size / rate) - (time_section / 2):
                #calc corr
                current_index = int(current_time * rate)
                end_index = int((current_time + time_section) * rate)
                ar_Md_co = np.corrcoef(data_arv[current_index:end_index], data_MdPF[current_index:end_index])[0, 1]

                f_arv_MdPF_corr.write(str(ar_Md_co))
                f_arv_MdPF_corr.write("\n")

                #calc arv smooth
                arv_smooth = np.average(data_arv[current_index:end_index])
                f_arv_smooth.write(str(arv_smooth))
                f_arv_smooth.write("\n")

                current_time += time_section / 2
            f_arv_MdPF_corr.close()
            f_arv_smooth.close()

            f_arv.close()
            f_MdPF.close()

            """
            f = open(Myo_analysis_filename + str(start_num) + "-" + str(index + 1) + ".txt", "r")
            draw_data = np.array(f.read().split())
            f.close()

            plt.plot(range(len(draw_data)),draw_data)
            plt.show()
            """

        start_num += 1

if __name__ == "__main__":
    file_start = 1
    file_end = 6

    subject_start = 1
    subject_end = 6

    while subject_start <= subject_end:
        filename_head = "../data/main experiment/" + str(subject_start) + "/"
        Myo_filename = filename_head + "myo/myo_file"
        Myo_analysis_filename = filename_head + "analysis/myo_calc_"

        MdPF_ex(Myo_filename, Myo_analysis_filename, file_start, file_end)

        print "finish subject " + str(subject_start)

        subject_start += 1
