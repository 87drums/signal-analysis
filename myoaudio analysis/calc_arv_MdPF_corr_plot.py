# -*-coding:utf-8 -*-
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import numpy as np
import struct
#import cv2
from PIL import Image

#output figure extension
fig_extension = "png"

def coor_shape(file_num, index, corr_filename, subject_num, output_filename):
    corr_file = open(corr_filename + str(file_num) + "-" + str(index + 1) + ".txt", "r")
    file_content = corr_file.read().split("\n")
    corr_list = np.array(file_content[:len(file_content)-1]).astype(np.float64)

    plt.plot(np.arange(len(corr_list)), corr_list, color = "r")

    fp = FontProperties(fname=r'C:\WINDOWS\Fonts\NotoSansCJKjp-Regular.otf', size=14)
    plt.grid()
    plt.minorticks_on()
    plt.xlabel(u"時間[sec]", fontproperties = fp)
    plt.ylabel(u"相関係数", fontproperties = fp)

    if corr_list.size >= 80:
        plt.xlim(0, 350)
    else:
        plt.xlim(0, 70)
    plt.ylim(-1, 1)

    if (index + 1) <= 1:
        plt.title(u"被験者" + str(subject_num) + u"試行" + str(file_num) + u"伸筋 疲労度", fontproperties = fp)
        plt.savefig(output_filename + str(file_num) + "_1." + fig_extension, transparent=True)
    else:
        plt.title(u"被験者" + str(subject_num) + u"試行" + str(file_num) + u"屈筋 疲労度", fontproperties = fp)
        plt.savefig(output_filename + str(file_num) + "_2." + fig_extension, transparent=True)
    plt.close()
    corr_file.close()

def wav_shape(myo_filename, file_num, index, subject_num, output_filename):
    Myo_f = open(myo_filename + str(file_num) + "-" + str(index + 1) + ".txt", "r")#"_trim.txt", "r")
    Myo_fdata = Myo_f.read()
    Myo_f.close()

    Myo_wdata = np.array(Myo_fdata.split()) #\n \t \s split to array
    data = Myo_wdata.astype(np.float64) #strings 2 float
    plt.plot(np.arange(len(data)), data, color = "b")

    fp = FontProperties(fname=r'C:\WINDOWS\Fonts\NotoSansCJKjp-Regular.otf', size=14)
    plt.grid()
    plt.minorticks_on()
    plt.xlabel(u"時間[sec]", fontproperties = fp)
    plt.ylabel(u"振幅", fontproperties = fp)

    if data.size >= 80:
        plt.xlim(0, 350)
    else:
        plt.xlim(0, 70)

    if (index + 1) <= 1:
        plt.title(u"被験者" + str(subject_num) + u"試行" + str(file_num) + u"伸筋 筋電位信号", fontproperties = fp)
        plt.savefig(output_filename + str(file_num) + "_1." + fig_extension, transparent=True)
    else:
        plt.title(u"被験者" + str(subject_num) + u"試行" + str(file_num) + u"屈筋 筋電位信号", fontproperties = fp)
        plt.savefig(output_filename + str(file_num) + "_2." + fig_extension, transparent=True)

    plt.close()

def images_conbined(filename1, filename2, file_num, index, output_filename):
    layer1 = Image.open(filename1 + str(file_num) + "_" + str(index + 1) + "." + fig_extension)
    layer2 = Image.open(filename2 + str(file_num) + "_" + str(index + 1) + "." + fig_extension)

    # layer1と同じ大きさの画像を全面透過で作成
    c = Image.new('RGBA', layer1.size, (255, 255,255, 0))
    c.paste(layer2, (0,0), layer2)
    result = Image.alpha_composite(layer1, c)
    result.save(output_filename + str(file_num) + "_" + str(index + 1) + "." + fig_extension)

def fill_target_range(myo_filename, file_num, index, corr_filename, subject_num, output_filename):
    #筋電データ読み込み
    Myo_f = open(myo_filename + str(file_num) + "-" + str(index + 1) + ".txt", "r")#"_trim.txt", "r")
    Myo_fdata = Myo_f.read()
    Myo_f.close()

    Myo_wdata = np.array(Myo_fdata.split()) #\n \t \s split to array
    data = Myo_wdata.astype(np.float64) #strings 2 float

    #相関係数データ読み込み
    corr_file = open(corr_filename + str(file_num) + "-" + str(index + 1) + ".txt", "r")
    file_content = corr_file.read().split("\n")
    corr_list = np.array(file_content[:len(file_content)-1]).astype(np.float64)

    comp1_list = []
    comp2_list = []
    for i in range(data.size - 2):
        comp1 = corr_list[i + 1] - corr_list[i] #comp:comparison（比較）の略
        comp2 = data[i + 1] - data[i]

        #in case of comp1 is 0, comp1 define 1(positive value) because I seen the subject suppress fatigue.
        if comp1 == 0:
            comp1 = 1
        #in case of comp2 is 0, comp2 define 1(positive value) because I seen decrease shape of signals when normal case.
        if comp2 == 0:
            comp2 = 1

        comp1_list.append(comp1)
        comp2_list.append(comp2)

    #筋電位信号が小さくなったタイミング黄色
    i = 0
    while i < len(comp1_list) - 1:
        x_section = []
        y_section = []
        #if """comp1_list[i] < 0 and""" comp2_list[i] > 0:
        if comp2_list[i] < 0:
            #左端のx軸値指定
            x_section.append(i)
            #右端のx軸探索
            #while ("""comp1_list[i + 1] < 0 and""" comp2_list[i + 1] > 0) and (i < len(comp1_list) - 2):
            while (comp2_list[i + 1] < 0) and (i < len(comp2_list) - 2):
                i += 1
            x_section.append(i + 1)
            x_section.append(i + 1)
            x_section.append(x_section[0])
            y_section.append(0)
            y_section.append(0)
            y_section.append(1)
            y_section.append(1)
            plt.fill(x_section, y_section, color = "y", alpha = 1)
        i += 1

    #負の相関区間（疲労回復区間）赤色で塗りつぶし
    """i = 0
    while i < len(comp1_list) - 1:
        x_section = []
        y_section = []
        if comp1_list[i] > 0 and comp2_list[i] < 0:
            #左端のx軸値指定
            x_section.append(i)
            #右端のx軸探索
            while (comp1_list[i + 1] > 0 and comp2_list[i + 1] < 0) and (i < len(comp1_list) - 2):
                i += 1
            x_section.append(i + 1)
            x_section.append(i + 1)
            x_section.append(x_section[0])
            y_section.append(0)
            y_section.append(0)
            y_section.append(1)
            y_section.append(1)
            plt.fill(x_section, y_section, color = "y", alpha = 1)
        i += 1"""

    fp = FontProperties(fname=r'C:\WINDOWS\Fonts\NotoSansCJKjp-Regular.otf', size=14)
    plt.grid()
    plt.minorticks_on()
    plt.xlabel(u"時間[sec]", fontproperties = fp)
    plt.ylabel(" ", fontproperties = fp)

    if data.size >= 80:
        plt.xlim(0, 350)
    else:
        plt.xlim(0, 70)

    if (index + 1) <= 1:
        plt.title(u"被験者" + str(subject_num) + u"試行" + str(file_num) + u"伸筋 負の相関区間", fontproperties = fp)
        plt.savefig(output_filename + str(file_num) + "_1." + fig_extension)#, transparent=True)
    else:
        plt.title(u"被験者" + str(subject_num) + u"試行" + str(file_num) + u"屈筋 負の相関区間", fontproperties = fp)
        plt.savefig(output_filename + str(file_num) + "_2." + fig_extension)#, transparent=True)

    plt.close()

def vel_shape(vel_filename, file_num, index, subject_num, output_filename):
    vel_f = open(vel_filename + str(file_num) + ".txt", "r")
    vel_fdata = vel_f.read()
    vel_f.close()

    vel_wdata = np.array(vel_fdata.split()) #\n \t \s split to array
    data = vel_wdata.astype(np.float64) #strings 2 float
    plt.plot(np.arange(len(data)), data, color = "b")

    fp = FontProperties(fname=r'C:\WINDOWS\Fonts\NotoSansCJKjp-Regular.otf', size=14)
    plt.grid()
    plt.minorticks_on()
    plt.xlabel(u"時間[sec]", fontproperties = fp)
    plt.ylabel(u"振幅", fontproperties = fp)
    if data.size >= 280:
        plt.xlim(0, 1400)
    else:
        plt.xlim(0, 280)

    plt.title(u"被験者" + str(subject_num) + u"試行" + str(file_num) + u"音量推移", fontproperties = fp)
    plt.savefig(output_filename + str(file_num) + "." + fig_extension, transparent=True)

    plt.close()

def images_conbined2(filename1, filename2, file_num, index, output_filename):
    layer1 = Image.open(filename1 + str(file_num) + "_" + str(index + 1) + "." + fig_extension)
    layer2 = Image.open(filename2 + str(file_num) + "." + fig_extension)

    # layer1と同じ大きさの画像を全面透過で作成
    c = Image.new('RGBA', layer1.size, (255, 255,255, 0))
    c.paste(layer2, (0,0), layer2)
    result = Image.alpha_composite(layer1, c)
    result.save(output_filename + str(file_num) + "_" + str(index + 1) + "." + fig_extension)

def adapt_plot(corr_filename, myo_filename, vel_filename, start_num, file_end, subject_num):
    file_num = start_num
    output_filename1 = "../data/main experiment/figure/" + fig_extension + "/arv_MdPF_corr_plot/" + str(subject_num) + "arv_MdPF_corr_plot"
    output_filename2 = "../data/main experiment/figure/" + fig_extension + "/myo_waveshape/" + str(subject_num) + "myo_waveshape"
    output_filename3 = "../data/main experiment/figure/" + fig_extension + "/corr_wave_conbine/" + str(subject_num) + "corr_wave_conbine"
    output_filename4 = "../data/main experiment/figure/" + fig_extension + "/negative_corr_section/" + str(subject_num) + "negative_corr_section"
    output_filename5 = "../data/main experiment/figure/" + fig_extension + "/ncs_cwc_conbine/" + str(subject_num) + "ncs_cwc_conbine"
    output_filename6 = "../data/main experiment/figure/" + fig_extension + "/velshape/" + str(subject_num) + "velshape"
    output_filename7 = "../data/main experiment/figure/" + fig_extension + "/ncs_vs_conbine/" + str(subject_num) + "ncs_vs_conbine"

    for index in range(2):
        file_num = start_num
        while file_num <= file_end:
            #corr shape書き出し
            coor_shape(file_num, index, corr_filename, subject_num, output_filename1)

            #wav shape書き出し
            wav_shape(myo_filename, file_num, index, subject_num, output_filename2)

            #images combined
            images_conbined(output_filename1, output_filename2, file_num, index, output_filename3)

            #fill target range
            fill_target_range(myo_filename, file_num, index, corr_filename, subject_num, output_filename4)

            #conbine negative corr section & corr wave corr_wave_conbine
            filename1 = output_filename4
            filename2 = output_filename3
            output_filename = output_filename5
            images_conbined(filename1, filename2, file_num, index, output_filename)

            #velocity shape書き出し
            if index <= 0:
                vel_shape(vel_filename, file_num, index, subject_num, output_filename6)
                images_conbined2(output_filename4, output_filename6, file_num, index, output_filename7)

            file_num += 1

if __name__ == "__main__":
    file_start = 1
    file_end = 6

    subject_start = 1
    subject_end = 6

    while subject_start <= subject_end:
        filename_head = "../data/main experiment/" + str(subject_start) + "/"
        MYO_FILENAME = filename_head + "analysis/myo_calc_arv_smooth" #"myo/myo_file"
        CORR_FILENAME = filename_head + "analysis/myo_calc_arv_MdPF_corr"
        VEL_FILENAME = filename_head + "analysis/Audio_velocity_max_analysis"

        adapt_plot(CORR_FILENAME, MYO_FILENAME, VEL_FILENAME, file_start, file_end, subject_start)

        print "finish subject " + str(subject_start)

        subject_start += 1
