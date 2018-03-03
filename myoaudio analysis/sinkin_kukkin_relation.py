# -*-coding:utf-8-*-
import numpy as np

def cor_calc(in_f, out_f, start_num, end_num):
    f = open(out_f, "w")
    while start_num <= end_num:
        s_myo = np.loadtxt(in_f + str(start_num) + ".txt")#np.loadtxt(in_f + str(start_num) + "-1.txt")#.astype(np.float64)#open(in_f + str(start_num) + "-1.txt").read().split("\n")
        k_myo = np.arange(s_myo.size)#np.loadtxt(in_f + str(start_num) + "-2.txt")#.astype(np.float64)#open(in_f + str(start_num) + "-2.txt").read().split("\n")

        f.write(str(np.corrcoef(s_myo, k_myo)[0, 1]))
        f.write("\n")

        start_num += 1
    f.close()

if __name__ == "__main__":
    file_start = 1
    file_end = 6

    subject_start = 1
    subject_end = 6

    while subject_start <= subject_end:
        filename_head = "../data/main experiment/" + str(subject_start) + "/analysis/"
        input_filename = filename_head + "Audio_velocity_max_analysis"#"myo_analysis"
        analysis_filename = filename_head + "audio_time_correl.txt"

        cor_calc(input_filename, analysis_filename, file_start, file_end)

        print "finished subject " + str(subject_start)

        subject_start += 1
