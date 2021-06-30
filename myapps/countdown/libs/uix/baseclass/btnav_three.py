import enum
from kivymd.uix.bottomnavigation import MDBottomNavigationItem

from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout

from kivy.properties import ListProperty, StringProperty
import utils
import json
import os
import sys

utils.load_kv("btnav_three.kv")
root_dir = os.path.split(os.path.abspath(sys.argv[0]))[0]


class BTNavThree(MDBottomNavigationItem):
    """
    Bottom Navigation Item Three.
    """

    def on_enter(self, *args):
        self.children[0].load()
        leaderboard = self.children[0].leaderboard
        standings = self.children[0].children[0].children

        # Update standings manually for now

        def convert_board(level="easy", idx=0):

            name = leaderboard[level]["names"][idx]
            result = leaderboard[level]["results"][idx]
            result = str(int(result))
            result = f"{result} seconds"

            return name, result

        for i in range(3):
            standings[i].text, standings[i].secondary_text = convert_board(
                level="hard", idx=-(i + 1)
            )

            standings[i + 4].text, standings[i + 4].secondary_text = convert_board(
                level="easy", idx=-(i + 1)
            )

        return super().on_enter(*args)


class LeaderboardView(BoxLayout):
    def __init__(self, **kwargs):
        self.load()
        super().__init__(**kwargs)

    def load(self):
        with open(os.path.join(root_dir, "leaderboard.json")) as f:
            self.leaderboard = json.load(f)
