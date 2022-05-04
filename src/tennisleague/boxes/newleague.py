import datetime
import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW, LEFT, RIGHT
from ..DB.dbinterface import DBInterface

class NewLeague:

    def __init__(self, database, homehandler, childhandler, errhandler):
        self.__database = database
        self.__Returnhandler = homehandler
        self.__Childhandler = childhandler
        self.__errhandler = errhandler

    def Build(self):
        self.__Update_Nums()

        main_box = toga.Box()
        main_box.style.update(direction=COLUMN, padding_top=10, flex=1)

        main_box.add(self.__Build_RowOne())
        main_box.add(self.__Build_RowTwo())
        main_box.add(self.__Build_Chooser())

        return main_box

    def __Update_Nums(self):
        self.__playerinfo = self.__database.get_nums()

    def __Build_RowOne(self):
        row1_box = toga.Box()
        row1_box.style.update(direction=ROW, padding_left=5, flex=1)

        row1_box.add(self.__Build_Label("League Name: "))

        title_inputbox = toga.Box()
        title_inputbox.style.update(direction=COLUMN, alignment=RIGHT, padding_left=5, flex=1)
        self.__title_input = toga.TextInput(style=Pack(width=150, alignment=RIGHT, padding=(0,2), flex=1))
        title_inputbox.add(self.__title_input)

        row1_box.add(title_inputbox)

        return row1_box

    def __Build_RowTwo(self):
        row2_box = toga.Box()
        row2_box.style.update(direction=ROW, padding_left=5, padding_top=10, flex=1)

        column1_box = toga.Box()
        column1_box.style.update(direction=COLUMN, padding_left=5, flex=1)

        weeks_input = toga.Box()

        weeks_input.style.update(direction=ROW, padding_left=5, flex=1)
        weeks_input.add(self.__Build_Label("Weeks: "))
        self.__weeks_input = toga.TextInput(style=Pack(width=40, alignment=RIGHT, padding=(0,2), flex=1))
        weeks_input.add(self.__weeks_input)

        column1_box.add(weeks_input)

        bonusgames_input = toga.Box()

        bonusgames_input.style.update(direction=ROW, padding_left=5)
        bonusgames_input.add(self.__Build_Label("Bonus Games: "))
        self.__bonusgames = toga.TextInput(style=Pack(width=27,padding=(0,2)))
        bonusgames_input.add(self.__bonusgames)

        column1_box.add(bonusgames_input)

        row2_box.add(column1_box)

        column2_box = toga.Box()
        column2_box.style.update(direction=COLUMN, padding_left=15)

        courts_input = toga.Box()

        courts_input.style.update(direction=ROW, padding_left=5)
        courts_input.add(self.__Build_Label("Courts: "))
        self.__courts_input = toga.NumberInput(min_value=1, max_value=3)
        courts_input.add(self.__courts_input)

        column2_box.add(courts_input)

        date_input = toga.Box()
        date_input.style.update(direction=ROW, padding_left=5)
        date_input.add(self.__Build_Label("Start Date: "))
#        self.__date = toga.DatePicker()
#        date_input.add(self.__date)

        column2_box.add(date_input)

        row2_box.add(column2_box)

        return row2_box

    def __Build_Label(self, text):
        label_box = toga.Box()
        label_box.style.update(direction=ROW)
        label_name = toga.Label(text)
        label_box.add(label_name)

        return label_box

    def __Build_Chooser(self):
        main_box = toga.Box()
        main_box.style.update(direction=ROW,flex=1)

        menubox = toga.Box()
        menubox.style.update(direction=COLUMN,padding_left=10,flex=1)

        menubox.add(self.__Build_MenuItem("Add Player",self.__ActivateChild))
        menubox.add(self.__Build_MenuItem("Submit",self.__Return))
        menubox.add(self.__Build_MenuItem("Return Home",self.__Return))

        main_box.add(menubox)

        player_box = toga.Box()
        player_box.style.update(direction=COLUMN)

        for player in self.__playerinfo:
            playerbox = toga.Box()
            playerbox.style.update(direction=COLUMN, alignment=RIGHT, padding=5)

            player_label = toga.Switch(label=player[0], style=Pack(alignment=RIGHT,padding=(1,5),flex=1))

            playerbox.add(player_label)
            player_box.add(playerbox)

        #scroller = toga.ScrollContainer(content=player_box,horizontal=False)
        scroller = toga.ScrollContainer(content=player_box)
        scroller.style.update(direction=COLUMN, flex=1)
        main_box.add(scroller)

        main_box.add(menubox)

        return main_box

    def __Build_MenuItem(self, label, action):
        itembox = toga.Box()
        itembox.style.update(direction=ROW)

        button = toga.Button(
            label,
            on_press=action,
            style=Pack(padding=5)
        )
        itembox.add(button)

        return itembox

    def __Return(self, widget):
        self.__Returnhandler()

    def __ActivateChild(self, widget):
        self.__Childhandler("NewPlayer")




