"""
Tennis League manager
"""
import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW, LEFT, RIGHT
from tennisleague import BoxManager

class TennisLeague(toga.App):

    def startup(self):
        self.main_window = toga.MainWindow(title=self.formal_name)

        Display = BoxManager(self.main_window)
        Display.BuildBoxes()

def main():
    return TennisLeague()
