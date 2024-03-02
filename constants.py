import numpy
from math import pi
# Audio stuff
CHANNELS=1
FORMAT="float64"
NP_FORMAT=numpy.float64

M=1
Fs = 44100 # samples per second
Fb = 10  # bauds/sec
F0 = 1000
F1 = M*Fb+F0

preamble = "10" * 5
char_length = 7 # I included this in case I want to change from ascii encoding
# NOT CONSTANTS
samples_per_baud = Fs // Fb
baud_index = numpy.arange(0,samples_per_baud,dtype=NP_FORMAT)
s0 = numpy.cos(2 * pi * F0 / Fs * baud_index)
s1 = numpy.cos(2 * pi * F1 / Fs * baud_index)
# hamming window
window = numpy.hamming(len(s0))
window = window.astype(NP_FORMAT)
s0 = window * s0
s1 = window * s1

if __name__ == "__main__":
    print(M)
    from matplotlib import pyplot

    fig, (s0plot,window,s1plot) = pyplot.subplots(nrows=3)
    s0plot.plot(s0,label="s0")
    window.plot(numpy.hamming(len(s0)),label="Hammed window")
    s1plot.plot(s1,label="s1")
    pyplot.show()