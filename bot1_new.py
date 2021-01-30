import requests
import vk_api, json, sqlite3
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.utils import get_random_id
from config import token
from datetime import datetime

vk_session = vk_api.VkApi(token=token)
session_api = vk_session.get_api()
longpoll = VkBotLongPoll(vk_session, 201924345)
db = sqlite3.connect("data.db")
sql = db.cursor()

sql.execute("""CREATE TABLE IF NOT EXISTS users (
    id INT,
    step INT,
    otvet1 TEXT,
    otvet2 TEXT,
    otvet3 TEXT,
    otvet4 TEXT,
    otvet5 TEXT,
    otvet6 TEXT
)""")

db.commit()

def send(id, text, key):
    try:
        vk_session.method('messages.send', {'user_id' : id, 'message' : text, 'random_id' : get_random_id(), 'keyboard' : key})
    except Exception as e:
        f = open('ErrorLog.txt', 'a')
        f.write(str(datetime.now())+' '+str(e)+"\n")
        f.close()

def send_media(id, url, text, key):
    try:
        vk_session.method('messages.send', {'user_id' : id, 'message' : text,'keyboard' : key, 'attachment' : url, 'random_id' : get_random_id()})
    except Exception as e:
        f = open('ErrorLog.txt', 'a')
        f.write(str(datetime.now())+' '+str(e)+"\n")
        f.close()

def stepW(id, step):
    try:
        sql.execute(f'UPDATE users SET step = {step} WHERE id = {id}')
        db.commit()
    except Exception as e:
        f = open('ErrorLog.txt', 'a')
        f.write(str(datetime.now())+' '+str(e)+"\n")
        f.close()

def stepR(id):
    try:
        for i in sql.execute(f"SELECT step FROM users WHERE id = {id}"):
            return i[0]
    except Exception as e:
        f = open('ErrorLog.txt', 'a')
        f.write(str(datetime.now())+' '+str(e)+"\n")
        f.close()

def otvetR(id, n):
    try:
        sql.execute(f"SELECT otvet{n} FROM users WHERE id = {id}")
        return sql.fetchone()[0]
    except Exception as e:
        f = open('ErrorLog.txt', 'a')
        f.write(str(datetime.now())+' '+str(e)+"\n")
        f.close()

def otvetW(id, n, text):
    try:
        sql.execute(f'UPDATE users SET otvet{n} = "{text}" WHERE id = {id}')
        db.commit()
    except Exception as e:
        f = open('ErrorLog.txt', 'a')
        f.write(str(datetime.now())+' '+str(e)+"\n")
        f.close()

key_start = VkKeyboard(one_time=False) #key_start (Начать)
key_start.add_button('Начать', color=VkKeyboardColor.POSITIVE)
key_start = key_start.get_keyboard()

key_play = VkKeyboard(one_time=False) #key_play (ГОТОВ)
key_play.add_button('Готов', color=VkKeyboardColor.POSITIVE)
key_play = key_play.get_keyboard()

key_null = {"buttons":[],"one_time": True}
key_null = json.dumps(key_null, ensure_ascii = False).encode('utf-8')
key_null = str(key_null.decode('utf-8'))

key_step6 = VkKeyboard(one_time=True) #key_step6 (ПРОДОЛЖИТЬ, НАЗАД)
key_step6.add_button('Продолжить', color=VkKeyboardColor.POSITIVE)
key_step6.add_button('Назад', color=VkKeyboardColor.NEGATIVE)
key_step6 = key_step6.get_keyboard()

key_end = VkKeyboard(one_time=False) #key_end (Сброс)
key_end.add_button('Сброс', color=VkKeyboardColor.NEGATIVE)
key_end.add_line()
key_end.add_openlink_button("Подпишись на нашу группу", 'https://vk.com/pearl_light')
key_end = key_end.get_keyboard()

def main():
    try:
        for event in longpoll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW:

                msg = event.obj.text
                id = event.obj.peer_id

                sql.execute(f"SELECT id FROM users WHERE id = {id}")
                if sql.fetchone() is None:
                    sql.execute(f"INSERT INTO users VALUES ('{id}',{0},'none','none','none','none','none','none')")
                    db.commit()
                    send_media(id, 'photo-201924345_457239025', f'Добро пожаловать в тест «Путник».\n\nЭтот тест покажет твои истинные ценности и приоритеты в жизни.\n\n⚠️ Слабонервным не проходить.\n⚠️ В этом тесте важно погружение.\n⚠️ Отнеситесь к тесту серьезно и осознанно.', None)
                    send_media(id, 'photo-201924345_457239018', f"Если ты полностью готов, нажми на кнопку ГОТОВ в меню.", None)
                    send(id, f"Возможно ты не видешь меню, тогда следует обновить приложение или ты можешь писать текстом.\nЗа техподдержкой писать в лс группы https://vk.com/pearl_light.\n\nЧто остановить бота, напиши команду СТОП.", key_play)
                else:
                    if msg.lower() == 'стоп' or msg.lower() == 'сброс':
                        send(id, '[Бот остановлен]', key_start)
                        sql.execute(f'DELETE FROM users WHERE id = {id}')
                        db.commit()
                    else:
                        step = stepR(id)
                        otvet1 = otvetR(id, 1)
                        otvet2 = otvetR(id, 2)
                        otvet3 = otvetR(id, 3)
                        otvet4 = otvetR(id, 4)
                        otvet5 = otvetR(id, 5)
                        otvet6 = otvetR(id, 6)

                        if step == 0:
                            send_media(id, 'photo-201924345_457239023',"Напиши 6 важных для тебя вещей в жизни (например: семья, здоровье, карьера, какие-то люди, вещи или занятия).\n\nПо одной ценности на сообщение (Как на картинке).", key_null)
                            step = 1
                        elif step == 1:
                            otvet1 = msg
                            send(id, '[Записанно 1/6]', None)
                            step = 2
                        elif step == 2:
                            otvet2 = msg
                            send(id, '[Записанно 2/6]', None)
                            step = 3
                        elif step == 3:
                            otvet3 = msg
                            send(id, '[Записанно 3/6]', None)
                            step = 4
                        elif step == 4:
                            otvet4 = msg
                            send(id, '[Записанно 4/6]', None)
                            step = 5
                        elif step == 5:
                            otvet5 = msg
                            send(id, '[Записанно 5/6]', None)
                            step = 6
                        elif step == 6:
                            otvet6 = msg
                            send(id, f'Проверь, все ли верно:\n\n1. {otvet1}\n2. {otvet2}\n3. {otvet3}\n4. {otvet4}\n5. {otvet5}\n6. {otvet6}\n\nЕсли ты ошибся, жми НАЗАД.\nЕсли все правильно, жми ПРОДОЛЖИТЬ.', key_step6)
                            step = 7
                        elif step == 7:
                            if msg.lower() == 'продолжить':
                                key_otvet = VkKeyboard(one_time=True)

                                key_otvet.add_button(f'{otvet1}', color=VkKeyboardColor.SECONDARY)
                                key_otvet.add_button(f'{otvet2}', color=VkKeyboardColor.SECONDARY)

                                key_otvet.add_line()  # Переход на вторую строку

                                key_otvet.add_button(f'{otvet3}', color=VkKeyboardColor.SECONDARY)
                                key_otvet.add_button(f'{otvet4}', color=VkKeyboardColor.SECONDARY)

                                key_otvet.add_line()  # Переход на вторую строку

                                key_otvet.add_button(f'{otvet5}', color=VkKeyboardColor.SECONDARY)
                                key_otvet.add_button(f'{otvet6}', color=VkKeyboardColor.SECONDARY)

                                send_media(id,'photo-201924345_457239031', f'Представь, ты идёшь по пустыне... Идёшь уже несколько дней, и у тебя закончились запасы воды. До ближайшего оазиса очень далеко. Тебя мучает жажда и тебе срочно необходима вода.\n\nНа встречу тебе идёт незнакомец. К счастью у него есть немного лишней воды.', key_otvet.get_keyboard())
                                send(id, f'Он готов обменять её на что-нибудь. У тебя с собой есть только:\n\n1. {otvet1}\n2. {otvet2}\n3. {otvet3}\n4. {otvet4}\n5. {otvet5}\n6. {otvet6}\n\nЧто ты обменяешь?', key_otvet.get_keyboard())

                                step = 8
                            else:
                                send_media(id, 'photo-201924345_457239023',"Напиши 6 важных для тебя вещей в жизни (например: семья, здоровье, карьера, какие-то люди, вещи или занятия).\n\nПо одной ценности на сообщение (Как на картинке).", key_null)
                                step = 1
                        elif step == 8:
                            otvet = otvet6
                            flag = 1
                            if msg == '1' or msg == otvet1:
                                otvet = otvet1
                                otvet1 = otvet6
                            elif msg == '2' or msg == otvet2:
                                otvet = otvet2
                                otvet2 = otvet6
                            elif msg == '3' or msg == otvet3:
                                otvet = otvet3
                                otvet3 = otvet6
                            elif msg == '4' or msg == otvet4:
                                otvet = otvet4
                                otvet4 = otvet6
                            elif msg == '5' or msg == otvet5:
                                otvet = otvet5
                                otvet5 = otvet6
                            elif msg != '6' and msg != otvet6:
                                send(id, 'Введенного ответа нет в списке, попробуй еще раз\n\n1. {otvet1}\n2. {otvet2}\n3. {otvet3}\n4. {otvet4}\n5. {otvet5}\n6. {otvet6}', None)
                                flag = 0
                            if flag == 1:
                                key_otvet = VkKeyboard(one_time=False)
                                key_otvet.add_button(f'{otvet1}', color=VkKeyboardColor.SECONDARY)
                                key_otvet.add_button(f'{otvet2}', color=VkKeyboardColor.SECONDARY)
                                key_otvet.add_line()  # Переход на вторую строку
                                key_otvet.add_button(f'{otvet3}', color=VkKeyboardColor.SECONDARY)
                                key_otvet.add_button(f'{otvet4}', color=VkKeyboardColor.SECONDARY)
                                key_otvet.add_line()  # Переход на вторую строку
                                key_otvet.add_button(f'{otvet5}', color=VkKeyboardColor.SECONDARY)

                                step = 9
                                send(id, f'[Ты отдал "{otvet}"]', key_null)
                                send_media(id,'photo-201924345_457239032', f'На следующий день у тебя опять закончилась вода, а ближайшего оазиса не видать.\nТебя так сильно мучает жажда, что ты готов отдать что-то ценное за глоток воды.\n\nИ тут тебе навстречу бежит счастливая девушка так, словно она не в пустыне, а по морскому побережью пробежку делает.', key_null)
                                send(id, f'Она готова поделиться с тобой источником своей энергии, глотком чистейшей воды, но ты ей должен отдать взамен  что-то из своих ценностей. У тебя с собой есть только:\n\n1. {otvet1}\n2. {otvet2}\n3. {otvet3}\n4. {otvet4}\n5. {otvet5}\n\nЧто ты обменяешь?', key_otvet.get_keyboard())
                        elif step == 9:
                            otvet = otvet5
                            flag = 1
                            if msg == '1' or msg == otvet1:
                                otvet = otvet1
                                otvet1 = otvet5
                            elif msg == '2' or msg == otvet2:
                                otvet = otvet2
                                otvet2 = otvet5
                            elif msg == '3' or msg == otvet3:
                                otvet = otvet3
                                otvet3 = otvet5
                            elif msg == '4' or msg == otvet4:
                                otvet = otvet4
                                otvet4 = otvet5
                            elif msg != '5' and msg != otvet5:
                                send(id, f'Введенного ответа нет в списке, попробуй еще раз\n\n1. {otvet1}\n2. {otvet2}\n3. {otvet3}\n4. {otvet4}\n5. {otvet5}', None)
                                flag = 0
                            if flag == 1:
                                key_otvet = VkKeyboard(one_time=False)
                                key_otvet.add_button(f'{otvet1}', color=VkKeyboardColor.SECONDARY)
                                key_otvet.add_button(f'{otvet2}', color=VkKeyboardColor.SECONDARY)
                                key_otvet.add_line()  # Переход на вторую строку
                                key_otvet.add_button(f'{otvet3}', color=VkKeyboardColor.SECONDARY)
                                key_otvet.add_button(f'{otvet4}', color=VkKeyboardColor.SECONDARY)

                                step = 10
                                send(id, f'[Ты отдал "{otvet}"]', key_null)
                                send_media(id,'photo-201924345_457239030', f'На следующий день ты вновь остался без воды.\nСолнце словно испепеляет тебя, мучает жажда. Тебе срочно необходима вода.\n\nНа встречу тебе идёт незнакомка, и к счастью у неё есть немного лишней воды.', key_null)
                                send(id, f'Она готова обменять её на что-то одно. У тебя из ценностей осталось  только:\n\n1. {otvet1}\n2. {otvet2}\n3. {otvet3}\n4. {otvet4}\n\nЧто ты выберешь на сей раз и отдашь взамен глотка воды?', key_otvet.get_keyboard())

                        elif step == 10:
                            otvet = otvet4
                            flag = 1
                            if msg == '1' or msg == otvet1:
                                otvet = otvet1
                                otvet1 = otvet4
                            elif msg == '2' or msg == otvet2:
                                otvet = otvet2
                                otvet2 = otvet4
                            elif msg == '3' or msg == otvet3:
                                otvet = otvet3
                                otvet3 = otvet4
                            elif msg != '4' and msg != otvet4:
                                send(id, f'Введенного ответа нет в списке, попробуй еще раз\n\n1. {otvet1}\n2. {otvet2}\n3. {otvet3}\n4. {otvet4}', None)
                                flag = 0
                            if flag == 1:
                                key_otvet = VkKeyboard(one_time=False)
                                key_otvet.add_button(f'{otvet1}', color=VkKeyboardColor.SECONDARY)
                                key_otvet.add_button(f'{otvet2}', color=VkKeyboardColor.SECONDARY)
                                key_otvet.add_line()  # Переход на вторую строку
                                key_otvet.add_button(f'{otvet3}', color=VkKeyboardColor.SECONDARY)

                                step = 11
                                send(id, f'[Ты отдал "{otvet}"]', key_null)
                                send_media(id,'photo-201924345_457239026', f'Ты прошагал по пустыне уже три дня. Половина пути пройдена. Держись, друг. Но у тебя опять закончилась вода.\nЖажда настолько не выносима, что ты что угодно отдашь за глоток воды.\n\nНа встречу тебе  уверенно идёт мужчина. Он спокоен и счастлив, потому что он знает, где оазис. Он указывает дорогу тебе, но вода необходима прямо сейчас. К счастью у него есть запасы воды.', key_null)
                                send(id, f'Он готов обменять её на что-то одно. У тебя с собой есть только:\n\n1. {otvet1}\n2. {otvet2}\n3. {otvet3}\n\nЧто ты обменяешь?', key_otvet.get_keyboard())

                        elif step == 11:
                            otvet = otvet3
                            flag = 1
                            if msg == '1' or msg == otvet1:
                                otvet = otvet1
                                otvet1 = otvet3
                            elif msg == '2' or msg == otvet2:
                                otvet = otvet2
                                otvet2 = otvet3
                            elif msg != '3' and msg != otvet3:
                                send(id, f'Введенного ответа нет в списке, попробуй еще раз\n\n1. {otvet1}\n2. {otvet2}\n3. {otvet3}', None)
                                flag = 0
                            if flag == 1:
                                key_otvet = VkKeyboard(one_time=False)
                                key_otvet.add_button(f'{otvet1}', color=VkKeyboardColor.SECONDARY)
                                key_otvet.add_button(f'{otvet2}', color=VkKeyboardColor.SECONDARY)

                                step = 12
                                send(id, f'[Ты отдал "{otvet}"]', key_null)
                                send_media(id,'photo-201924345_457239028', f'  Запас воды, что дал тебе незнакомец, на следующий день закончился, а оазиса так и не видать. Ты изнемогаешь от жажды. Силы на исходе. Но ты не сдаешься и движешься вперёд.\n\nНа встречу тебе идут 3 туриста. Они веселы и полны энергии.\n- В чем ваш секрет?\n- Мы выжили. Мы дошли до оазиса. И он уже "рукой подать".\nУ них есть немного лишней воды.', key_null)
                                send(id, f'Они готовы поделиться с тобой, но взамен ты должен им дать свою ценность. У тебя с собой есть только:\n\n1. {otvet1}\n2. {otvet2}\n\nЧто ты обменяешь?', key_otvet.get_keyboard())

                        elif step == 12:
                            flag = 1
                            if msg == '1' or msg == otvet1:
                                otvet1, otvet2 = otvet2, otvet1
                            elif msg != '2' and msg != otvet2:
                                send(id, f'Введенного ответа нет в списке, попробуй еще раз\n\n1. {otvet1}\n2. {otvet2}', None)
                                flag = 0
                            if flag == 1:
                                step = 13
                                send(id, f'[Ты отдал "{otvet2}"]', key_null)
                                send_media(id, 'photo-201924345_457239027', f'Ты наконец добрался до оазиса и обнаруживаешь, что у тебя с собой остлалсь только - {otvet1},\n\n{otvet1} - Твоя истинная ценность в жизни...', key_null)
                                send(id, 'Благодарим за прохождение теста.  Если хочешь пройти его еще раз, нажми СБРОС.', key_end)

                        stepW(id, step)
                        otvetW(id, 1, otvet1)
                        otvetW(id, 2, otvet2)
                        otvetW(id, 3, otvet3)
                        otvetW(id, 4, otvet4)
                        otvetW(id, 5, otvet5)
                        otvetW(id, 6, otvet6)
    except Exception as e:
        f = open('ErrorLog.txt', 'a')
        f.write(str(datetime.now())+' '+str(e)+"\n")
        f.close()
f = open('ErrorLog.txt', 'a')
f.write(str(datetime.now())+' RUN'+"\n")
f.close()
while True:
    main()