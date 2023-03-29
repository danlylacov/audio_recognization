import sounddevice as sd
from scipy.io.wavfile import write
import wavio as wv
from settings import SEMPLATE_OF_SIGNAL
import wave
import struct


def pcm_channels(wave_file):  # wav to PCM
    stream = wave.open(wave_file, "rb")

    num_channels = stream.getnchannels()
    sample_rate = stream.getframerate()
    sample_width = stream.getsampwidth()
    num_frames = stream.getnframes()

    raw_data = stream.readframes(num_frames)
    stream.close()

    total_samples = num_frames * num_channels

    if sample_width == 1:
        fmt = "%iB" % total_samples
    elif sample_width == 2:
        fmt = "%ih" % total_samples
    else:
        raise ValueError("Only supports 8 and 16 bit audio formats.")

    integer_data = struct.unpack(fmt, raw_data)
    del raw_data

    channels = [[] for time in range(num_channels)]

    for index, value in enumerate(integer_data):
        bucket = index % num_channels
        channels[bucket].append(value)

    return channels



def recording(name: str = 'audio', sec: int = 5):
    print('Сделайте запись в течении '+str(sec)+' сек')
    recording = sd.rec(int(sec * SEMPLATE_OF_SIGNAL),
                   samplerate=SEMPLATE_OF_SIGNAL, channels=1)
    sd.wait()
    wv.write("dict\ "+ name + ".wav", recording, SEMPLATE_OF_SIGNAL, sampwidth=2)
    return pcm_channels("dict\ "+ name + ".wav")[0]

