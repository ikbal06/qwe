
from robot.libraries.BuiltIn import BuiltIn


class NesneUretenLib:
    def __init__(self, mesaj):
        print('benden bir nesne yaratiyor: ', mesaj)
        self.Mesaj = mesaj

    def yazdir(self):
        BuiltIn().log("Ben: ", self.Mesaj)
