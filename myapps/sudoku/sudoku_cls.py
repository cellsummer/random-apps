from dataclasses import dataclass, field
import requests
from datetime import datetime
from bs4 import BeautifulSoup
from random import randint
import numpy as np
import pandas as pd
import collections


@dataclass
class SudokuCls:
    puzzle: np.array = field(default_factory=list)
    solution: np.array = field(default_factory=list)
    level: str = field(default_factory=list)
    name: str = field(default_factory=list)

    def __init__(
        self, max_id=800, repo_file="myapps/sudoku/sudoku_repo.csv", daily=False
    ):
        self.puzzle = np.zeros((9, 9), "int32")
        self.solution = np.zeros((9, 9), "int32")

        if daily:
            today = datetime.today().strftime("%d/%m/%Y")
            url = f"http://www.sudoku.org.uk/DailySudoku.asp?day={today}"
            self.name, self.level, p = self.fetch_record(
                url,
            )
        else:
            repo = pd.read_csv(
                repo_file, names=["name", "level", "board"], dtype="object"
            )
            id = randint(0, max_id)
            self.level = str(repo.loc[id, "level"])
            self.name = str(repo.loc[id, "name"])
            p = str(repo.loc[id, "board"])

        for r in range(9):
            for c in range(9):
                self.puzzle[r][c] = p[r * 9 + c]

        self.solution = self.puzzle.copy()

        def nextCell(board: np.array) -> tuple[int, int]:
            # find next empty cell, order: row then col
            for i in range(9):
                for j in range(9):
                    if board[i][j] == 0:
                        return (i, j)

            # if the entire board is filled return None
            return

        def solveSudokuRec(board: np.array, nums: list[int], rows, cols, boxes) -> bool:
            # start solving
            cell = nextCell(board)
            if not cell:
                return True
            # print(f"solving cell ({cell[0]}, {cell[1]})")
            # solving
            r, c = cell
            for num in nums:

                if (
                    (num not in rows[r])
                    and (num not in cols[c])
                    and (num not in boxes[r // 3 * 3 + c // 3])
                ):
                    # recursion
                    rows[r].add(num)
                    cols[c].add(num)
                    boxes[r // 3 * 3 + c // 3].add(num)
                    board[r][c] = num

                    if solveSudokuRec(board, nums, rows, cols, boxes):
                        return True

                    else:
                        rows[r].discard(num)
                        cols[c].discard(num)
                        boxes[r // 3 * 3 + c // 3].discard(num)
                        board[r][c] = 0
                        continue

            # print("Completed. The board is not solvable")
            return False

        def solveSudoku(board: np.array) -> None:

            nums = [i + 1 for i in range(9)]
            # use dictionaries of set, rows, cols, boxes
            rows, cols, boxes = (
                collections.defaultdict(set),
                collections.defaultdict(set),
                collections.defaultdict(set),
            )

            for i in range(9):
                for j in range(9):
                    s = board[i][j]
                    if s != 0:
                        rows[i].add(s)
                        cols[j].add(s)
                        boxes[i // 3 * 3 + j // 3].add(s)

            solveSudokuRec(board, nums, rows, cols, boxes)

        solveSudoku(self.solution)

    def fetch_record(self, url: str, type="daily"):
        doc = requests.get(url).text
        tbl_id_map = {"daily": 4, "weekly": 3}

        board = pd.read_html(doc)[tbl_id_map[type]]

        board_line = [
            np.nan_to_num(board.iloc[i, j]).astype("int32").astype("str")
            for i in range(9)
            for j in range(9)
        ]

        soup = BeautifulSoup(doc, "lxml")
        if type == "daily":
            name, level = soup.p.font.text.split(",")
        elif type == "weekly":
            name, level = soup.body.td.find_all("font")[1].text.split(",")
        else:
            return

        print(f"Successfully fetched {name} ...")

        return name, level, board_line
