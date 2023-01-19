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



# if user press 'create'
# 1) create a ROOM
# 2) write user to log file
# 3) create a user`s file in ROOM

@bot.callback_query_handler(func=lambda call: True)
def call_collector(call):
    if call.data == 'create':
        # 1) Create a ROOM
        letters = string.ascii_uppercase
        room_name = ''.join(random.choice(letters) for i in range(5))
        os.mkdir('Rooms\\' + room_name)

        # 2) write user to log file '{user_id}*{room_name}*{host or not}'
        with open('log.txt', 'a', encoding='utf-8') as log:
            log.write(str(call.from_user.id) + '*' + room_name + '*' + 'HOST' + '\n')

        # 3) create a user`s file in ROOM
        player = [f'{call.from_user.id}*0*','None*None*','*','*']
        main.addToFile(f'Rooms\\{room_name}\\pl1', player, 'w')

        bot.send_message(call.from_user.id ,'Код вашей комнаты -> ' + room_name +'. Игрок, желающий играть с вами, должен отправить этот код боту!')

    # if user press 'enter room'
    elif call.data == 'enter':
        bot.send_message(call.from_user.id,'Введите код комнаты, чтобы присоединиться к другому игроку!')


# 1) chek if player in log
# 2) if it`s in log -> he didn`t need to write a room name
def entering_code(message):
    if len(message.text) == 5:
        if main.checkLog(message.from_user.id):
            return False
        else:
            return True
    else:
        return False

# user send FFFFF message
# 1) check if this room exist
# 2) if so, check its full or not
# 3) if not full (less then 2 files) - write to log file
# 4) create a file in room for second player
# 5) send HOST themes list
# 6) create file with entered themes
@bot.message_handler(func=entering_code, content_types=['text'])
def enter(message):
    # 1) check if this room exist
    if os.path.exists('Rooms\\' + message.text):

        # 2) if so, check its full or not
        files = os.listdir(path=f'Rooms\\{message.text}')
        if len(files) < 2:

            # 3) if not full (less then 2 files) - write to log file
            with open('log.txt', 'a', encoding='utf-8') as log:
                log.write(str(message.from_user.id) + '*' + str(message.text) + '*' + 'GUEST' + '\n')

            # 4) create a file in room for second player
            player = [f'{message.from_user.id}*0*', 'None*None*', '*', '*']
            main.addToFile(f'Rooms\\{message.text}\\pl2', player, 'w')

            bot.send_message(message.from_user.id, 'Ожидаем создателя комнаты...')

            # 5) send HOST themes list
            with open('Rooms\\' + message.text + '\\pl1.txt', 'r', encoding='utf-8') as pl1:
                pl1_first_line = pl1.readline().split('*')
                all_themes = main.getFile('Themes\\темы')
                bot.send_message(pl1_first_line[0],'Второй игрок уже в комнате! сейчас вам будет отправлен список тем.\
Вы должны выбрать пять штук. Напишите их в пяти разных сообщениях именно так, как они есть в списке, без пробела после названия темы')
                bot.send_message(pl1_first_line[0], ' | '.join(all_themes))
                # 6) create file with entered themes
                c = open('Rooms\\' + message.text + '\\Themes.txt', 'w', encoding='utf-8')
                c.close()
        else:
            bot.send_message(message.from_user.id, 'Кажется эта комната занята! Попробуйте другую!')
    else:
        bot.send_message(message.from_user.id, 'Увы, такой комнаты нет :C')

# 1) if user = HOST
# 2) if themes.txt - exist (means that previous step is passed)
# 3) if themes < 5
def checkIfThemes(message):
    room = main.getRoom(message.from_user.id)
    if main.getHost(message.from_user.id) and os.path.exists('Rooms\\' + room + '\\Themes.txt')\
and len(main.getFile('Rooms\\' + room + '\\Themes')) < 5:
        return True
    else:
        return False


# 1) get all themes
# 2) chek if user`s theme is in list 1) ->
# 3) write users theme in Theme
# 4) if there are five themes
# 5) create cards
@bot.message_handler(func=checkIfThemes, content_types=['text'])
def write_themes(message):
    # 1) get all themes
    all_themes = main.getFile('Themes\\темы')

    # 2) chek if user`s theme is in list 1)
    if message.text in all_themes:
        room = main.getRoom(message.from_user.id)
        # 3) write users theme in Theme
        main.addToFile(f'Rooms\\{room}\\Themes.txt', list(message.text), 'a')

        # 4) if there are five themes
        themes = main.getFile(f'Rooms\\{room}\\Themes.txt')
        if len(themes) == 5:

            # 5) create cards
            cards = main.set_cards(themes)
            ind = 0
            for i in cards:
                main.addToFile(f'Rooms\\{room}\\card{ind}.txt', i, 'w')
                ind += 1
            sec_pl_id = main.getAnotherPlayerId(message.from_user.id)
            question = random.choice(cards)
            word_eng = question.eng.pop()
            word_rus = question.rus.pop()
            bot.send_message(sec_pl_id, f'Игра началась! Вашему оппоненту отправлено слово {word_eng} из темы {question.theme}. Перевод - {word_rus}')
            bot.send_message(message.from_user.id, f'Игра началась! Ваше первое слово - {word_eng} из темы {question.theme}')
            ind_of_question = cards.index(question)

            main.setCur(f'Rooms\\{room}\\pl1',word_eng, word_rus, 1)

            main.addToFile(f'Rooms\\{room}\\card{ind_of_question}.txt', question, 'w')


    else:
        bot.send_message(message.from_user.id, 'Такой темы нет!')

# #if user active - then message.text will be accepted as answer
# def is_user_active(message):
#     if main.getStatus(message.from_user.id) == 'True':
#
#         print('проходи не задерживайся')
#         return True
#     else:
#
#         print('хуй тебе')
#         return False
#
#
# # this func will catch user`s answers
# @bot.message_handler(func=is_user_active, content_types=['text'])
# def answering(message):
#     # check done or undone and set status for another player
#     main.check(message.from_user.id ,message.text)
#     # ask question for another player




# RUN
bot.polling(none_stop=True)