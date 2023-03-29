import sqlite3
from recording import recording
from audio import audio_main
from indification import sity_lengh


try:
    db = sqlite3.connect('users.db')
    cur = db.cursor()
    print('Database connected!')
except:
    print('Database error!')



def str_to_list(data: str = ''):
    data = data[2:-2]
    data = data.split('], [')
    res = []
    for i in range(len(data)):
        mas = []
        st = data[i].split(',')
        for j in range(len(st)):
            mas.append(float(st[j]))
        res.append(mas)
    return res



def registration():
    print('Введите логин: ')
    login = str(input())
    data =  recording(login)
    data = audio_main(data)
    cur.execute('INSERT INTO main(login, vector) VALUES (?, ?)', (login, str(data)))
    db.commit()
    print('Вы успешно зарегистрированы!')


def enter():
    print('Введите логин: ')
    login = str(input())

    cur.execute('SELECT vector FROM main WHERE login = ?', (login,))
    data_bd = (str_to_list(cur.fetchone()[0]))

    data_new = recording(login)
    data_new = audio_main(data_new)

    difference = sity_lengh(data_bd, data_new)
    print(difference)
    if difference[1] <=58.46:
        print('Вы успешно вошли!')
    else:
        print('Голос не совпал!')




command = ''
while command != 'exit':
    command = str(input())
    if command == 'registration':
        registration()
    if command == 'enter':
        enter()




