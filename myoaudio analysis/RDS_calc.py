# -*- coding:utf-8 -*-
import numpy as np
from matplotlib import pyplot as plt

def RDS_output(file_head, num):
    Myo_data1 = np.loadtxt(file_head + "myo/myo_file" + str(num) + "-1.txt")
    Myo_data2 = np.loadtxt(file_head + "myo/myo_file" + str(num) + "-2.txt")

    rate = int(Myo_data1.size // Myo_data1[0])

    MM = np.ones(int(rate * 0.009))/int(rate * 0.009)

    Myo_data1_ave = np.convolve(np.absolute(Myo_data1), MM, "valid")
    Myo_data2_ave = np.convolve(np.absolute(Myo_data2), MM, "valid")

    Myo_RDS = (Myo_data1_ave - Myo_data2_ave)/(Myo_data1_ave + Myo_data2_ave)

    text_f = open(file_head + "analysis/RDS_calc" + str(num) + ".txt", "w")

    for row in Myo_RDS:
        text_f.write(str(row))
        text_f.write("\n")

    text_f.close()

    """
    plt.plot(Myo_RDS)
    plt.show()
    """

if __name__ == "__main__":
    start_num = 2
    end_num = 7
    file_head = "../data/20161225/4/"

    while start_num <= end_num:
        RDS_output(file_head, start_num)
        start_num += 1
