import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW, LEFT, RIGHT

class NewPlayer:

    def __init__(self, database, handler, errhandler):
        self.__Database = database
        self.__Returnhandler = handler
        self.__errhandler = errhandler
        

    def Build(self):
        main_box = toga.Box()
        main_box.style.update(direction=COLUMN, padding_top=10)

        main_box.add(self.__Build_Title())

        name_box = toga.Box()
        name_box.style.update(direction=ROW, padding_left=5)
        name_label = toga.Label("Name: ")
        name_box.add(name_label)
        self.__nameinput = toga.TextInput(style=Pack(width=150))
        name_box.add(self.__nameinput)

        main_box.add(name_box)

        number_box = toga.Box()
        number_box.style.update(direction=ROW, padding_left=5)
        number_label = toga.Label("Starting Number: ")
        number_box.add(number_label)
        self.__numberinput = toga.TextInput(style=Pack(width=60))
        number_box.add(self.__numberinput)

        main_box.add(number_box)

        padding_box = toga.Box()
        padding_box.style.update(direction=ROW, padding_left=5)
        padding_label = toga.Label("Padding Games: ")
        padding_box.add(padding_label)
        self.__paddinginput = toga.TextInput(style=Pack(width=60))
        padding_box.add(self.__paddinginput)

        main_box.add(padding_box)

        button_box = toga.Box()
        button_box.style.update(direction=ROW, padding_left=5)
        submit_button = toga.Button(
            "Submit",
            on_press=self._processinput,
            style=Pack(padding=5)
        )
        button_box.add(submit_button)
        return_button = toga.Button(
            "Return",
            on_press=self.__Return,
            style=Pack(padding=5)
        )
        button_box.add(return_button)

        main_box.add(button_box)

        return main_box
        

    def __Build_Title(self):
        main_box = toga.Box()
#        main_box.style.update(direction=COLUMN, flex=1, alignment=CENTER)
        main_box.style.update(direction=COLUMN, flex=1)

        title = toga.Label("Add a Player")
        title.style.update(font_weight='bold')

        main_box.add(title)

        return main_box

    def _processinput(self, widget):
        self.__name = self.__nameinput.value
        self.__number = self.__numberinput.value
        self.__padding = self.__paddinginput.value
        
        """make a call to database here"""

    def __Return(self, widget):
        self.__Returnhandler()
