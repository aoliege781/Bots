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
    log = getFile('log')
    return str(id) in log

def getHost(id):
    log = getFile('log')
    for i in log:
        if str(id) in i:
            line_with_id = i.split('*')
            if line_with_id[2] =='HOST':
                return True
            else:
                return False
        else:
            return False

def getRoom(id):
    log = getFile('log')
    for i in log:
        if str(id) in i:
            line_with_id = i.split('*')
            room = line_with_id[1]
            return room
        else:
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
    word_eng = ''
    word_rus = ''
    while len(word_eng) != 5:
        ind = random.randint(1, len(from_sep[0])-1)
        if from_sep[0][ind] not in word_eng:
            word_eng += from_sep[0][ind] + '*'
            word_rus += from_sep[1][ind] + '*'

    return word_eng, word_rus

# метод принимает список из 5 тем
# метод вернет лист с 5 картами, в каждой карте есть: Тема, 5 слов на eng и 5 слов на rus
def set_cards(themes):
    cards = []
    for i in range(0,5):
        words = random_ten_words(separate(getFile(f'Themes\\{themes[i]}')))
        cards.append(Card(themes[i], words[0], words[1]))
    return cards

def get_cards(id):
    room = getRoom(id)
    cards = []
    count = 0
    while len(cards) < 5:
        cards.append(getFile(f'Rooms\\{room}\\card{count}'))



# check player`s status
def getStatus(player_id):
    room = getRoom(player_id)
    # print(getHost(id))
    if os.path.exists(f'Rooms\\{room}\\pl1.txt') or os.path.exists(f'Rooms\\{room}\\pl1.txt'):
        if getHost(player_id) == room:
            path_for_create = f'{room}\\pl1'
        else:
            path_for_create = f'{room}\\pl2'
        with open('Rooms\\' + path_for_create + '.txt', 'r', encoding='utf-8') as file:
            s = file.readline()
            pl = s.split('*')
        return pl[1]
    else:
        return False

# set True
def setStatus(path):
    player = getFile(path)
    first_line = player[0].split('*')
    first_line[1] = 'True'
    player[0] = '*'.join(first_line)
    # create_pl(path[6:], player)

# set player`s cur word and status
def setCur(pl, eng, rus, status):
    # get pl file
    player = getFile(pl)
    first_line = player[0].split('*')
    first_line[1] = str(status)
    player[0] = '*'.join(first_line)
    player[1] = f'{eng}*{rus}*'
    addToFile(pl,player,'w')

# chek answer and set it done or undone
def check(id, mes):
    room = getRoom(id)
    if getHost(id) == False:
        player = getFile(f'Rooms\\{room}\\pl2')
        path_for_create = f'{room}\\pl2'
        setStatus(f'Rooms\\{room}\\pl1')
    else:
        setStatus(f'Rooms\\{room}\\pl2')
        player = getFile(f'Rooms\\{room}\\pl1')
        path_for_create = f'{room}\\pl1'
    first_line = player[0].split('*')
    first_line[1] = 'False'
    player[0] = '*'.join(first_line)
    cur_words = player[1].split('*')
    done_words = player[2].split('*')
    undone_words = player[3].split('*')
    # If player is right
    # we should del cur words
    if mes == cur_words[1]:
        done_words.append(mes)
        player[1] = 'None*None*'
        player[2] = '*'.join(done_words)
    else:
        undone_words.append(mes)
        player[1] = 'None*None*'
        player[3] = '*'.join(undone_words)
    # create_pl(path_for_create, player)
