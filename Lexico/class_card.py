class Card(object):

    def __init__(self, theme, eng, rus):
        self.theme = theme
        self.eng = eng
        self.rus = rus

    def getTheme(self):
        return self.theme

    def getEng(self):
        return self.eng

    def getRus(self):
        return self.rus

