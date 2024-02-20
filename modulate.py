import numpy
from math import pi
from matplotlib import pyplot
from constants import *

def bytes_to_bin(msg: bytes):
    """
    take msg (bytes) and turn it into binary
    I'm gonna use a string of 1s and 0s
    because it is the easiest to do when you are
    decoding the bytes in python
    """
    msg_binary = ""
    for byte in msg:
        byte_binary = bin(byte)
        # this pad the byte to proper length
        byte_binary += "0" * (8 - len(byte_binary))
        msg_binary += byte_binary
    return msg_binary

def bytes_to_sig(msg: str, s0: numpy.ndarray,s1:numpy.ndarray):
    """
    Take the bytes msg and make it into an fsk sig according to s0,s1
    """
    msg_binary = bytes_to_bin(msg)
    signal = numpy.empty(0)
    
    for bit in msg_binary:
        if bit == "1":
            signal = numpy.concatenate((signal,s1))
        if bit == "0":
            signal = numpy.concatenate((signal,s0))
    return signal






def main():
    samples_per_baud = Fs // Fb

    f0_periods_per_baud = F0 / Fs * samples_per_baud
    print(f0_periods_per_baud)

    baud_index = numpy.arange(0,samples_per_baud)

    s0 = numpy.cos(2 * pi * F0 / Fs * baud_index)
    s1 = numpy.cos(2 * pi * F1 / Fs * baud_index)

    msg = b"Q"
    signal = bytes_to_sig(msg,s0,s1)
    pyplot.plot(s0)
    pyplot.plot(s1)
    pyplot.plot(signal)

    pyplot.show()

if __name__ == "__main__":
    main()