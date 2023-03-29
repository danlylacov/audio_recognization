from audio import audio_main, draw_grafic


def sity_lengh(p_data, q_data): # расстояние городских кварталов
    res_list = []
    for i in range(len(p_data)):
        res = 0
        for j in range(min(len(p_data[i]), len(q_data[i]))):
            res += abs(p_data[i][j] - q_data[i][j])
        res_list.append(res)
    return res_list, sum(res_list)






























