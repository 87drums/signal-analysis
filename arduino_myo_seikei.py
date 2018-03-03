# -*- coding: utf-8 -*-
def decode_myo(data1, data2):
    d1 = int(data1) - 128
    d2 = int(data2)
    data = 0

    #正の値
    if d1 >= 64:
        d1 -= 64
        return d1 + d2
    #負の値
    else:
        return 0 - (d1 + d2)

def bytes2byte(myo_output_filename, file_num):
    for i in range(2):
        #Myoelectronical output
        content = open(myo_output_filename + "-" + str(i+1) + ".txt").read()
        Scontent = content.split("\n")

        Myo_getTime = float(Scontent[0]) #th_end_time - th_start_time #Myoelectronical's time while Myo get

        f = open(myo_output_filename + "-" + str(i+1) + "_trim.txt", "w")

        f.write(str(Myo_getTime)) #write time while Myo get
        f.write("\n")

        if int(Scontent[1]) >= 128:
            start = 1
        else:
            start = 2

        i = start
        while i <= len(Scontent) - start - 1:
            num = int(Scontent[i])
            if num >= 128:
                if num-128 < 64:
                    data = -(num - 128)
                else:
                    data = num - 128 - 64
                f.write(str(data))
                f.write("\n")
            else:
                pass

            i += 1
        f.close()

if __name__ == "__main__":
    MYO_OUTPUT_FILENAME = "../data/preexperiment/test/myo/myo_filetesttest" #myo file name head
    start_num = 1
    end_num = 1

    while start_num <= end_num:
        bytes2byte(MYO_OUTPUT_FILENAME, start_num)
        start_num += 1
