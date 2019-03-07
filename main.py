import os
import scipy.io.wavfile
from numpy import mean , shape, argmax
from pylab import fft
from copy import deepcopy
from scipy.signal import decimate

frequency_threshold = 160

def checkGender(name):
    f, signal = scipy.io.wavfile.read(name)
    full_time = len(signal) / f
    if len(shape(signal)) == 2:
        signal = [mean(s) for s in signal]
    part = int(len(signal) / 5)
    signal = signal[2*part:3 * part]
    spectrum = abs(fft(signal))
    clean_spec = deepcopy(spectrum)
    part_time = full_time * 1/5

    for i in range(2, 6):
        decimate_spec = decimate(clean_spec, i)
        spectrum[:len(decimate_spec)] *= decimate_spec
    check = (40 + argmax(spectrum[40:]))/ part_time
    correct = name[-5]
    if int(check) > frequency_threshold:
        print("K")
    else:
        print("M")


if __name__ == '__main__':
    filenames = os.listdir("data/")
    for filename in filenames:
        checkGender("data/" + filename)