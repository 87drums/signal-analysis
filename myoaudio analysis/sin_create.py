# -*- coding: utf-8 -*-

import wave
import numpy as np
from matplotlib import pylab as plt
import struct

a = 1     #振幅
fs = 1000 #サンプリング周波数
f0 = 440  #周波数
sec = 5   #秒

swav=[]

for n in np.arange(fs * sec):
    #サイン波を生成
    s = a * np.sin(2.0 * np.pi * f0 * n / fs)
    swav.append(s)

#Myoelectronical output
f = open("sine440.txt", "w")

for row in swav:
    f.write(str(row)) #外れ値削除しファイルに書き込み""".translate(None, "・")"""
    f.write("\n")
f.close()
