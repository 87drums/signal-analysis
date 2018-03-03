# -*-coding:utf-8-*-
import matplotlib as mpl
import matplotlib.pyplot as plt
import pylab
from matplotlib.font_manager import FontProperties
import numpy as np

def get_plot_list(iti_f, vel_f, start_num, end_num):
    iti_list = []
    vel_list = []
    iti_std_list = []
    vel_std_list = []

    while start_num <= end_num:
        text_i = np.loadtxt(iti_f + str(start_num) + ".txt")
        text_v = np.loadtxt(vel_f + str(start_num) + ".txt")

        iti_list.append(np.mean(text_i)) #ITI平均
        iti_std_list.append(np.std(text_i)) #ITI標準偏差

        vel_list.append(np.mean(text_v)) #振幅平均
        vel_std_list.append(np.std(text_v)) #振幅標準偏差

        start_num += 1
    return iti_list, iti_std_list, vel_list, vel_std_list

if __name__ == "__main__":
    file_start = 1
    file_end = 6

    subject_start = 1
    subject_end = 6

    while subject_start <= subject_end:
        filename_head = "../data/main experiment/" + str(subject_start) + "/analysis/"
        iti_filename = filename_head + "Audio_interval_analysis"
        vel_filename = filename_head + "Audio_velocity_max_analysis"
        iti_plot_filename = "../data/main experiment/figure/ITI_plot" + str(subject_start) + ".png"
        vel_plot_filename = "../data/main experiment/figure/VEL_plot" + str(subject_start) + ".png"

        iti, iti_std, vel, vel_std = get_plot_list(iti_filename, vel_filename, file_start, file_end)

        x_list = range(7)[1:]
        """
        pylab.plot(x_list, iti)
        pylab.errorvar(x_list, iti, iti_std,fmt = "o")
        fp = FontProperties(fname=r'C:\WINDOWS\Fonts\YuGothic.ttf', size=14)
        ax.set_xticklabels(["1", "2", "3", "4", "5", "6"], fontproperties = fp)
        plt.grid()
        plt.xlabel("試行", fontproperties = fp)
        plt.ylabel("Median Power Frequency", fontproperties = fp)
        plt.ylim([0,350])
        """

        fig = plt.figure()
        ax = fig.add_subplot(111)
        bp = ax.plot(x_list, iti)
        plt.errorbar(x_list, iti, yerr = iti_std,fmt = "o")
        fp = FontProperties(fname=r'C:\WINDOWS\Fonts\YuGothic.ttf', size=14)
        plt.grid()
        plt.xlabel("試行", fontproperties = fp)
        plt.ylabel("Inter-Tap Interval[sec]", fontproperties = fp)
        plt.xlim([0, 7])
        plt.ylim([0.22, 0.28])
        plt.savefig(iti_plot_filename)

        fig = plt.figure()
        ax = fig.add_subplot(111)
        bp = ax.plot(x_list, vel)
        plt.errorbar(x_list, vel, yerr = vel_std,fmt = "o")
        fp = FontProperties(fname=r'C:\WINDOWS\Fonts\YuGothic.ttf', size=14)
        plt.grid()
        plt.xlabel("試行", fontproperties = fp)
        plt.ylabel("Amplitude", fontproperties = fp)
        plt.xlim([0, 7])
        plt.ylim([0, 1])
        plt.savefig(vel_plot_filename)

        print "finished subject " + str(subject_start)

        subject_start += 1
