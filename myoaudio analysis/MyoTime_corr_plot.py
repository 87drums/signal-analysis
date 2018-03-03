# --- coding:utf-8 ---
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

def MyoAudio_correl(Myo_analysis_filename, start_num, end_num):
    corr1_list = []
    corr2_list = []
    while start_num <= end_num:
        mf1 = np.loadtxt(Myo_analysis_filename + str(start_num) + "-1.txt") #median frequency
        mf2 = np.loadtxt(Myo_analysis_filename + str(start_num) + "-2.txt") #median frequency

        corr1_list.append(np.corrcoef(mf1, range(mf1.size))[0,1])
        corr2_list.append(np.corrcoef(mf2, range(mf2.size))[0,1])

        start_num += 1
    return corr1_list, corr2_list

if __name__ == "__main__" :
    subject_start = 1
    subject_end = 6

    corr1 = []
    corr2 = []
    corr1_list_ave = []
    corr2_list_ave = []

    while subject_start <= subject_end:
        filename_head = "../data/main experiment/" + str(subject_start) + "/analysis/"
        Myo_analysis_filename = filename_head + "myo_analysis"

        file_start = 1
        file_end = 6

        corr1_list, corr2_list = MyoAudio_correl(Myo_analysis_filename, file_start, file_end)

        corr1.append(corr1_list)
        corr2.append(corr2_list)
        corr1_list_ave.append(sum(corr1_list)/len(corr1_list))
        corr2_list_ave.append(sum(corr2_list)/len(corr2_list))

        print "finish subject " + str(subject_start)

        subject_start += 1

    corr_filename_head = "../data/main experiment/figure/"
    myo1_plot_filename = corr_filename_head + "myo_time_corr1.eps"
    myo2_plot_filename = corr_filename_head + "myo_time_corr2.eps"

    color = ["c","g","k","y","r","b"]

    fig = plt.figure()
    ax = fig.add_subplot(111)
    for index in range(6):
        bp = ax.plot(corr1[index], [index + 1] * 6, color[index] + ".", ms=15)
        bp += ax.plot(corr1_list_ave[index], [index + 1], color[index] + "*", ms=15)
    fp = FontProperties(fname=r'C:\WINDOWS\Fonts\YuGothic.ttf', size=14)
    plt.grid()
    plt.xlabel("相関係数", fontproperties = fp)
    plt.ylabel("被験者", fontproperties = fp)
    plt.xlim([-1, 1])
    plt.ylim([0, 7])
    plt.savefig(myo1_plot_filename)

    fig = plt.figure()
    ax = fig.add_subplot(111)
    for index in range(6):
        bp = ax.plot(corr2[index], [index+1] * 6, color[index] + ".", ms=15)
        bp += ax.plot(corr2_list_ave[index], [index + 1], color[index] + "*", ms=15)
    fp = FontProperties(fname=r'C:\WINDOWS\Fonts\YuGothic.ttf', size=14)
    plt.grid()
    plt.xlabel("相関係数", fontproperties = fp)
    plt.ylabel("被験者", fontproperties = fp)
    plt.xlim([-1, 1])
    plt.ylim([0, 7])
    plt.savefig(myo2_plot_filename)
