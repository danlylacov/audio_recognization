import matplotlib.pyplot as plt
from cmath import cos, pi
import scipy.fft
import numpy as np
from python_speech_features import mfcc
from settings import SEMPLATE_OF_SIGNAL,  DELETE_FRAME_LIMIT, FRAME_LIMIT, SUBTASK_LENGTH


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
        if data[i] < FRAME_LIMIT:
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
    return mfcc(data, SEMPLATE_OF_SIGNAL)


def get_average_vector(data):  # усреднение вектора признаков для каждого участка записи
    average_vector = [list(0 for i in range(len(data[0][0]))) for i in range(len(data[0]))]
    len_data = len(data)
    for n in range(len(data)):

        vector = data[n]
        for i in range(len(vector)):
            for j in range(len(vector[i])):
                average_vector[i][j] = average_vector[i][j] + vector[i][j]

    for i in range(len(average_vector)):
        for j in range(len(average_vector[i])):
            average_vector[i][j] = average_vector[i][j] / len_data

    return average_vector



def draw_grafic(data):  # отрисовка графика
    plt.plot(data)
    plt.show()



def audio_main(data):
    #data = pcm_channels(file_name)[0]  # запись PCM данных в массив
    #draw_grafic(data)

    data = normolize(data)  # нормализация сигнала
    #draw_grafic(data)

    data = list(partition(data, SUBTASK_LENGTH))  # разделение задачи на подзадачи (data[n] - отдельно взятый отрезок)


    for i in range(len(data)):  # действия над каждой подзадачей
        try:
            if is_clean(data[i]) > DELETE_FRAME_LIMIT:# удаление пустых участков записи
                del data[i]
                continue


            data[i] = hamming(data[i])# умножение на окно Хемминга
            data[i] = scipy.fft.fft(data[i], len(data[i]))# прогонка через дискретное преобразование фурье
            data[i] = gz_to_mel(data[i]) # перевод из Гц в мел
            data[i] = vector(data[i]) # вычленение вектора признаков
            #print('dcsdc')
        except:
            break

    data = get_average_vector(data)
    return  data












