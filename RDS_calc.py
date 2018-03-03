# -*- coding:utf-8 -*-
import numpy as np

def RDS_calc(myo_filename, file_num, end_num):
    while file_num <= end_num:
        #file read
        filename = myo_filename + str(file_num) + "-"

        Myo_data1 = open(filename + "1_trim.txt", "r").read().split("\n")
        Myo_data2 = open(filename + "2_trim.txt", "r").read().split("\n")

        Myo_data1_a = []
        Myo_data2_a = []
        for x in range(len(Myo_data1)-1):
            Myo_data1_a.append(float(Myo_data1[x].split(",")[1]))
            Myo_data2_a.append(float(Myo_data2[x].split(",")[1]))

        num = 10.0 #移動平均の個数
        b = np.ones(num)/num #重み決定，今回は等価

        Myo_data1_sma = np.convolve(np.array(Myo_data1_a), b, mode = 'valid')
        Myo_data2_sma = np.convolve(np.array(Myo_data2_a), b, mode = 'valid')

        f = open(filename + "_trim_rds.txt", "w")

        for i in range(Myo_data1_sma.size):
            rds = (Myo_data2_sma[i] - Myo_data1_sma[i]) / (Myo_data2_sma[i] + Myo_data1_sma[i]) #移動平均後なら~~_sma，前なら~~_a
            f.write(str(rds))
            f.write("\n")

        file_num += 1

if __name__ == "__main__":
    subject = "test"
    Myo_filename = "../data/preexperiment/" + subject + "/myo/myo_file"

    start_num = 1
    end_num = 1

    RDS_calc(Myo_filename, start_num, end_num)
