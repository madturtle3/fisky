from constants import *
import numpy
import modulate
from matplotlib import pyplot

def baud_picker(correlate0:numpy.ndarray, correlate1:numpy.ndarray, samples_per_baud:int):
    """
    this takes the signal given and turns it into a string of 1s and 0s
    correlate0 and correlate 1 being the correlation of the high and low
    bauds with the graph
    """
    picked_bauds = ""
    for index in numpy.arange(len(correlate1)-samples_per_baud,step=samples_per_baud):
        max0 = max(correlate0[index:index+samples_per_baud])
        max1 = max(correlate1[index:index+samples_per_baud])
        if max1 > max0:
            picked_bauds += "1"
        elif max0 > max1:
            picked_bauds += "0"
    return picked_bauds

        


def main():
    msg = b"hello"
    signal = modulate.bytes_to_sig(msg,s0,s1)

    correlate0 = numpy.correlate(signal,s0)
    correlate1 = numpy.correlate(signal,s1)

    binary_msg = baud_picker(correlate0,correlate1,samples_per_baud)
    expected_msg = modulate.bytes_to_bin(msg)

    print("Expected Message:".ljust(20), expected_msg)
    print("Decoded Message:".ljust(20),binary_msg)

    # all this is graphing stuff
    # NOTE: WHY do I get an extra (incorrect) bit at the start if I pad it
    fig, (c0plot,c1plot,togetherplot) = pyplot.subplots(nrows=3,sharex=True)
    c0plot.set_title("s0 correlation")
    c0plot.plot(correlate0)
    c1plot.set_title("s1 correlation")
    c1plot.plot(correlate1)
    togetherplot.set_title("combined correlation")
    togetherplot.plot(correlate0)
    togetherplot.plot(correlate1)
    pyplot.show()

if __name__ == "__main__":
    main()