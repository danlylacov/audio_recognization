import wave
import struct
import matplotlib.pyplot as plt
from cmath import cos, pi, log10
import scipy.fft
import numpy as np
from python_speech_features import mfcc


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

def is_clean(data):
    count = 0
    for i in range(len(data)):
        if data[i] < 0.12:
            count += 1
    return count


def hamming(data):  # ф-я умноженя каждого элемента массива на окно Хемминга
    for n in range(len(data)):
        data[n] = data[n] * (0.53836 + 0.46164 * cos(2 * pi * n / (len(data) - 1)))
    return data


def gz_to_mel(data):  # перевод из гц в мелы
    for i in range(len(data)):
        data[i] = 1125 * np.log(1 + data[i] / 700)
    return data


def vector(data):
    return mfcc(data, 48000)


def draw_grafic(data):  # отрисовка графика
    plt.plot(data)
    plt.show()


def audio_main(file_name):
    data = pcm_channels(file_name)[0]  # запись PCM данных в массив
    #draw_grafic(data)

    data = normolize(data)  # нормализация сигнала
    #draw_grafic(data)

    data = list(partition(data, 3000))  # разделение задачи на подзадачи (data[n] - отдельно взятый отрезок)


    for i in range(len(data)):  # действия над каждой подзадачей
        try:
            if is_clean(data[i]) > 5800:# удаление пустых участков записи
                del data[i]
                continue


            data[i] = hamming(data[i])# умножение на окно Хемминга
            data[i] = scipy.fft.fft(data[i], len(data[i]))# прогонка через дискретное преобразование фурье
            data[i] = gz_to_mel(data[i]) # перевод из Гц в мел
            data[i] = vector(data[i]) # вычленение вектора признаков
            #print('dcsdc')
        except:
            break


    vector_mel = []
    for i in range(len(data[0])):  # выделение среднего вектора признаков для всех участков
        s = 0
        try:
            for j in range(len(data)):
                s += data[j][i]
            vector_mel.append(s / len(data[0]))
        except:
            pass
    print(data[1])
    print(data[2])
    #draw_grafic(vector_mel)
    print(vector_mel[0])

    return vector_mel


