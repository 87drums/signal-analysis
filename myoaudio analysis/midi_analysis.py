# -*-coding:utf-8-*-
import csv
import numpy as np
import scipy as sp

Midi_filename = "../data/Midi_data/Midi_test.txt"
Midi_vdata = np.loadtxt(Midi_filename)
print Midi_vdata[7,1]
"""
#file read
Midi_f = open(Midi_filename, "r")
Midi_fdata = Midi_f.read()
Midi_f.close()

Midi_wdata = np.array(Midi_fdata.split()) #\n \t \s split to array

Midi_vdata = np.array([[]])
Midi_vdata = np.append(Midi_vdata, np.array([[1,2,3]]))
Midi_vdata = np.append(Midi_vdata, np.array([[1,2,3]]))

print Midi_vdata
"""
