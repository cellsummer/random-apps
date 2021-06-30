import enum
from kivymd.uix.bottomnavigation import MDBottomNavigationItem
from kivymd.uix.gridlayout import MDGridLayout
from kivy.uix.gridlayout import GridLayout
from kivy.core.audio import SoundLoader
from kivymd.uix.button import MDRaisedButton
from kivy.uix.button import Button
from kivymd.app import MDApp
from kivy.utils import get_color_from_hex
from kivy.uix.popup import Popup
from kivy.uix.label import Label
import utils
from random import randint
import numpy as np
from datetime import datetime
import os
import sys
import json

utils.load_kv("btnav_three.kv")
root_dir = os.path.split(os.path.abspath(sys.argv[0]))[0]
utils.load_kv("btnav_one.kv")


class BTNavOne(MDBottomNavigationItem):
    """
    Bottom Navigation Item One.
    """


class Cell(Button):
    colors = {
        0: get_color_from_hex("#ddede1"),
        1: get_color_from_hex("#009966"),
        2: get_color_from_hex("#f0dd35"),
        3: get_color_from_hex("#f05435"),
    }

    # background_color = get_color_from_hex("#ddede1")
    # md_bg_color = (1, 0, 1, 1)
    color = get_color_from_hex("#000000")
    font_family = "times"
    font_size = 40
    size_hint = (1, 1)
    background_normal = ""
    # size = (60, 60)
    # size_hint = (1, 1)

    def __init__(self, x_pos=0, y_pos=0, val=0, **kwargs):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.val = val
        self.text = str(val)
        self.background_color = self.colors[self.val]
        super().__init__(**kwargs)

    def on_press(self):
        self.play_sound()
        self.val += -1 if self.val > 0 else 3
        self.update()
        board = self.parent

        for (inc_x, inc_y) in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nx = self.x_pos + inc_x
            ny = self.y_pos + inc_y
            if nx >= 0 and nx < 6 and ny >= 0 and ny < 6:
                cell = board.cells[nx][ny]
                cell.val += -1 if cell.val > 0 else 3
                cell.update()

        self.check_complete()

    def update(self):
        self.text = str(self.val)
        self.background_color = self.colors[self.val]

        return super().on_press()

    def check_complete(self):
        self.parent.check_complete()

    def play_sound(self):
        sound = SoundLoader.load("assets/sounds/click.wav")
        sound.play()


class Board(GridLayout):
    cells = []
    puzzle = np.zeros(shape=(6, 6), dtype="int32")
    start_time = 0
    complete_time = 0
    record_seconds = 999
    # level = 10

    def __init__(self, level=10, **kwargs):
        super().__init__(**kwargs)
        self.cells = [[Cell(row, col) for col in range(6)] for row in range(6)]
        self.level = level
        for row in self.cells:
            for cell in row:
                self.add_widget(cell)
        self.read_leaderboard()
        self.generate()

    def check_complete(self):
        if sum([cell.val for row in self.cells for cell in row]) == 0:
            self.complete_time = datetime.now()
            self.record_seconds = (self.complete_time - self.start_time).total_seconds()
            # Update leaderboard
            self.update_leaderboard()

            # show the popup
            close_btn = Button(text="close")
            popup = Popup(
                title="Congrats!",
                content=Label(
                    text=f"You have conmpleted in {int(self.record_seconds)} seconds. \n Click anywhere to start a new game."
                ),
                # content=close_btn,
                size_hint=(None, None),
                size=("400dp", "100dp"),
                auto_dismiss=True,
            )

            def restart(instance):
                self.generate()

            # close_btn.bind(on_press=popup.dismiss)
            popup.bind(on_dismiss=restart)
            popup.open()
            # self.generate()
            return True
        return False

    def reset(self):
        for row in self.cells:
            for cell in row:
                cell.val = self.puzzle[cell.x_pos][cell.y_pos]
                cell.update()

    def generate(self):

        self.puzzle = np.zeros((6, 6), "int32")

        def click(puzzle):
            r, c = randint(0, 5), randint(0, 5)
            puzzle[r][c] += 1

            for (inc_x, inc_y) in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                nr = r + inc_x
                nc = c + inc_y
                if nr >= 0 and nr < 6 and nc >= 0 and nc < 6:
                    puzzle[nr][nc] += 1

        for _ in range(self.level):
            click(self.puzzle)
            self.puzzle = self.puzzle % 4

        for row in self.cells:
            for cell in row:
                cell.val = self.puzzle[cell.x_pos][cell.y_pos]
                cell.update()

        self.start_time = datetime.now()

    def update_leaderboard(self):
        cur = self.leaderboard[("easy" if self.level == 10 else "hard")]
        # print("current leaderboard", cur)
        # for i in range(3):
        if self.record_seconds < cur["results"][2]:

            cur["results"][2] = self.record_seconds
            cur["names"][2] = MDApp.get_running_app().username
            zipped = list(zip(cur["names"], cur["results"]))
            zipped.sort(key=lambda x: x[1])
            cur["names"], cur["results"] = zip(*zipped)
            cur["results"] = list(cur["results"])
            cur["names"] = list(cur["names"])
        # write to the json file
        with open(os.path.join(root_dir, "leaderboard.json"), "w") as f:
            json.dump(self.leaderboard, f, indent=4)

        return True

    def read_leaderboard(self):
        with open(os.path.join(root_dir, "leaderboard.json")) as f:
            self.leaderboard = json.load(f)


class Board_Easy(Board):
    def __init__(self, **kwargs):
        super().__init__(level=10, **kwargs)


class Board_Hard(Board):
    def __init__(self, **kwargs):
        super().__init__(level=20, **kwargs)
