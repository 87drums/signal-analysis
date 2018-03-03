# -*-coding:utf-8 -*-
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import numpy as np

def box_plot(myo_filename, start_num, file_end, subject_num):
    file_num = start_num

    for index in range(2):
        file_num = start_num
        box_list = []
        while file_num <= file_end:
            #print "subject " + str(subject_num) + " = file" + str(file_num) + "-" + str(index + 1)
            file_content = open(myo_filename + str(file_num) + "-" + str(index + 1) + ".txt", "r").read().split("\n")#np.loadtxt(myo_filename + str(file_num) + "-" + str(index + 1) + ".txt")
            box_list.append(map(float, file_content[:len(file_content)-2]))

            file_num += 1
        fig = plt.figure()
        ax = fig.add_subplot(111)
        bp = ax.boxplot(box_list)

        max_list_index = box_list.index(max(box_list))
        max_index = box_list[max_list_index].index(max(box_list[max_list_index]))
        max_num = box_list[max_list_index][max_index]

        min_list_index = box_list.index(min(box_list))
        min_index = box_list[min_list_index].index(min(box_list[min_list_index]))
        min_num = box_list[min_list_index][min_index]

        fp = FontProperties(fname=r'C:\WINDOWS\Fonts\YuGothic.ttf', size=14)
        ax.set_xticklabels(["1", "2", "3", "4", "5", "6"], fontproperties = fp)
        plt.grid()
        plt.xlabel("試行", fontproperties = fp)
        plt.ylabel("Median Power Frequency", fontproperties = fp)
        plt.ylim(min_num-10, max_num+10)
        output_filename = "../data/main experiment/figure/test/MdPF_box_plot"
        if (index + 1) <= 1:
            plt.title("被験者" + str(subject_num) + "伸筋", fontproperties = fp)
            plt.savefig(output_filename + str(subject_num) + "_1.eps")
        else:
            plt.title("被験者" + str(subject_num) + "屈筋", fontproperties = fp)
            plt.savefig(output_filename + str(subject_num) + "_2.eps")

if __name__ == "__main__":
    file_start = 1
    file_end = 6

    subject_start = 1
    subject_end = 6

    while subject_start <= subject_end:
        filename_head = "../data/main experiment/" + str(subject_start) + "/analysis/"
        MYO_MdPF_FILENAME = filename_head + "myo_analysis"

        box_plot(MYO_MdPF_FILENAME, file_start, file_end, subject_start)

        print "finish subject " + str(subject_start)

        subject_start += 1
