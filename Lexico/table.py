import random
import telebot
from telebot import types
import main
from class_player import Player
import cfg
import string
import os

bot = telebot.TeleBot(cfg.TOKEN)

# мы нажали старк, предлагают выбрать или создать комнату
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton('Войти в комнату', callback_data='enter')
    button2 = types.InlineKeyboardButton('Создать комнату', callback_data='create')
    markup.add(button1)
    markup.add(button2)
    bot.send_message(message.chat.id, 'Привет! Это игровой бот Lexico! Ты хочешь вступить в какую-то игру,\
или создать комнату?', reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def call_collector(call):
    # if user press 'create new room'
    if call.data == 'create':
        # generate a room name
        letters = string.ascii_uppercase
        room_name = ''.join(random.choice(letters) for i in range(5))
        # create a folder with room name
        os.mkdir('Rooms\\' + room_name)
        # write to log file '{user_id}*{room_name}*{host or not}'
        with open('log.txt', 'a', encoding='utf-8') as log:
            log.write(str(call.from_user.id) + '*' + str(room_name) + '*' + 'HOST' + '\n')
        # create a file in Room, with first player info
        player = [f'{call.from_user.id}*True*','None*None*','None','None']
        main.create_pl(f'{room_name}\\pl1', player)
        bot.send_message(call.from_user.id ,'Код вашей комнаты -> ' + room_name +'. Игрок, желающий играть с вами, должен отправить этот код боту!')

    # if user press 'enter room'
    elif call.data == 'enter':
        bot.send_message(call.from_user.id,'Введите код комнаты, чтобы присоединиться к другому игроку!')



def entering_code(message):
    # open the log file and check if user already in room
    # if in room:

    if len(message.text) == 5:
        # если игрока нет в логе, значит нет и в комнате, значит можно его куда-то определить
        if main.checkRoom(message.from_user.id):
            return True
    else:
        return False

@bot.message_handler(func=entering_code, content_types=['text'])
def enter(message):
    # if this room exists
    if os.path.exists('Rooms\\' + message.text):
        # if room is not full
        files = os.listdir(path=f'Rooms\\{message.text}')
        if len(files) < 2:
            # write to log file '{user_id}*{room_name}*{host or not}'
            with open('log.txt', 'a', encoding='utf-8') as log:
                log.write(str(message.from_user.id) + '*' + str(message.text) + '*' + 'GUEST' + '\n')
            # create a file in Room, with second player info
            player = [f'{message.from_user.id}*True*','None*None*','None','None']
            main.create_pl(f'{message.text}\\pl2', player)
            bot.send_message(message.from_user.id, 'Ожидаем создателя комнаты...')

            # now bot should send themes to Host to choose
            # open pl1 file to find host`s id

            with open('Rooms\\' + message.text + '\\pl1.txt', 'r', encoding='utf-8') as pl1:
                # get Themes
                player = pl1.readline().split('*')
                all_themes = main.getFile('Themes\\темы')
                bot.send_message(player[0],'Второй игрок уже в комнате! сейчас вам будет отправлен список тем. Вы должны выбрать 5')
                bot.send_message(player[0],'Напишите их в пяти разных сообщениях')
                bot.send_message(player[0], ' | '.join(all_themes))
                # create file for five themes
                c = open('Rooms\\' + message.text + '\\Themes.txt', 'w', encoding='utf-8')
                c.close()

        else:
            bot.send_message(message.from_user.id, 'Кажется эта комната занята! Попробуйте другую!')
    else:
        bot.send_message(message.from_user.id, 'Увы, такой комнаты нет :C')

# эта функция фильтр. Она пропустит собщение в хендлер, 1) если тот, кто отправил - хост
# 2) если в комнате есть файл "темы" и его длина меньше 5
def checkIfThemes(message):
    a = main.getHost(message.from_user.id)
    # если отправитель хост - и файл Темы существует
    if a != False and os.path.exists('Rooms\\' + a + '\\Themes.txt'):
        # посчитаем кол-во тем
        with open('Rooms\\' + a + '\\Themes.txt', 'r', encoding='utf-8') as file:
            count = 0
            while True:
                b = file.readline()
                if b != '':
                    count += 1
                else:
                    break
            if count < 5:
                return True
            else:
                print('пишет Хост но вопросы заполнены')
                return False
    else:
        print('пишет не Хост')
        return False

# этот хендлер должен есть только отдельные сообщения от хоста
# ЕСЛИ ТЕМ УЖЕ 5 ТО СЮДА СООБЩЕНИЯ НЕ ПОПАДУТ
# тут же мы создадим 5 карт и отправим первый вопрос юзеру
@bot.message_handler(func=checkIfThemes, content_types=['text'])
def write_themes(message):
    # get all themes
    all_themes = main.getFile('Themes\\темы')
    # if user`s message is in the all_themes
    if message.text in all_themes:
        c = main.getHost(message.from_user.id) # number of ROOM if user - HOST
        # writing
        with open('Rooms\\' + c + '\\Themes.txt', 'a', encoding='utf-8') as file:
            file.write(message.text + '\n')
        themes = main.getFile(f'Rooms\\{c}\\Themes')
        if len(themes) == 5:
            # create cards
            cards = main.set_cards(themes)
            ind = 0
            for i in cards:
                with open('Rooms\\' + c + '\\' + 'card' + str(ind) + '.txt', 'w', encoding='utf-8') as file:
                    file.write(str(i.theme) + '\n')
                    file.write(str(i.eng) + '\n')
                    file.write(str(i.rus) + '\n')
                ind += 1
            with open('Rooms\\' + c + '\\' + 'pl2.txt', 'r', encoding='utf-8') as pl2:
                sec_pl_id = int(pl2.readline().split('*')[0])
            question = random.choice(cards)
            word_eng = question.eng.pop()
            word_rus = question.rus.pop()
            bot.send_message(sec_pl_id, f'Игра началась! Вашему оппоненту отправлено слово {word_eng} из темы {question.theme}. Перевод - {word_rus}')
            bot.send_message(message.from_user.id, f'Игра началась! Ваше первое слово - {word_eng} из темы {question.theme}')
            ind_of_question = cards.index(question)
            # set user`s cur words
            main.setCur(f'Rooms\\{c}\\pl1',word_eng, word_rus, True)

            with open('Rooms\\' + c + '\\' + 'card' + str(ind_of_question) + '.txt', 'w', encoding='utf-8') as file:
                file.write(str(question.theme) + '\n')
                file.write(str(question.eng) + '\n')
                file.write(str(question.rus) + '\n')

    else:
        bot.send_message(message.from_user.id, 'Такой темы нет!')

#if user active - then message.text will be accepted as answer
def is_user_active(message):
    return main.getStatus(message.from_user.id)

# this func will catch user`s answers
@bot.message_handler(func=is_user_active, content_types=['text'])
def answering(message):
    print('разрешили сюда зайти')
    # we should check if answer is correct or not
    main.check(message.from_user.id ,message.text)



# RUN
bot.polling(none_stop=True)