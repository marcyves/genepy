from os.path import isdir
from os import mkdir
    
class myMenu:

    def __init__(self, title, choices):
        self.title = "|  {}  |".format(title)
        self.bar = "+"+ "-" * (len(self.title)-2) + "+"
        self.title = self.bar + "\n" + self.title + "\n" + self.bar
        self.choices = choices
        self.count = len(choices)

    def show(self):
        print(self.title)
        print("")
        for index,label in enumerate(self.choices.keys()):
            print("\t{} - {}".format(index+1, label))
        print("\t- - ---------")
        print("\t0 - Exit")
        print("")
        rep = -1
        while (rep <0 or rep >self.count):
            try:
                rep = int(input("Votre choix => "))
            except:
                rep = 0

        return rep
class mySimpleMenu:

    def __init__(self, title, choices):
        self.title = "|  {}  |".format(title)
        self.bar = "+"+ "-" * (len(self.title)-2) + "+"
        self.title = self.bar + "\n" + self.title + "\n" + self.bar
        self.choices = choices
        self.count = len(choices)

    def show(self):
        print(self.title)
        print("")
        for index,label in enumerate(self.choices):
            print("\t{} - {}".format(index+1, label))
        print("\t- - ---------")
        print("\t0 - Exit")
        print("")
        rep = -1
        while (rep <0 or rep >self.count):
            try:
                rep = int(input("Votre choix => "))
            except:
                rep = 0

        return rep
class msg:

    @staticmethod
    def info(text):
        print("=== {}".format(text))

    @staticmethod
    def error(text):
        print("+++ {}".format(text))

    @staticmethod
    def title(text):
         print("\n----------------------------------------------------------------")
         print("=== {}".format(text))
         print("----------------------------------------------------------------")
