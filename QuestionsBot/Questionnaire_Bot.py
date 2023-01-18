import telebot
from telebot import types

bot = telebot.TeleBot(TOKEN)


# this function cathes the '/start' command
@bot.message_handler(commands=['start'])
def start(message):
    global nq
    nq = 0
    qs_file = open('questions.txt', 'r', encoding='utf-8')
    for u in qs_file:
        nq += 1
    qs_file.close()
    markup = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton('Let\'s start!', callback_data='start')
    markup.add(button1)
    bot.send_message(message.chat.id, 'Hello! I`m a questionnaire bot. \
You will be presented with the questions in the survey one by one. \
At the end, you can change some of the answers or do it all over again.', reply_markup=markup)


# this function cathes all callbacks
@bot.callback_query_handler(func=lambda call: True)
def call_collector(call):

    # if call.data == 'start' (user pressed the 'Let`s start!' button from start())
    # then file for user`s answers will be created (ans_file) or rewrited
    # and first question will be send
    if call.data == 'start':
        ans_file = open(str(call.from_user.username) + '.txt', 'w', encoding='utf-8')
        qs_file = open('questions.txt', 'r', encoding='utf-8')
        bot.send_message(call.from_user.id, qs_file.readline())
        qs_file.close()
        ans_file.close()

    # if call.data == 'send' (user pressed the 'Send' button from filling())
    elif call.data == 'send':
        bot.send_message(call.from_user.id, 'Done! You will be contacted soon.')

    # if call.data == 'edit' (user pressed the 'Edit' button from filling())
    # open 'questions' file 
    elif call.data == 'edit':
        qs_file = open('questions.txt', 'r', encoding='utf-8')
        markup = types.InlineKeyboardMarkup()
        # counting questions
        # and creating inline buttons
        m = 0
        for i in qs_file:
            m += 1
            exec("b{} = types.InlineKeyboardButton('{}', callback_data='{}')".format(m, i[:20]+'...', m))
            exec("markup.add(b{})".format(m))
        bot.send_message(call.from_user.id, 'Pick a question to edit', reply_markup=markup)
        qs_file.close()

    # if call.data == 'number of question' (user pressed the button with question number from above)
    # open file with questions, file with answers and reserve file with answers
    else:
        qs_file = open('questions.txt', 'r', encoding='utf-8')
        ans_file = open(str(call.from_user.username) + '.txt', 'r', encoding='utf-8')
        re_ans_file = open('new' + str(call.from_user.username) + '.txt', 'w', encoding='utf-8')
        list_ans = []
        # search for question number-1 (number from call.data)
        for j in range(int(call.data)-1):
            qs_file.readline()
        # filling list_ans with answers
        # mark the replacable file with 'REPLACE ME'
        for o in ans_file:
            list_ans.append(o)
        list_ans[int(call.data)-1] = 'REPLACE ME\n'
        # send question that user wants to reanswer
        bot.send_message(call.from_user.id, qs_file.readline())
        # writing a reserve file with a marked answer from list_ans
        for p in list_ans:
            re_ans_file.write(p)
        qs_file.close()
        ans_file.close()
        re_ans_file.close()


def _ending_message(message):
    markup = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton('Send answers', callback_data='send')
    button2 = types.InlineKeyboardButton('Edit answers', callback_data='edit')
    button3 = types.InlineKeyboardButton('Refill', callback_data='start')
    markup.add(button1)
    markup.add(button2)
    markup.add(button3)
    bot.send_message(message.chat.id, 'Done!', reply_markup=markup)


# this function for filling answers
@bot.message_handler(content_types=['text'])
def filling(message):

    # if user send message
    try:
        global nq
        # if file with answers exist and it`s not full
        ans_file = open(str(message.from_user.username) + '.txt', 'r', encoding='utf-8')
        qs_file = open('questions.txt', 'r', encoding='utf-8')
        # counting lines 
        m = 0
        for i in ans_file:
            m += 1
        if m < nq:
            # open file with answers for writing
            ans_file = open(str(message.from_user.username) + '.txt', 'a', encoding='utf-8')
            # writing
            ans_file.write(message.text + '\n')
            # if it is not last answer

            if m < (nq-1):
                # search for next question
                
                for i in range(m+1):
                    qs_file.readline()
                # send next question
                bot.send_message(message.chat.id, qs_file.readline())
            # if all answers given
            elif m == (nq - 1):
                _ending_message(message)                
        else:
            ans_file.close()
            qs_file.close()
    except:
        None

    # if reserve file exist and it is not empty
    try:
        ans_file = open('new' + str(message.from_user.username) + '.txt', 'r', encoding='utf-8')
        list_ans = []
        # counting lines
        # and writing them in list_ans
        n = 0
        for x in ans_file:
            n += 1
            list_ans.append(x)
        # if file not empty
        if n != 0:
            # searching for REPLACE ME element in list_ans
            # and replace it with message.text
            list_ans[list_ans.index('REPLACE ME\n')] = message.text + '\n'
            # open original file with answers for rewriting
            ans_file = open(str(message.from_user.username) + '.txt', 'w', encoding='utf-8')
            for z in list_ans:
                ans_file.write(z)
            ans_file.close()
            # open reserve file to delete content
            ans_file = open('new' + str(message.from_user.username) + '.txt', 'w', encoding='utf-8')
            ans_file.close()
            _ending_message(message)
        ans_file.close()
    except:
        None

# RUN
bot.polling(none_stop=True)
