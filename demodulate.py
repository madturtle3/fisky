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

def add_noise(signal,noise_multiplier):
    if noise_multiplier > 0:
        return numpy.add(signal,numpy.random.rand(len(signal)) * noise_multiplier) /(noise_multiplier) 
    else:
        return signal

def delay_start(signal,start_delay):
    return numpy.concatenate((numpy.zeros(start_delay),signal))

def main():
    msg = b"Q"
    signal = modulate.bytes_to_sig(msg,s0,s1)

    # pad the end of the signal so it picks up the last baud
    signal = numpy.concatenate((signal,numpy.zeros(samples_per_baud)))
    
    # add a delay before the start of the signal
    start_delay = 568
    signal = delay_start(signal,start_delay)

    # uncomment below to add noise
    noise_multiplier = 15
    signal = add_noise(signal,noise_multiplier)

    correlate0 = numpy.correlate(signal,s0)
    correlate1 = numpy.correlate(signal,s1)

    # pad the correlation so the maxima align with the baud centers
    correlate0 = numpy.concatenate((numpy.zeros(samples_per_baud//2),correlate0))
    correlate1 = numpy.concatenate((numpy.zeros(samples_per_baud//2),correlate1))

    binary_msg = baud_picker(correlate0,correlate1,samples_per_baud)
    expected_msg = modulate.bytes_to_bin(msg)

    print("Expected Message:".ljust(20), expected_msg)
    print("Decoded Message:".ljust(20),binary_msg)

    # all this is graphing stuff
    # NOTE: WHY do I get an extra (incorrect) bit at the start if I pad it
    fig, (c0plot,c1plot,togetherplot,sigplot) = pyplot.subplots(nrows=4,sharex=True)
    c0plot.set_title("s0 correlation")
    c0plot.plot(correlate0, label="0 correlation")
    c0plot.legend(loc='lower left')
    c1plot.set_title("s1 correlation")
    c1plot.plot(correlate1, label="1 correlation")
    c1plot.legend(loc='lower left')
    togetherplot.set_title("combined correlation")
    togetherplot.plot(correlate0, label = "0 correlation")
    togetherplot.plot(correlate1, label = "1 correlation")
    togetherplot.legend(loc='lower left')
    sigplot.plot(signal, label="signal plot")
    sigplot.legend(loc='lower left')
    pyplot.show()

if __name__ == "__main__":
    main()