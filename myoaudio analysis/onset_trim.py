# -*- coding:utf-8 -*-
import numpy as np

def trim_onset(filename_head, file_num, end_num):
    while file_num <= end_num:
        content = open(filename_head + str(file_num) + ".txt").read().split("\n")

        f = open(filename_head + str(file_num) + "_trim.txt", "w")

        for row in content:
            if row.find("d") <= -1:
                f.write(row)
                f.write("\n")

        file_num += 1

if __name__ == "__main__":
    filename_head = "../data/main experiment/6/analysis/onset_"
    start_num = 1
    end_num = 6

    trim_onset(filename_head, start_num, end_num)
