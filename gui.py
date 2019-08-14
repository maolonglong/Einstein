# -*- coding: utf-8 -*-
# author: MaoLongLong
# date: 2019/8/14
import numpy as np
import tkinter as tk
from mcts.node import MonteCarloTreeSearchNode
from mcts.search import MonteCarloTreeSearch
from mcts.einstein import State


class Board(tk.Tk):
    arr = np.array([[6, 5, 1, 0, 0],
                    [4, 3, 0, 0, 0],
                    [2, 0, 0, 0, -3],
                    [0, 0, 0, -5, -1],
                    [0, 0, -4, -2, -6]])
    empty = 0
    _focus = None

    def __init__(self):
        super(Board, self).__init__()

        self.title('Einstein')
        self.maxsize(480, 500)
        self.minsize(480, 500)

        self.cv = tk.Canvas(self)
        self.cv.pack(fill=tk.BOTH, expand=tk.YES)
        self.cv.create_rectangle(10, 10, 470, 470,
                                 outline='white', fill='green')
        for i in range(20, 461, 88):
            self.cv.create_line(20, i, 460, i, width=3, fill='gray')
            self.cv.create_line(i, 20, i, 460, width=3, fill='gray')

        # self.print_chess(0, 0, 'red', 1)
        # self.print_chess(0, 1, 'red', 2)
        # self.print_chess(0, 2, 'red', 3)
        # self.print_chess(1, 0, 'red', 4)
        # self.print_chess(1, 1, 'red', 5)
        # self.print_chess(2, 0, 'red', 6)
        # self.print_chess(2, 4, 'blue', -1)
        # self.print_chess(3, 3, 'blue', -2)
        # self.print_chess(3, 4, 'blue', -3)
        # self.print_chess(4, 2, 'blue', -4)
        # self.print_chess(4, 3, 'blue', -5)
        # self.print_chess(4, 4, 'blue', -6)
        self.show_board()

        self.cv.bind("<Button-1>", self.on_left_click)  # 左键点击事件
        self.cv.bind("<Button-3>", self.on_right_click)  # 右键点击事件

        menu_bar = tk.Menu(self)
        menu_menu = tk.Menu(menu_bar)
        menu_menu.add_command(label='print board', command=Board.print_board)
        menu_menu.add_command(label='print focus', command=Board.print_focus)
        menu_bar.add_cascade(label='menu', menu=menu_menu)
        self.config(menu=menu_bar)

        tk.Label(self, text="author: MaoLongLong").pack(side=tk.BOTTOM)

    def print_chess(self, i, j, color, key, line='green'):
        x1, y1 = j * 88 + 30, i * 88 + 30
        x2, y2 = x1 + 68, y1 + 68
        if color == 'empty':
            Board.arr[i][j] = Board.empty
            self.cv.create_oval(x1, y1, x2, y2, fill='green', outline=line,
                                width=3)
        else:
            self.cv.create_oval(x1, y1, x2, y2, fill=color, outline=line,
                                width=3)
        Board.arr[i][j] = key

    def show_board(self):
        for i in range(5):
            for j in range(5):
                if Board.arr[i][j] != Board.empty:
                    color = 'red' if Board.arr[i][j] > 0 else 'blue'
                    self.print_chess(i, j, color, Board.arr[i][j])
                else:
                    self.print_chess(i, j, 'empty', 0)

    @staticmethod
    def print_board():
        print(Board.arr)

    @staticmethod
    def print_focus():
        print(Board._focus)

    def on_left_click(self, event):
        i = (event.y - 20) // 88
        j = (event.x - 20) // 88
        if Board.arr[i][j] != Board.empty:
            if Board._focus is not None:
                tp = Board._focus
                self.print_chess(tp[0], tp[1], tp[2], tp[3])
            if Board.arr[i][j] > 0:
                Board._focus = (i, j, 'red', Board.arr[i][j])
                self.print_chess(i, j, 'red', Board.arr[i][j], 'black')
            else:
                Board._focus = (i, j, 'blue', Board.arr[i][j])
                self.print_chess(i, j, 'blue', Board.arr[i][j], 'black')

    @staticmethod
    def get_key():
        return np.random.randint(1, 7)

    def on_right_click(self, event):
        i = (event.y - 20) // 88
        j = (event.x - 20) // 88
        if Board._focus is not None:
            tp = Board._focus
            Board._focus = None
            self.print_chess(tp[0], tp[1], 'empty', 0)
            self.print_chess(i, j, tp[2], tp[3])
            print('start...')
            key = Board.get_key()
            print(key)
            state = State(Board.arr, -1, key)
            node = MonteCarloTreeSearchNode(state)
            mcts = MonteCarloTreeSearch(node)
            Board.arr = mcts.best_action().state.board
            self.show_board()
            print('end...')


if __name__ == '__main__':
    board = Board()
    board.mainloop()
