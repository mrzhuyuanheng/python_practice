import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav

fs=44100
duration = 10  # seconds
myrecording = sd.rec(duration * fs, samplerate=fs, channels=2, dtype='float64')
print ("Recording Audio for %s seconds" %(duration))
sd.wait()
print ("Audio recording complete , Playing recorded Audio")
sd.play(myrecording, fs)
sd.wait()
print ("Play Audio Complete")
