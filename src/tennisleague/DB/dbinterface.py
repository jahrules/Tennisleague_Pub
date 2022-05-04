import sqlite3
import openpyxl
import re
import os

dirname = os.path.dirname(__file__)
s_DB = os.path.join(dirname, "Tennis.db")
s_Sheet = os.path.join(dirname, "Tennis_Example.xlsx")

class DBInterface:

    def __init__(self):
        #sql objects
        self.__conn = sqlite3.connect(s_DB)
        self.__cursor = self.__conn.cursor()

        #excel objects
        self.__wb = openpyxl.load_workbook(filename = s_Sheet)
        self.__ws = self.__wb.active

        #if I ever build a 'new sheet' function I need to look at setting these better
        self.__s_StartCol = "J"
        self.__s_EndCol = "BA"

#SQL Queries

    def get_playerdict(self):
        query = "SELECT Name, Active FROM Players"
        self.__cursor.execute(query)

        return dict(tuple(self.__cursor.fetchall()))

    def get_playernames(self):
        query = "SELECT Name FROM Players"
        self.__cursor.execute(query)

        return self.__cursor.fetchall()

    def get_nums(self):
        query = """SELECT Name, Number
            FROM Players ORDER BY Number DESC"""
        self.__cursor.execute(query)

        return self.__cursor.fetchall()

#SQL Updates

    def __insert_num(self, querydata):
        query = """UPDATE Players set Number = (?)
                WHERE Name = (?)"""

        self.__cursor.execute(query, querydata)
        self.__conn.commit()

        return 1

#Excel Functions

    def Update_Numbers(self):
        playernames = self.get_playernames()

        for row in playernames:
                player = row[0]
                cells = self.__search(player)

                xlrow = cells[0].row
                num = self.__calc_num(xlrow)

                t_Info = tuple([num, player])
                self.__insert_num(t_Info)

        return 1

    def __calc_num(self, row):
        won = self.__sum_row(row)
        row = int(row) + 1 
        lost = self.__sum_row(row)

        total = won + lost

        number = (won / total) * 1000

        return number

    def __search(self, term):
        l_Cells = []
        for a in self.__ws.rows:
                row = tuple(a)
                for cell in row:
                        if re.search(term, str(cell.value), re.IGNORECASE):
                                l_Cells.append(cell)

        return l_Cells

    def __sum_row(self, row):
        start = "{}{}".format(self.__s_StartCol, row)
        end = "{}{}".format(self.__s_EndCol,row)

        cells = self.__ws[start:end][0]

        count = 0
        for num in cells:
                if 'None' not in str(num.value):
                        count = count + float(str(num.value))

        return count

    def Update_Scores(self, scores, date):
        loc_col = self.__search(date)

        if len(loc_col) == 0:
                print("Date not found in workbook")
                return 0

        col = loc_col[0].column_letter

        for score in scores:
                loc_row = self.__search(score[0])
                winrow = loc_row[0].row
                lossrow = str(int(winrow + 1))

                wincell = "{}{}".format(col, winrow)
                losscell = "{}{}".format(col, lossrow)

                self.__ws[wincell] = score[1]
                self.__ws[losscell] = score[2]

        self.__wb.save(s_Sheet)

        return 1
