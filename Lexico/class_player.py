class Player(object):

    def __init__(self, id, active, cur_eng, cur_rus, done, undone):
        self.id = id
        self.active = active
        self.cur_eng = cur_eng
        self.cur_rus = cur_rus
        self.done = done
        self.undone = undone

    # метод вернет имя игрока
    def getId(self):
        return self.id

    # метод вернет слова, которые игрок отгадал
    def getDone(self):
        return self.done

    # метод вернет слова, которые игрок не отгадал
    def getUndone(self):
        return self.undone

    # метод вернет состояние игрока - он отвечает сейчас или нет
    def getActive(self):
        return self.active


    # Set методы
    def setName(self, id):
        self.id = id

    def setDone(self, done):
        self.done = done

    def setUndone(self, undone):
        self.undone = undone

    def setActive(self, active):
        self.active = active

