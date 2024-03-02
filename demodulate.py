from constants import *
import numpy
import modulate
from matplotlib import pyplot
from numpy.linalg import norm
import time
import sounddevice

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

def callback(data,frames,time,status):
    global signal
    data = data.astype(NP_FORMAT)
    signal = numpy.concatenate((signal,data.T[0]))

def main():

    inputstream = sounddevice.InputStream(samplerate=Fs,channels=CHANNELS,callback=callback,blocksize=Fs)
    inputstream.start()
    try:
        print("GO")
        start = time.time()
        while True:
            pass
    except Exception as err:
        raise err
    except KeyboardInterrupt:
        inputstream.stop(False)
        stop = time.time()
        print("TIME ELAPSED: ",round(stop-start,3))
        print("TIME RECORDED:",round(len(signal)/Fs,3))
        print("PROCESSING")

    # add a delay before the start of the signal
    #start_delay = 2500
    #signal = delay_start(signal,start_delay)

    # uncomment below to add noise
    # noise_multiplier = .3
    # signal = add_noise(signal,noise_multiplier)


    # add echo
    # alpha = .6
    # echo_time = 450
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
    # expected_msg = modulate.bytes_to_bin(msg)
    # if numpy.array_equal(signal,signal_old):
    #     print("they are the same")
    print("# OF PREAMBLES: ",len(binary_msg))
    print("EXPECTED:",modulate.bytes_to_bin("HELLO"))
    for bin_text in binary_msg:
        print(bin_text)
        print(bin_to_ascii(bin_text))
        #print(expected_msg,binary_msg)
    # all this is graphing stuff
    # NOTE: WHY do I get an eaxtra (incorrect) bit at the start if I pad it
    fig, ((c0plot,c1plot),(togetherplot,sigplot),(hist1,hist0)) = pyplot.subplots(nrows=3,ncols=2,sharex="row")
    c0plot.set_title("s0 correlation")
    c0plot.plot(correlate0, label="0 correlation")
    c0plot.legend(loc='lower left')
    c1plot.set_title("s1 correlation")
    c1plot.plot(correlate1, label="1 correlation",color="orange")
    c1plot.legend(loc='lower left')
    togetherplot.set_title("combined correlation")
    togetherplot.plot(correlate0, label = "0 correlation")
    togetherplot.plot(correlate1, label = "1 correlation",color="orange")
    togetherplot.legend(loc='lower left')
    sigplot.plot(signal, label="signal plot")
    sigplot.legend(loc='lower left')
    hist1.hist(correlate1,25,color="orange",label="correlate1 histogram")
    hist1.legend()
    hist0.hist(correlate0,25,label="correlate0 histogram")
    hist0.legend()
    pyplot.show()
    print("1 count:","".join(binary_msg).count("1"))
    print("0 count:","".join(binary_msg).count("0"))
    sounddevice.play(signal,Fs)
    sounddevice.wait()

if __name__ == "__main__":
    signal = numpy.empty((0),NP_FORMAT)
    main()