# -*-coding:utf-8-*-
import numpy as np

def mid_calc(iti_f, vel_f, out_f, start_num, end_num):
    text_calc = open(out_f, "w")
    while start_num <= end_num:
        text_i = np.loadtxt(iti_f + str(start_num) + ".txt")
        text_v = np.loadtxt(vel_f + str(start_num) + ".txt")

        text_calc.write(str(np.mean(text_i)) + "\t") #ITI平均
        text_calc.write(str(np.std(text_i)) + "\t") #ITI標準偏差
        text_calc.write(str(np.var(text_i)) + "\t") #ITI分散
        text_calc.write(str(np.mean(text_v)) + "\t") #振幅平均
        text_calc.write(str(np.std(text_v)) + "\t") #振幅標準偏差
        text_calc.write(str(np.var(text_v)) + "\n") #振幅分散
        """
        text_calc.write(str(np.median(text_i))) #ITI中央値
        text_calc.write("(平均値：" + str(np.mean(text_i)) + ")")
        text_calc.write("±" + str(np.max(text_i) - np.median(text_i)))
        text_calc.write("(標準偏差：" + str(np.std(text_i)) + ")")
        text_calc.write("(分散：" + str(np.var(text_i)) + ")")
        text_calc.write(",") #区切り
        text_calc.write(str(np.median(text_v))) #velocity中央値
        text_calc.write("(平均値：" + str(np.mean(text_v)) + ")")
        text_calc.write("±" + str(np.max(text_v) - np.median(text_v)))
        text_calc.write("(標準偏差：" + str(np.std(text_v)) + ")")
        text_calc.write("(分散：" + str(np.var(text_i)) + ")")
        text_calc.write("\n")
        """

        start_num += 1
    text_calc.close()

if __name__ == "__main__":
    file_start = 1
    file_end = 6

    subject_start = 1
    subject_end = 6

    while subject_start <= subject_end:
        filename_head = "../data/main experiment/" + str(subject_start) + "/analysis/"
        iti_filename = filename_head + "Audio_interval_analysis"
        vel_filename = filename_head + "Audio_velocity_max_analysis"
        analysis_filename = filename_head + "ITI_VEL_mid.txt"

        mid_calc(iti_filename, vel_filename, analysis_filename, file_start, file_end)

        print "finished subject " + str(subject_start)

        subject_start += 1
