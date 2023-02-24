import cmath
import wave
import struct
import matplotlib.pyplot as plt
from math import cos, pi
from cmath import exp, pi, sqrt


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


def normolize(data):  # нормализация PCM данных
    m = max(data)
    for i in range(len(data)):
        data[i] = data[i] / m
    return data


def partition(data, n):  # разделение задачи на подзадачи (data - входной массив данных, n - размер отрезка)
    for i in range(0, len(data), n // 2):
        yield data[i:i + n // 2 + n // 2]


def window_of_hemming(data, N):  # использование окна Хемминга к каждому значению списка
    for i in range(len(data)):
        data[i] = 0.53836 - 0.46164 * cos((2 * pi * (i + 1)) / (N - 1))
    return data


def furie(data, k):  # дискретное преобразование фурье и возведение значения в квадрат
    res = 0
    N = len(data)
    for i in range(N):
        res += data[i] * exp(((-2 * pi * sqrt(-1)) / N) * k * i)
    return res ** 2


def gz_to_mel(f):  # перевод из гц в мелы
    return 2595 * cmath.log10(1 + f / 700)


def vector(data, K):
    vector_data = []
    c = 0
    for n in range(1, len(data)):
        a = cmath.log10(data[i]) * (n * (n - 0.5) * (pi / K))
        c += a
        vector_data.append(c)
    return vector_data


def draw_grafic(data):  # отрисовка графика
    plt.plot(data)
    plt.show()


data = pcm_channels('sample-3s.wav')[0]
# draw_grafic(data)
data = normolize(data)
# draw_grafic(data)
data = list(partition(data, 6000))  # разделение задачи на подзадачи
# draw_grafic(data[0])
for i in range(len(data)):
    data[i] = window_of_hemming(data[i], 6000)
for i in range(len(data)):
    data[i] = furie(data[i], i)
draw_grafic(data[0])
#a = vector(data, 20)
print(vector(data, 20))







