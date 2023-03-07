import wave
import struct
import matplotlib.pyplot as plt
from cmath import cos,  pi, log10
import scipy.fft


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


def hamming(data): # ф-я умноженя каждого элемента массива на окно Хемминга
    for n in range(len(data)):
        data[n] = data[n] * (0.54 + 0.46 * cos(pi * n / (len(data) - 1)))
    return data


def gz_to_mel(data):  # перевод из гц в мелы
    for i in range(len(data)):
        data[i] = 2595 * log10(1 + data[i] / 700)
    return data


def vector(data, K):
    vector_data = []
    c = 0
    for n in range(1, len(data)):
        a = log10(data[i]) * (n * (n - 0.5) * (pi / K))
        c += a
        vector_data.append(c)
    return vector_data


def draw_grafic(data):  # отрисовка графика
    plt.plot(data)
    plt.show()


data = pcm_channels('sample-3s.wav')[0]# запись PCM данных в массив
#draw_grafic(data)

data = normolize(data)# нормализация сигнала
#draw_grafic(data)

data = list(partition(data, 6000))  # разделение задачи на подзадачи (data[n] - отдельно взятый отрезок)
#draw_grafic(data[1])

for i in range(len(data)):# умножение каждого значения кадра на окно Хемминга
    data[i] = hamming(data[i])

#draw_grafic(data[1])


for i in range(len(data)): # прогонка значений через дискретное преобразование Фурье
    data[i] = scipy.fft.fft(data[i], len(data[i]))



for i in range(len(data)): # преобразование данных из Гц в Мел
    data[i] = gz_to_mel(data[i])

for i in range(len(data)):
    draw_grafic(vector(data[i], 20))










