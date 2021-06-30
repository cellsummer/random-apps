from kivy.app import App
from kivy.lang import Builder
from kivy.uix.behaviors import focus
from kivymd.app import MDApp
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.properties import NumericProperty
from kivy.properties import StringProperty
from kivy.core.window import Window
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import (
    MDFlatButton,
    MDFloatingActionButton,
    MDRoundFlatButton,
    MDRaisedButton,
    MDRectangleFlatButton,
)
from kivy.utils import get_color_from_hex

from kivy.core.text import LabelBase
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivy.uix.popup import Popup
from kivymd.theming import ThemeManager
from kivymd.font_definitions import theme_font_styles
from kivy.lang import Builder
from kivymd.uix.toolbar import MDToolbar
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.menu import MDDropdownMenu
from kivymd_extensions.sweetalert.sweetalert import SweetAlert
from sudoku_cls import SudokuCls

import numpy as np

Window.size = (600, 650)


class SudokuApp(MDApp):
    # pass
    # path_to_kv_file = "Sudoku.kv"
    sudoku = SudokuCls()

    cur_cell = (0, 0)

    # Change APP colors here
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.theme_cls.primary_palette = "BlueGray"
        self.theme_cls.primary_hue = "600"
        self.theme_cls.accent_palette = "Blue"
        self.theme_cls.accent_hue = "800"
        self.theme_cls.theme_style = "Light"
        self.accent_color = [255 / 255, 64 / 255, 129 / 255, 1]

    # generate board
    # solve the board

    def build(self):

        # set font (seems not working)

        # LabelBase.register(name="JetBrainsMono", fn_regular="JetBrainsMono-Regular.ttf")
        # theme_font_styles.append("JetBrainsMono")
        # self.theme_cls.font_styles["JetBrainsMono"] = [
        #     "JetBrainsMono",
        #     16,
        #     False,
        #     0.15,
        # ]

        return MainBox()

    def callback(self):

        SweetAlert(font_style_title="H5",).fire(
            "About",
            "Sudoku v1.0.0 by Wenjing Fang",
            # type="info",
        )

        # popup = Popup(
        #     content=Label(text="Sudoku v1.0.0 by Wenjing Fang"),
        #     title="About",
        #     size_hint=(None, None),
        #     size=("400dp", "100dp"),
        # )

        # popup.open()
        # Snackbar(text="Sudoku v1.0.0 by Wenjing Fang").show()

        return


class CellInput(TextInput):
    nums = [f"{i}" for i in range(1, 10)]

    def __init__(self, x_pos, y_pos, **kwargs):
        super().__init__(**kwargs)
        self.x_pos = x_pos
        self.y_pos = y_pos
        # Formatting the cell
        self.font_family = "JetBrains Mono"
        self.font_size = "40dp"
        self.halign = "center"

    def insert_text(self, substring, from_undo=False):
        nums = self.nums
        if substring not in nums or len(self.text) > 0:
            substring = ""

        return super(CellInput, self).insert_text(substring, from_undo=from_undo)

    # def on_text_validate(self):
    #     board = MDApp.get_running_app().sudoku.board
    #     if self.text in self.nums:
    #         board[self.x_pos][self.y_pos] = int(self.text)
    #     return

    def _on_focus(self, instance, value, *largs):
        super()._on_focus(instance, value, *largs)
        MDApp.get_running_app().cur_cell = (self.x_pos, self.y_pos)
        return


class GridLayoutFrame(MDGridLayout):
    def __init__(self, frame_id, **kwargs):
        super().__init__(**kwargs)
        self.cells = []
        self.frame_id = frame_id
        self.rows = 3
        self.cols = 3
        board = MDApp.get_running_app().sudoku.puzzle

        for i in range(9):

            x_pos = self.frame_id // 3 * 3 + i // 3
            y_pos = (self.frame_id % 3) * 3 + (i % 3)

            cell = CellInput(x_pos, y_pos, multiline=False)

            if board[cell.x_pos][cell.y_pos] > 0:
                cell.disabled = True

            cell.text = (
                str(board[cell.x_pos][cell.y_pos])
                if board[cell.x_pos][cell.y_pos] > 0
                else ""
            )

            # print(self.frame_id)
            self.cells.append(cell)
            self.add_widget(cell)


class GridLayoutBoard(MDGridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.frames = [GridLayoutFrame(frame_id=i) for i in range(9)]
        for frame in self.frames:
            self.add_widget(frame)


class MainBox(MDBoxLayout):
    def get_hint(self):
        print("getting a hint...")
        app = MDApp.get_running_app()
        board = app.sudoku.puzzle
        solution = app.sudoku.solution
        grid = self.ids.grid
        # cur_cell = app.cur_cell

        r, c = app.cur_cell
        # print((r, c))
        if board[r][c] == 0:
            frame = r // 3 * 3 + c // 3
            cell = r % 3 * 3 + c % 3
            cur_cell = grid.frames[frame].cells[cell]
            if cur_cell.text == "":
                cur_cell.text = str(solution[r][c])
                cur_cell.foreground_color = get_color_from_hex("#2a6138")

            else:
                Popup(
                    content=Label(text="Choose a blank cell to get a hint"),
                    title="Message",
                    size_hint=(None, None),
                    size=("400dp", "100dp"),
                ).open()

            return

        print("It seems you have already completed the puzzle!")

    def check_board(self):
        my_solution = np.zeros(shape=(9, 9), dtype="int32")
        for frame in range(9):
            for cell in range(9):
                r = frame // 3 * 3 + cell // 3
                c = frame % 3 * 3 + cell % 3
                s = self.ids.grid.frames[frame].cells[cell].text
                my_solution[r][c] = int(s) if s != "" else 0

        solution = MDApp.get_running_app().sudoku.solution
        result = np.array_equal(solution, my_solution)

        if result:
            popup = Popup(
                content=Label(text="Congratulations! You have solved the puzzle!"),
                title="Submission",
                size_hint=(None, None),
                size=("400dp", "150dp"),
            )
            print("Congratulations! You have solved the puzzle!")
            popup.open()
        else:
            popup = Popup(
                content=Label(text="The solution is incorrect. Please check! "),
                title="Submission",
                size_hint=(None, None),
                size=("400dp", "150dp"),
            )
            print("The solution is incorrect. Please check!")
            popup.open()
        return result

    def refreshBoard(self, sudoku):
        # grid = self.ids.grid
        # toolbar = self.children[2]
        for frame in range(9):
            for cell in range(9):
                r = frame // 3 * 3 + cell // 3
                c = frame % 3 * 3 + cell % 3
                cur_cell = self.ids.grid.frames[frame].cells[cell]
                if sudoku.puzzle[r][c] > 0:
                    cur_cell.text = str(sudoku.puzzle[r][c])
                    cur_cell.disabled = True
                else:
                    cur_cell.text = ""
                    cur_cell.foreground_color = get_color_from_hex("#000000")
                    cur_cell.disabled = False
        self.ids.banner.title = f"Sudoku: {sudoku.name} - {sudoku.level}"

        return True

    def new_board(self):
        app = MDApp.get_running_app()
        app.sudoku = SudokuCls()
        # app.board = app.sudoku.puzzle
        print("creating new board...")
        self.refreshBoard(app.sudoku)

    def daily(self):
        app = MDApp.get_running_app()
        app.sudoku = SudokuCls(daily=True)
        print("creating new board for today...")
        self.refreshBoard(app.sudoku)


class ButtonsLayout(MDBoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class BannerLabel(MDToolbar):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # self.title = f"Sudoku: {name} - {level}"
        sudoku = MDApp.get_running_app().sudoku
        self.title = f"Sudoku: {sudoku.name} - {sudoku.level}"


class BannerLayout(MDBoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


if __name__ == "__main__":

    SudokuApp().run()
