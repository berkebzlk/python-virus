import wavio as wv
from sounddevice import rec, wait


def record(name, x):
    freq = 44100
    duration = x
    recording = rec(int(duration * freq), samplerate=freq, channels=2)
    wait()
    wv.write(name, recording, freq, sampwidth=2)