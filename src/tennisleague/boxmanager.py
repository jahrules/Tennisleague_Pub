import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW, LEFT, RIGHT
from .DB.dbinterface import DBInterface
from .boxes.scoreinput import ScoreInput
from .boxes.rankings import Rankings
from .boxes.errorbox import ErrorBox
from .boxes.newleague import NewLeague
from .boxes.newplayer import NewPlayer

class BoxManager:

    def __init__(self, mainwindow):
        self.__MainWindow = mainwindow
        self.__RootBox = toga.Box()
        self.__ErrBox = ErrorBox(self.ActivateBox)
        self.__ActiveBox = "HomeBox"
        self.__HomeBox = "HomeBox"
        self.__LastBox = "HomeBox"
        self.__d_Boxes = dict()
        self.__database = DBInterface()

    def ReturnHome(self, rebuild=False):
        if rebuild == True:
            self.__d_Boxes["HomeBox"] = self.__BuildHomeBox(self.__database.get_nums())

        self.__RootBox.remove(self.__d_Boxes[self.__ActiveBox])
        self.__RootBox.add(self.__d_Boxes[self.__HomeBox])
        self.__LastBox = self.__ActiveBox
        self.__ActiveBox = "HomeBox"

    def ReturnLast(self):
        self.__RootBox.remove(self.__d_Boxes[self.__ActiveBox])
        self.__RootBox.add(self.__d_Boxes[self.__LastBox])
        savelast = self.__LastBox
        self.__LastBox = self.__ActiveBox
        self.__ActiveBox = savelast

    def ActivateBox(self, boxname):
        self.__RootBox.remove(self.__d_Boxes[self.__ActiveBox])
        self.__RootBox.add(self.__d_Boxes[boxname])
        self.__LastBox = self.__ActiveBox
        self.__ActiveBox = boxname

    def __BuildHomeBox(self, playerinfo):
        root = toga.Box()
        root.style.update(direction=ROW,flex=1)

        rankobj = Rankings(playerinfo)
        rankbox = rankobj.Build()

        menuobj = MainMenu(self.ActivateBox)
        menubox = menuobj.Build()

        root.add(rankbox)
        root.add(menubox)

        return root

    def BuildBoxes(self):
        self.__RootBox.style.update(direction=ROW)

        d_Players = self.__database.get_playerdict()

        self.__d_Boxes["HomeBox"] = self.__BuildHomeBox(self.__database.get_nums())
        
        scorebox = ScoreInput(d_Players, self.__database, self.ReturnHome, self.__ErrorHandler)
        self.__d_Boxes["ScoreInput"] = scorebox.Build()

        newbox = NewLeague(self.__database, self.ReturnHome, self.ActivateBox, self.__ErrorHandler)
        self.__d_Boxes["NewSeason"] = newbox.Build()

        newplayer = NewPlayer(self.__database, self.ReturnLast, self.__ErrorHandler)
        self.__d_Boxes["NewPlayer"] = newplayer.Build()
        
        self.__RootBox.add(self.__d_Boxes["HomeBox"])

        self.__MainWindow.content = self.__RootBox
        self.__MainWindow.show()

    def __ErrorHandler(self,errmsg="Unknown Error",fatalflg=False,returnwin="HomeBox"):
        if fatalflg == True:
            self.__d_Boxes["ErrorBox"] = self.__ErrBox.Build(errmsg, returnwin)
            self.ActivateBox("ErrorBox")
        else:
            self.__MainWindow.info_dialog(
                'Error:',
                errmsg
            )

class MainMenu:
    
    def __init__(self, handler):
        self.__handler = handler
        self.__RootBox = toga.Box()

    def Build(self):
        self.__RootBox.style.update(direction=COLUMN, alignment=LEFT)

        resultsbox = toga.Box()
        resultsbox.style.update(direction=ROW, alignment=RIGHT)
        button = toga.Button(
            'Input Scores',
            on_press=self.show_input_window,
            style=Pack(alignment=RIGHT, padding=5)
        )
        resultsbox.add(button)

        self.__RootBox.add(resultsbox)

        leaguebox = toga.Box()
        leaguebox.style.update(direction=ROW, alignment=RIGHT)
        button = toga.Button(
            'New Season',
            on_press=self.new_season_window,
            style=Pack(alignment=RIGHT, padding=5)
        )
        leaguebox.add(button)

        self.__RootBox.add(leaguebox)

        newpbox = toga.Box()
        newpbox.style.update(direction=ROW, alignment=RIGHT)
        button = toga.Button(
            'Add Player',
            on_press=self.new_player_window,
            style=Pack(alignment=RIGHT, padding=5)
        )
        newpbox.add(button)

        self.__RootBox.add(newpbox)

#        testbox = toga.Box()
#        testbox.style.update(direction=ROW, alignment=RIGHT)
#        check = toga.Checkbox()
#        testbox.add(check)
#
#        self.__RootBox.add(testbox)

        return self.__RootBox

# todo: make this function more generic so it can take multiple handlers.
    def show_input_window(self, widget):
        self.__handler("ScoreInput")
        
    def new_season_window(self, widget):
        self.__handler("NewSeason")

    def new_player_window(self, widget):
        self.__handler("NewPlayer")




