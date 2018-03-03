# -*- coding:utf-8 -*-
import numpy as np
import re

def tired_search(Onset_filename, tired_filename, analysis_filename, file_num, file_end):
    while file_num <= file_end:
        onset_content = np.loadtxt(Onset_filename + str(file_num) + "_trim.txt")
        tired_content = re.split('\n|,', open(tired_filename + str(file_num) + ".txt", "r").read())

        f = open(analysis_filename + str(file_num) +".txt", "w")

        if len(tired_content) >= 1:
            for i, row in enumerate(tired_content):
                for j in range(onset_content.size - 2):
                    if onset_content[j] < row <= onset_content[j+1]:
                        print "text"
                        f.write(str(j))
                        f.write(",")
                        break

        file_num += 1

if __name__ == "__main__":
    file_start = 1
    file_end = 6

    subject_start = 1
    subject_end = 6

    while subject_start <= subject_end:
        filename_head = "../data/main experiment/" + str(subject_start) + "/"
        Onset_filename = filename_head + "analysis/onset_"
        tired_filename = filename_head + "tired/tired_file"
        analysis_filename = filename_head + "analysis/tired_hit"

        tired_search(Onset_filename, tired_filename, analysis_filename, file_start, file_end)

        print "finish subject " + str(subject_start)

        subject_start += 1
