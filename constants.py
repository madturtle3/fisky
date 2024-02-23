import numpy
from math import pi
M=1
Fs = 2000 # samples per second
Fb = 100  # bauds/sec
F0 = 500
F1 = M*Fb+F0

preamble = "10" * 5
char_length = 7 # I included this in case I want to change from ascii encoding
# NOT CONSTANTS
samples_per_baud = Fs // Fb
baud_index = numpy.arange(0,samples_per_baud)

s0 = numpy.cos(2 * pi * F0 / Fs * baud_index)
s1 = numpy.cos(2 * pi * F1 / Fs * baud_index)

# hamming window
s0 = numpy.hamming(len(s0)) * s0
s1 = numpy.hamming(len(s1)) * s1

if __name__ == "__main__":
    print(M)
    from matplotlib import pyplot

    fig, (s0plot,window,s1plot) = pyplot.subplots(nrows=3)
    s0plot.plot(s0,label="s0")
    window.plot(numpy.hamming(len(s0)),label="Hammed window")
    s1plot.plot(s1,label="s1")
    pyplot.show()