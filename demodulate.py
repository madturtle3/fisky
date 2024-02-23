from constants import *
import numpy
import modulate
from matplotlib import pyplot
from numpy.linalg import norm

def baud_picker(correlate0:numpy.ndarray, correlate1:numpy.ndarray, samples_per_baud:int):
    """
    this takes the signal given and turns it into a string of 1s and 0s
    correlate0 and correlate 1 being the correlation of the high and low
    bauds with the graph.
    This will return a list of the binary recieved split up by any preambles detected.
    The split occurs after end of the preamble.
    """
    picked_bauds = ""
    msglist = []
    for index in numpy.arange(len(correlate1)-samples_per_baud,step=samples_per_baud):
        max0 = max(correlate0[index:index+samples_per_baud])
        max1 = max(correlate1[index:index+samples_per_baud])
        if max1 > max0:
            picked_bauds += "1"
        elif max0 > max1:
            picked_bauds += "0"
        # if there is a preamble we see we want to know it is there
        if picked_bauds.endswith(preamble):
            msglist.append(picked_bauds)
            picked_bauds = ""
    if len(picked_bauds) > 0:
        msglist.append(picked_bauds)
    return msglist

def bin_to_ascii(msg):
    """
    Take ascii as a 7 bit msg and convert it back to text
    """
    result = ""
    for char_range in range(0,len(msg),char_length):
        result += str(
            chr(
                int(
                        msg[char_range:char_range+char_length],2)))
    return result


def normalized_correlation(signal,template_normed):
    """
    Correlate the normalized signal with a (already normalized) template
    """
    correlation = numpy.empty(len(signal)-len(template_normed))
    for index in numpy.arange(len(signal)-len(template_normed)):
        chunk = signal[index:index+len(template_normed)]
        corr_val = numpy.sum(chunk * template_normed) / norm(chunk)
        correlation[index] = corr_val
    return correlation

def add_noise(signal,noise_multiplier):
    if noise_multiplier > 0:
        return numpy.add(signal,numpy.random.rand(len(signal)) * noise_multiplier) /(noise_multiplier) 
    else:
        return signal

def add_echo(signal,alpha,echo_time):
    echo = numpy.concatenate(([1],numpy.zeros(echo_time),[alpha]))
    return numpy.convolve(signal,echo)

def delay_start(signal,start_delay):
    return numpy.concatenate((numpy.zeros(start_delay),signal))


def main():
    msg = "abcdefghijklmnopqrstuvwxyz"
    signal = modulate.bytes_to_sig(msg,s0,s1)

    # pad the end of the signal so it picks up the last baud
    signal = numpy.concatenate((signal,numpy.zeros(samples_per_baud)))
    #signal_old = signal.copy()

    # add a delay before the start of the signal
    start_delay = 2500
    #signal = delay_start(signal,start_delay)

    # uncomment below to add noise
    noise_multiplier = 1
    signal = add_noise(signal,noise_multiplier)


    # add echo
    alpha = .6
    echo_time = 450
    #signal = add_echo(signal,alpha,echo_time)

    # normalize templates
    s0n = s0/norm(s0)
    s1n = s1/norm(s1)
    correlate0 = normalized_correlation(signal,s0n)
    correlate1 = normalized_correlation(signal,s1n)

    # pad the correlation so the maxima align with the baud centers
    correlate0 = numpy.concatenate((numpy.zeros(samples_per_baud//2),correlate0))
    correlate1 = numpy.concatenate((numpy.zeros(samples_per_baud//2),correlate1))

    binary_msg = baud_picker(correlate0,correlate1,samples_per_baud)
    expected_msg = modulate.bytes_to_bin(msg)
    # if numpy.array_equal(signal,signal_old):
    #     print("they are the same")
    if len(binary_msg) > 1:
        if expected_msg == binary_msg[1]:
            print('correct decode!')
        print("English Message:".ljust(20),bin_to_ascii(binary_msg[1]))
        print(binary_msg[1])
    else:

        print(expected_msg,binary_msg)
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