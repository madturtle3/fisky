import numpy
from math import pi
F0 = 440
F1 = 650
Fs = 8000 # samples per second
Fb = 5    # bauds per second

preamble = "10" * 5
char_length = 7 # I included this in case I want to change from ascii encoding
# NOT CONSTANTS
samples_per_baud = Fs // Fb

baud_index = numpy.arange(0,samples_per_baud)

s0 = numpy.cos(2 * pi * F0 / Fs * baud_index)
s1 = numpy.cos(2 * pi * F1 / Fs * baud_index)