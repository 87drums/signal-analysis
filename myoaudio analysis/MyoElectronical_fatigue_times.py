# -*-coding:utf-8-*-
import numpy as np

def fatigue_sum(myo_filename, out_f, start_num, end_num):
    f = open(out_f + ".txt", "w")
    while start_num <= end_num:
        for index in range(2):
            fatigue_count = 0
            myo_content = np.loadtxt(myo_filename + str(start_num) + "-" + str(index + 1) + ".txt")

            for i in range(len(myo_content)-1):
                if (myo_content[i+1] - myo_content[i]) < 0:
                    fatigue_count += 1

            f.write(str((fatigue_count / (myo_content.size - 1.0)) * 100)) #str(start_num) + "-" + str(index + 1) + " : " + str(fatigue_count)
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
        myo_filename = filename_head + "myo_analysis"
        analysis_filename = filename_head + "MyoE_fatigue_times" + str(subject_start)

        fatigue_sum(myo_filename, analysis_filename, file_start, file_end)

        print "finished subject " + str(subject_start)

        subject_start += 1
