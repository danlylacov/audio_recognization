from audio import audio_main, draw_grafic


def sity_lengh(p_data, q_data): # расстояние городских кварталов
    res = 0
    for i in range(min(len(p_data), len(q_data))):
        res += abs(p_data[i] - q_data[i])
    return res

dan1 = audio_main('audio1\Record (online-voice-recorder.com)--online-audio-convert.com.wav')
dan2 = audio_main('audio1\Record (online-voice-recorder.com) (2)--online-audio-convert.com.wav')
andr1 = audio_main('audio1\Record (online-voice-recorder.com) (3)--online-audio-convert.com.wav')
andr2 = audio_main('audio1\Record (online-voice-recorder.com) (4)--online-audio-convert.com.wav')
dan3 = audio_main('audio1\Record (online-voice-recorder.com) (5)--online-audio-convert.com.wav')
al1 = audio_main('audio1\Record (online-voice-recorder.com) (6)--online-audio-convert.com.wav')
al2 = audio_main('audio1\Record (online-voice-recorder.com) (7)--online-audio-convert.com.wav')
print(sity_lengh(dan1, dan2))
print(sity_lengh(al1,  dan1))
print(sity_lengh(al1, al2))




