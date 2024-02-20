import numpy
from math import pi
F0 = 440
F1 = 620
Fs = 8000 # samples per second
Fb = 8    # bauds per second

# NOT CONSTANTS
samples_per_baud = Fs // Fb

baud_index = numpy.arange(0,samples_per_baud)

s0 = numpy.cos(2 * pi * F0 / Fs * baud_index)
s1 = numpy.cos(2 * pi * F1 / Fs * baud_index)