# -*- coding:utf-8 -*-

"""
テキストファイル読み込み
一列目に時間　時分は:，秒数のコンマ以下は.で区切られるような時間表記限定(labchart表記)
一行目にファイルの記録にかかった秒数，二行目以降にデータを記述したテキスト吐き出し
"""

import numpy as np
import re

def file_write(OUTPUT_FILENAME, Frames):
    f = open(OUTPUT_FILENAME, "w")

    f.write(str(Frames[0])) #write time while Myo get
    f.write("\n")
    for row in Frames[1:]:
        if type(row) == float:
            data = row
        else:
            data = float(row)

        f.write(str(data))
        f.write("\n")

    f.close()

def trim_myo(filename):
    content = np.loadtxt(filename + ".txt", dtype = "str")

    time_str = content[:,0][len(content[:,0])-1]

    if re.search(":", time_str):
        time_str_split = time_str.split(":")
        time = 0.0
        max_num = len(time_str_split)
        for i in range(max_num):
            time += float(time_str_split[i]) * np.power(60, (max_num - 1) - i)
    else:
        time = float(time_str)

    rows, cols = content.shape

    for i in range(cols - 1):
        mus = np.array([])
        mus = np.append(mus, content[:,i + 1])
        mus = np.insert(mus, 0, str(time))
        print mus
        file_write(filename + "_trim" + str(i + 1) + ".txt", mus)

if __name__ == "__main__":
    filename = "../data/preexperiment/20170622 myo_pre/myo/myoware"

    content = trim_myo(filename)
