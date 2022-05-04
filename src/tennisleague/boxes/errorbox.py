import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW, LEFT, RIGHT

class ErrorBox:

    def __init__(self, returnbox):
        self.__ReturnHandler = returnbox

    def Build(self, error_msg, returnwin="HomeBox"):
        self.__RootBox = toga.Box()
        self.__ReturnBox = returnwin

        self.__RootBox.style.update(direction=COLUMN)

        labelbox = toga.Box()
        labelbox.style.update(direction=ROW)
        errorheader = toga.Label("ERROR!:")
        errorheader.style.update(font_weight='bold')
        labelbox.add(errorheader)

        self.__RootBox.add(labelbox)

        messagebox = toga.Box()
        messagebox.style.update(direction=ROW, padding_left=5)
        errormessage = toga.Label(error_msg)
        messagebox.add(errormessage)

        self.__RootBox.add(messagebox)

        returnbox = toga.Box()
        returnbox.style.update(direction=ROW)
        returnbutton = toga.Button('Return', on_press=self.__exiterr)
        returnbox.add(returnbutton)

        self.__RootBox.add(returnbox)

        return self.__RootBox

    def __exiterr(self, widget):
        self.__ReturnHandler(self.__ReturnBox)
