import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW, LEFT, RIGHT

class Rankings:

    def __init__(self, playerinfo):
        self.__playerinfo = playerinfo
        self.__root = ""

    def Build(self):
        self.__root = toga.Box()
        self.__root.style.update(direction=COLUMN, padding_top=10)
        for player in self.__playerinfo:
            playerbox = toga.Box()

            score_label = toga.Label(player[1][0:3], style=Pack(padding=(0,5), width = 75))
            player_label = toga.Label(player[0], style=Pack(padding=(0,5)))

            playerbox.add(score_label)
            playerbox.add(player_label)

            playerbox.style.update(direction=ROW, padding=5)

            self.__root.add(playerbox)

        scroller = toga.ScrollContainer(content=self.__root,horizontal=False)
        scroller.style.update(direction=COLUMN,flex=1)

        return scroller
