import datetime
import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW, LEFT, RIGHT

class ScoreInput:

    def __init__(self, d_Players, dbint, handler, errhandler, courts=3, bonusgames=2):
        self.__d_Players = d_Players
        self.__database = dbint
        self.__Returnhandler = handler
        self.__errhandler = errhandler
        self.__courts = courts
        self.__bonusgames = bonusgames

        listfront = [" ",]
        self.__a_Players = listfront + list(self.__d_Players)

        self.__win_p_boxes = []
        self.__lose_p_boxes = []
        self.__win_s_boxes = []
        self.__lose_s_boxes = []
        self.__result = []
        self.__root = ""


    def Build(self):
        main_box = toga.Box()
        main_box.style.update(direction=COLUMN, padding_top=10)

#        date_box = toga.Box()
#        date_box.style.update(direction=ROW, padding_left=5)

#        self.date_chooser = toga.DatePicker(initial=datetime.date.today())
#        date_box.add(self.date_chooser)

#        main_box.add(date_box)

        court_boxes = toga.Box()
        court_boxes.style.update(direction=COLUMN, padding_left=5)
        for i in range(self.__courts):
            court_root_box = toga.Box()
            court_root_box.style.update(direction=COLUMN, padding_bottom=10)

            courtlabel_box = toga.Box()
            courtlabel_box.style.update(direction=ROW)
            court_num = "Court {}:".format(int(i + 1))
            court_label = toga.Label(court_num)
            court_label.style.update(font_weight='bold')
            courtlabel_box.add(court_label)

            court_root_box.add(courtlabel_box)

            player_labels = []
            player_labels.append(toga.Label('Winning Players:'))
            player_labels.append(toga.Label('Losing Players:'))

            court_box = toga.Box()
            court_box.style.update(direction=ROW, padding_right=5)

            line_box = toga.Box()
            line_box.style.update(flex=1,direction=COLUMN, padding_left=5, padding_bottom=2)
            for j in [0, 1]:
                line_box.add(player_labels[j])

                c = []
                select_box = toga.Box()
                select_box.style.update(direction=ROW)

                for k in [0, 1]:
                    selection = toga.Box()
                    selection.style.update(flex=1,direction=COLUMN,padding_left=5)
                    c.append(toga.Selection(on_select=self._refresh_select,items=self.__a_Players,style=Pack(flex=1, width=175)))
                    selection.add(c[k])
                    select_box.add(selection)

                if j == 0:
                    self.__win_p_boxes.append(c)
                else:
                    self.__lose_p_boxes.append(c)

                line_box.add(select_box)

            court_box.add(line_box)

            score_labels = []
            score_labels.append(toga.Label('Score: '))
            score_labels.append(toga.Label(''))

            score_box = toga.Box()
            score_box.style.update(direction=COLUMN, padding_left=5)
            for j in [0, 1]:
                score_box.add(score_labels[j])

                c = []
                set_box = toga.Box()
                set_box.style.update(direction=ROW)

                for k in [0, 1, 2]:
                    c.append(toga.TextInput(placeholder='0',style=Pack(width=27,padding=(0,2))))
                    set_box.add(c[k])

                if j == 0:
                    self.__win_s_boxes.append(c)
                else:
                    self.__lose_s_boxes.append(c)

                score_box.add(set_box)

            court_box.add(score_box)
            court_root_box.add(court_box)
            court_boxes.add(court_root_box)

        main_box.add(court_boxes)

        lastrow = toga.Box()
        lastrow.style.update(direction=ROW)

        button = toga.Button(
            'Submit',
            on_press=self.__Submission,
            style=Pack(padding=5)
        )

        lastrow.add(button)

        button2 = toga.Button(
            'Return Home',
            on_press=self.__Return,
            style=Pack(padding=5)
        )

        lastrow.add(button2)

        main_box.add(lastrow)

        self.__root = toga.ScrollContainer(content=main_box, vertical=False)
        self.__root.style.update(direction=COLUMN,flex=1)

        return self.__root

    def getBox(self):
        return self.__root

    def _refresh_select(self, widget):
        widget.refresh()

    def __Submission(self, widget):
#        date = self.date_chooser.value
        date = "Apr 14"

        for i in range(self.__courts):
            winning_players = []
            winning_scores = []
            losing_players = []
            losing_scores = []

            for player in self.__win_p_boxes[i]:
                if player.value != ' ':
                    winning_players.append(player.value)
            for score in self.__win_s_boxes[i]:
                if score.value != '':
                    winning_scores.append(score.value)

            for player in self.__lose_p_boxes[i]:
                if player.value != ' ':
                    losing_players.append(player.value)
            for score in self.__lose_s_boxes[i]:
                if score.value != '':
                    losing_scores.append(score.value)

#validate input here
            if len(winning_players) <= 1 or len(losing_players) <= 1:
                self.__handle_error("Must select players") 
                return

            d_Court = {
                "winners": tuple(winning_players),
                "winscores": tuple(winning_scores),
                "losers": tuple(losing_players),
                "losescores": tuple(losing_scores)
            }

            self.__result.append(d_Court.copy())

#        self._calc_games(date.strftime('%d %b'))
        self.__calc_games(date)

    def __calc_games(self, date):
        scores = []

        for court in self.__result:
            wingames = 0
            losegames = 0
            for score in court['winscores']:
                wingames = wingames + int(score)

            for score in court['losescores']:
                losegames = losegames + int(score)

            adjustedgames = wingames + self.__bonusgames
            for player in court['winners']:
                if self.__d_Players[player] == 1:
                    scores.append((player,adjustedgames,losegames))
                else:
                    scores.append((player,wingames,losegames))

            for player in court['losers']:
                scores.append((player,losegames,wingames))

        try:
            self.__database.Update_Scores(scores, date)
            self.__database.Update_Numbers()
        except:
            self.__handle_error("Error updating database",True)
        self.__Returnhandler(True)

    def __Return(self, widget):
        self.__Returnhandler()

    def __handle_error(self, errmsg, fatalflg=False):
        self.__errhandler(errmsg,fatalflg)
