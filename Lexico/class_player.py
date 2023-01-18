class Player(object):

    def __init__(self, name, done, undone, active, host):
        self.name = name
        self.done = done
        self.undone = undone
        self.active = active
        self.host = host

    # метод вернет имя игрока
    def getName(self):
        return self.name

    # метод вернет слова, которые игрок отгадал
    def getDone(self):
        return self.done

    # метод вернет слова, которые игрок не отгадал
    def getUndone(self):
        return self.undone

    # метод вернет состояние игрока - он отвечает сейчас или нет
    def getActive(self):
        return self.active

    def getHost(self):
        return self.host

    # Set методы
    def setName(self, name):
        self.name = name

    def setDone(self, done):
        self.done = done

    def setUndone(self, undone):
        self.undone = undone

    def setActive(self, active):
        self.active = active

