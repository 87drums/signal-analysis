# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt

import scipy.signal as spsig
from scipy.fftpack import fft, fftfreq
from scipy import hamming
import math

import matplotlib.pyplot as plt

import sys

#midi_setting_limit
up_limit = 80 #upper limit
bo_limit = 50 #bottom limit

#fft by hamming window
def do_fft(sig):
    win = hamming(sig.size)
    sig_spectrum = fft(sig * win)
    return abs(sig_spectrum[:(int)(sig.size / 2 + 1)])

#MdPF calc
def MdPF_ARV_calc(Myo_Frames, Midi_Frames, omit_tap):
    MdPF_Frames = []
    ARV_Frames = []

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

        #フレーム数足りてる場合
        try:
            high_pass_sig = spsig.lfilter(co, 1, Myo_Frames[start_point:end_point])
            ARV_Frames.append(np.average(Myo_Frames[start_point:end_point]))

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
        #フレーム数足りてない場合
        except:
            #print("test")
            #print start_point, end_point, Myo_Frames[start_point:end_point], len(Myo_Frames)
            #sys.exit()
            pass

        i += 1
    return MdPF_Frames, ARV_Frames

#MdPFとARVから筋疲労度算出 corr_tap_numは相関係数の窓幅
def Myo_fatigue(MdPF_Frames, ARV_Frames, corr_tap_num):
    index = 0
    Fatigue_Frames = []
    while index + corr_tap_num <= len(MdPF_Frames):
        Fatigue_Frames.append(np.corrcoef(MdPF_Frames[index:index + corr_tap_num], ARV_Frames[index:index + corr_tap_num])[0, 1])
        index += int(math.ceil(corr_tap_num / 10.0)) #窓幅の1/10を移動幅と設定，小数点以下は切り上げ
    return Fatigue_Frames

#全体の面積における負の相関（疲労状態）の割合
def Ratio_calc(Myo_fatigue_Frames):
    frames_sum = 0
    minus_sum = 0
    for row in Myo_fatigue_Frames:
        frames_sum += abs(row)
        if row < 0:
            minus_sum += abs(row)
    return float(minus_sum) / float(frames_sum), np.var(Myo_fatigue_Frames)

def Frate_MIDI_write(OUTPUT_FIGNAME, Myo_fatigue_Frames, Midi_Frames):
    Midi_normalize_Frames = []
    for row in Midi_Frames:
        Midi_normalize_Frames.append(((row / 127.0)-0.5)*2)

    #plt.title(OUTPUT_FIGNAME)
    plt.plot(Myo_fatigue_Frames, linewidth=5)
    print(Myo_fatigue_Frames[1])
    #plt.plot(Midi_normalize_Frames, linewidth=1)
    #plt.hlines(y = [((up_limit/127.0)-0.5)*2, ((bo_limit/127.0)-0.5)*2], xmin = 0, xmax = len(Midi_normalize_Frames)-1)

    plt.show()
    #plt.savefig(OUTPUT_FIGNAME)
    plt.cla()

def MdPF_write(MdPF_OUTPUT_FILENAME, MdPF_OUTPUT_FIGNAME, MdPF_Frames, fh):
    f = open(MdPF_OUTPUT_FILENAME, "w")
    for row in MdPF_Frames:
        f.write(str(row))
        f.write("\n")
    f.close()

    plt.title(MdPF_OUTPUT_FILENAME)
    plt.plot(MdPF_Frames, linewidth = 5)
    #plt.plot(fh)

    #plt.show()
    plt.savefig(MdPF_OUTPUT_FIGNAME)
    plt.cla()

def Calc_fatigue_futuers(fatigue_Frames):
    threshold = -0.2
    f_duration = 0
    f_times = 0

    index = 0
    while index <= len(fatigue_Frames) - 1:
        if fatigue_Frames[index] <= threshold:
            f_times += 1
            while index <= len(fatigue_Frames) - 1 and fatigue_Frames[index] <= threshold:
                f_duration += 1
                index += 1
            index -= 1
        index += 1

    return f_times, f_duration

if __name__ == "__main__":
    #疲労傾向に関するファイル書き出し
    FATIGUE_FUTUERS_OUTPUT_FILENAME = "../data/mainexperiment/result/fatigue_futuers.txt"
    fatigue_f = open(FATIGUE_FUTUERS_OUTPUT_FILENAME, "w")

    #前後の省略叩打数
    omit_tap = 40
    MdPF_Frames = []

    #被験者ナンバー
    start_sub_num = 6
    end_sub_num = 6

    #ファイルナンバー
    start_file_num = 3
    end_file_num = 3

    sub_num = start_sub_num
    while sub_num <= end_sub_num:
        #読み込みファイル名指定
        print ("subject = ", sub_num)
        filename_head = "../data/mainexperiment/" + str(sub_num) + "/"
        Myo_filename = filename_head + "myo/myo_file"
        Midi_filename = filename_head + "midi/midi_file"

        MdPF_RECURRENCE_OUTPUT_FILENAME = filename_head + "analysis/mdpf_recurrence/mdpf_file_recurrence.txt"
        recurrence_f = open(MdPF_RECURRENCE_OUTPUT_FILENAME, "w")

        CORR_RATIO_OUTPUT_FILENAME = filename_head + "analysis/mdpf_arv_corr/fatigue_ratio_file.txt"
        ratio_f = open(CORR_RATIO_OUTPUT_FILENAME, "w")

        file_num = start_file_num
        while file_num <= end_file_num:
            print ("file = ", file_num)
            #書き出しファイル名
            MdPF_OUTPUT_FILENAME1 = filename_head + "analysis/mdpf/mdpf_file" + str(file_num) + "ex_1kHz.txt"
            MdPF_OUTPUT_FILENAME2 = filename_head + "analysis/mdpf/mdpf_file" + str(file_num) + "fl_1kHz.txt"
            MdPF_OUTPUT_FIGNAME1 = "../data/mainexperiment/figure/mdpf_recurrence/" + str(sub_num) + "mdpf_file" + str(file_num) + "ex_1kHz.png"
            MdPF_OUTPUT_FIGNAME2 = "../data/mainexperiment/figure/mdpf_recurrence/" + str(sub_num) + "mdpf_file" + str(file_num) + "fl_1kHz.png"

            CORR_OUTPUT_FILENAME1 = filename_head + "analysis/mdpf_arv_corr/fatigue_file" + str(file_num) + "ex_1kHz.txt"
            CORR_OUTPUT_FILENAME2 = filename_head + "analysis/mdpf_arv_corr/fatigue_file" + str(file_num) + "fl_1kHz.txt"
            CORR_OUTPUT_FIGNAME1 = "../data/mainexperiment/figure/mdpf_arv_corr/" + str(sub_num) + "fatigue_file" + str(file_num) + "ex_1kHz.png"
            CORR_OUTPUT_FIGNAME2 = "../data/mainexperiment/figure/mdpf_arv_corr/" + str(sub_num) + "fatigue_file" + str(file_num) + "fl_1kHz.png"

            FRATE_MIDI_OUTPUT_FIGNAME1 = "../data/mainexperiment/figure/fatigue_rate_midi/aaaaaa/" + str(sub_num) + "fatigue_file" + str(file_num) + "ex_1kHz_aaaaaaaaaaa.png"
            FRATE_MIDI_OUTPUT_FIGNAME2 = "../data/mainexperiment/figure/fatigue_rate_midi/aaaaaa/" + str(sub_num) + "fatigue_file" + str(file_num) + "fl_1kHz_aaaaaaaaaaa.png"

            #Myo読み込み
            filename1 = Myo_filename + str(file_num) + "ex_resample.txt"
            filename2 = Myo_filename + str(file_num) + "fl_resample.txt"
            Myo_data1 = np.loadtxt(filename1, dtype = "float64")
            Myo_data2 = np.loadtxt(filename2, dtype = "float64")

            #MIDI読み込み
            filename = Midi_filename + str(file_num) + ".txt"
            Midi_data = np.loadtxt(filename, dtype = "int")

            #MdPF, ARV算出
            MdPF_Frames1, ARV_Frames1 = MdPF_ARV_calc(Myo_data1, Midi_data, omit_tap)
            MdPF_Frames2, ARV_Frames2 = MdPF_ARV_calc(Myo_data2, Midi_data, omit_tap)

            """#MdPF回帰直線算出
            x1 = np.linspace(1, len(MdPF_Frames1), len(MdPF_Frames1)) #x1 = range(len(MdPF_Frames1))
            a1, b1 = np.polyfit(x1, MdPF_Frames1, 1)
            fh1 = a1 * x1 + b1

            x2 = np.linspace(1, len(MdPF_Frames2), len(MdPF_Frames2)) #x2 = range(len(MdPF_Frames2))
            a2, b2 = np.polyfit(x2, MdPF_Frames2, 1)
            fh2 = a2 * x2 + b2

            #テキスト，フィギュア書き出し
            MdPF_write(MdPF_OUTPUT_FILENAME1, MdPF_OUTPUT_FIGNAME1, MdPF_Frames1, fh1)
            MdPF_write(MdPF_OUTPUT_FILENAME2, MdPF_OUTPUT_FIGNAME2, MdPF_Frames2, fh2)
            """
            #筋疲労度算出
            corr_tap_num = 40 #相関係数を見る窓幅（単位は叩打数），移動幅が1/10なので10以上で
            Myo_fatigue_Frames1 = Myo_fatigue(MdPF_Frames1, ARV_Frames1, corr_tap_num)
            Myo_fatigue_Frames2 = Myo_fatigue(MdPF_Frames2, ARV_Frames2, corr_tap_num)

            #負の相関割合算出
            try:
                minus_ratio1, var_fatigue1 = Ratio_calc(Myo_fatigue_Frames1)
                minus_ratio2, var_fatigue2 = Ratio_calc(Myo_fatigue_Frames2)

                ratio_f.write(str(minus_ratio1) + "\t" + str(minus_ratio2) + "\t" + str(var_fatigue1) + "\t" + str(var_fatigue2) + "\n")
            except:
                pass

            #相関係数回帰直線算出
            try:
                """
                x1 = np.linspace(1, len(Myo_fatigue_Frames1), len(Myo_fatigue_Frames1)) #x1 = range(len(Myo_fatigue_Frames1))
                a1, b1 = np.polyfit(x1, Myo_fatigue_Frames1, 1)
                fh1 = a1 * x1 + b1

                x2 = np.linspace(1, len(Myo_fatigue_Frames2), len(Myo_fatigue_Frames2)) #x2 = range(len(Myo_fatigue_Frames2))
                a2, b2 = np.polyfit(x2, Myo_fatigue_Frames2, 1)
                fh2 = a2 * x2 + b2

                MdPF_write(CORR_OUTPUT_FILENAME1, CORR_OUTPUT_FIGNAME1, Myo_fatigue_Frames1, fh1)
                MdPF_write(CORR_OUTPUT_FILENAME2, CORR_OUTPUT_FIGNAME2, Myo_fatigue_Frames2, fh2)
                """
                pass
            except:
                print ("miss")
                pass
            #print len(Myo_fatigue_Frames1), len(Midi_data[omit_tap : -(omit_tap*2) :int(math.ceil(omit_tap/10)),1])
            smooth_Midi_data = []
            index = omit_tap
            steps = int(math.ceil(omit_tap/10.0))
            while index <= len(Midi_data[omit_tap:-(omit_tap + 1),1]):
                smooth_Midi_data.append(sum(Midi_data[index:index + steps,1])/steps)
                index += steps
            print (len(Myo_fatigue_Frames1), len(smooth_Midi_data))
            #print (np.corrcoef(Myo_fatigue_Frames1, smooth_Midi_data)[0, 1])
            #print (np.corrcoef(Myo_fatigue_Frames2, smooth_Midi_data)[0, 1])
            #Frate_MIDI_write(FRATE_MIDI_OUTPUT_FIGNAME1, Myo_fatigue_Frames1, Midi_data[omit_tap : -(omit_tap*2) : int(math.ceil(omit_tap/10.0))])
            #Frate_MIDI_write(FRATE_MIDI_OUTPUT_FIGNAME2, Myo_fatigue_Frames2, Midi_data[omit_tap : -(omit_tap*2) : int(math.ceil(omit_tap/10.0))])
            Frate_MIDI_write(FRATE_MIDI_OUTPUT_FIGNAME1, Myo_fatigue_Frames1, smooth_Midi_data)
            Frate_MIDI_write(FRATE_MIDI_OUTPUT_FIGNAME2, Myo_fatigue_Frames2, smooth_Midi_data)

            #recurrence_f.write(str(a1) + "\t" + str(b1) + "\t" + str(max(MdPF_Frames1)) + "\t" + str(min(MdPF_Frames1)) + "\t" + str(sum(MdPF_Frames1)/len(MdPF_Frames1)) + "\t")
            #recurrence_f.write(str(a2) + "\t" + str(b2) + "\t" + str(max(MdPF_Frames2)) + "\t" + str(min(MdPF_Frames2)) + "\t" + str(sum(MdPF_Frames2)/len(MdPF_Frames2)) + "\n")

            f_times1, f_duration1 = Calc_fatigue_futuers(Myo_fatigue_Frames1)
            f_times2, f_duration2 = Calc_fatigue_futuers(Myo_fatigue_Frames2)

            fatigue_f.write(str(len(Myo_fatigue_Frames1)) + "\t" + str(f_times1) + "\t" + str(f_duration1) + "\t")
            fatigue_f.write(str(f_times2) + "\t" + str(f_duration2) + "\n")

            file_num += 1
        fatigue_f.write("\n")

        recurrence_f.close()
        ratio_f.close()
        sub_num += 1

    fatigue_f.close()
