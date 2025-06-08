from os.path import isdir
from os import mkdir

class saveFolder:

    def __init__(self, folder):
        self.main_folder = folder        
        self.check(folder)

    def check(self, folder):
        if not isdir(folder):
            print("\n\t=== Create Folder "+ folder)
            mkdir(folder)
            return True
        else:
            return False

    def setSubFolder(self, folder):
        folder = folder.split("/")[0]
    #        folder = folder.replace("/", "_")
        self.save_folder = self.main_folder + "/" + folder
        return self.check(self.save_folder)

    def getSubFolder(self):
        return self.save_folder + "/"
    
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
