import numpy
from math import pi
from matplotlib import pyplot
from constants import *

def bytes_to_bin(msg: str):
    """
    take msg (bytes) and turn it into binary
    I'm gonna use a string of 1s and 0s
    because it is the easiest to do when you are
    decoding the bytes in python
    """
    msg_binary = ""
    for char in msg:
        char_binary = bin(ord(char))[2:]
        # this pad the byte to proper length
        char_binary = "0" * (char_length - len(char_binary)) + char_binary
        msg_binary += char_binary
    return msg_binary

def bytes_to_sig(msg: str, s0: numpy.ndarray,s1:numpy.ndarray):
    """
    Take the bytes msg and make it into an fsk sig according to s0,s1
    """
    msg_binary = bytes_to_bin(msg)
    # insert preamble
    msg_binary = preamble + msg_binary
    signal = numpy.empty(0)
    
    for bit in msg_binary:
        if bit == "1":
            signal = numpy.concatenate((signal,s1))
        if bit == "0":
            signal = numpy.concatenate((signal,s0))
    return signal






def main():

    msg = "Q"
    signal = bytes_to_sig(msg,s0,s1)
    fig, (spectrogram,sigplot,plot0,plot1) = pyplot.subplots(nrows=4)
    spectrogram.set_ylabel("FFT of modulated signal")
    spectrogram.specgram(signal,NFFT=256,Fs=Fs,noverlap=32)
    sigplot.plot(signal)
    sigplot.set_ylabel("Signal")
    plot0.set_ylabel("0 tone")
    plot0.plot(s0)
    plot1.set_ylabel("1 tone")
    plot1.plot(s1)
    pyplot.show()

if __name__ == "__main__":
    main()