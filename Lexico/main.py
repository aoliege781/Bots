import os.path
import random
from class_player import Player
from class_card import Card

# get File name
# return list of lines from file
def getFile(c):
    word_list = []
    with open(c+'.txt', 'r', encoding='utf-8') as file:
        while True:
            a = file.readline()
            if a != '':
                word_list.append(a[0:len(a) - 1])
            else:
                break
    return word_list

# get path to file and list with info
# return - nothing
def addToFile(path, info, mode):
    with open(path + '.txt',f'{mode}',encoding='utf-8') as file:
        for i in info:
             file.write(i + '\n')


def checkLog(id):
    try:
        log = getFile('log')
        for i in log:
            if str(id) in i:
                break
        return str(id) in i
    except:
        return False

def getHost(id):
    log = getFile('log')

    for i in log:
        if str(id) in i:
            line_with_id = i.split('*')
            if line_with_id[2] =='HOST':
                return True
            else:
                continue
        else:
            continue
    else:
        return False

def getRoom(id):
    try:
        log = getFile('log')
        for i in log:
            if str(id) in i:
                line_with_id = i.split('*')
                room = line_with_id[1]
                return room
            else:
                continue
        else:
            return False
    except:
        return False

def getAnotherPlayerId(id):
    room = getRoom(id)
    log = getFile('log')
    for i in log:
        if room in i and str(id) not in i:
            line_with_id = i.split('*')
            another_id = line_with_id[0]
            return another_id
        else:
            continue
    else:
        return False







# метод принимает лист, содержащий все слова из файла (результат getThemes)
# метод вернет кортеж с двумя листами слов (eng и rus) из одной темы
def separate(all):
    word_eng = []
    word_rus = []
    for i in range(0,len(all)):
        if i%2:
            word_rus.append(all[i])
        else:
            word_eng.append(all[i])


    return word_eng, word_rus

# метод принимает два листа (eng и rus) из одной темы (результат separate)
# метод вернет кортеж из 2 листов 5 рандомных eng и 5 рандомных rus
def random_ten_words(from_sep):
    word_eng = []
    word_rus = []
    while len(word_eng) != 5:
        ind = random.randint(1, len(from_sep[0])-1)
        if from_sep[0][ind] not in word_eng:
            word_eng.append(from_sep[0][ind])
            word_rus.append(from_sep[1][ind])

    return word_eng, word_rus

# метод принимает список из 5 тем
# метод вернет лист с 5 картами, в каждой карте есть: Тема, 5 слов на eng и 5 слов на rus
def set_cards(themes):
    cards = []
    for i in range(0,2):
        words = random_ten_words(separate(getFile(f'Themes\\{themes[i]}')))
        words_string_eng = '*'.join(words[0])
        words_string_rus = '*'.join(words[1])

        cards.append([themes[i], words_string_eng, words_string_rus])
    return cards




# set player`s cur word and status
def setCur(pl, eng, rus, status):
    # get pl file
    player = getFile(pl)
    first_line = player[0].split('*') # id*status*
    first_line[1] = str(status)

    player[0] = '*'.join(first_line) # id*status*
    player[1] = f'{eng}*{rus}*' # engword*rusword*
    addToFile(pl,player,'w')


def getCards(id):
    cards = []
    room = getRoom(id)
    for i in range(0,2):
        if os.path.exists(f'Rooms\\{room}\\card{i}.txt'):
            card = getFile(f'Rooms\\{room}\\card{i}')
            cards.append(card)

        else:
            continue
    return cards


# delete last word from card
# rewrite card
# return two words eng and rus for user
def getNextWords(id):
    cards = getCards(id)
    room = getRoom(id)

    cur_card = random.choice(cards)
    words_eng = cur_card[1].split('*')
    words_rus = cur_card[2].split('*')
    eng = words_eng.pop()
    rus = words_rus.pop()
    cur_card[1] = '*'.join(words_eng)
    cur_card[2] = '*'.join(words_rus)
    index_cur = cards.index(cur_card)

    addToFile(f'Rooms\\{room}\\card{index_cur}',cur_card,'w')

    return cur_card[0], eng, rus

# get user status
def getStatus(id):
    try:
        room = getRoom(id)
        if getHost(id) == True:
            pl_numb = 1
        else:
            pl_numb = 2

        player = getFile(f'Rooms\\{room}\\pl{pl_numb}')
        status = player[0].split('*')
        return status[1]
    except:
         return '0'

def checkAnswer(text, id):
    room = getRoom(id)
    if getHost(id) == True:
        pl_numb = 1
    else:
        pl_numb = 2

    player = getFile(f'Rooms\\{room}\\pl{pl_numb}')
    guess_word = player[1].split('*')
    if text == guess_word[1]:
        player[2] = player[2] + text + '*'
    else:
        player[3] = player[3] + text + '*'

    addToFile(f'Rooms\\{room}\\pl{pl_numb}',player,'w')

def rewriteLog(id,info):
    log = getFile('log')
    for i in range(0,len(log)):
        print(log[i])
        if id in log[i]:
            log[i] = info
        else:
            continue
    for j in log:
        print(j)
    addToFile('log',log,'w')
