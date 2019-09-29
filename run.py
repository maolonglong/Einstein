# -*- coding: utf-8 -*-
# author: MaoLongLong
# date: 2019/9/12
# -*- coding: utf-8 -*-
# author: MaoLongLong
# date: 2019/8/13
import tkinter as tk

import numpy as np

from mcts.einstein import State
from mcts.node import MonteCarloTreeSearchNode
from mcts.search import MonteCarloTreeSearch


class Game(tk.Tk):  # TODO 增加先手
    first = None
    board = None
    empty = 0
    _focus = None

    def __init__(self):
        super(Game, self).__init__()
        self.cv = tk.Canvas(self)
        self.setup_board()
        self.setup_ui()

    def setup_board(self):
        select = input('是否先手? ')
        Game.first = True if select == 'y' else False
        if Game.first:
            Game.board = np.array([
                [6, 2, 4, 0, 0],
                [1, 5, 0, 0, 0],
                [3, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0]
            ])
            print('我方摆放: ')
            print(Game.board)
            chess = input('对方摆放: ')
            Game.board[2][4] = -int(chess[0])
            Game.board[3][3] = -int(chess[1])
            Game.board[3][4] = -int(chess[2])
            Game.board[4][2] = -int(chess[3])
            Game.board[4][3] = -int(chess[4])
            Game.board[4][4] = -int(chess[5])
            print(Game.board)
            key = int(input('我方色子: '))
            state = State(Game.board, 1 if Game.first else -1, key)
            node = MonteCarloTreeSearchNode(state)
            tree = MonteCarloTreeSearch(node)
            Game.board = tree.best_action()
            self.show_board()
            print(Game.board)

        else:
            Game.board = np.array([
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, -3],
                [0, 0, 0, -5, -1],
                [0, 0, -4, -2, -6]
            ])
            print('我方摆放: ')
            print(Game.board)
            chess = input('对方摆放: ')
            Game.board[0][0] = int(chess[0])
            Game.board[0][1] = int(chess[1])
            Game.board[0][2] = int(chess[2])
            Game.board[1][0] = int(chess[3])
            Game.board[1][1] = int(chess[4])
            Game.board[2][0] = int(chess[5])
            print(Game.board)

    def setup_ui(self):
        self.title('Einstein')
        self.maxsize(480, 480)
        self.minsize(480, 480)
        self.cv.pack(fill=tk.BOTH, expand=tk.YES)
        self.cv.create_rectangle(10, 10, 470, 470,
                                 outline='white', fill='grey')
        for i in range(20, 461, 88):
            self.cv.create_line(20, i, 460, i, width=3, fill='black')
            self.cv.create_line(i, 20, i, 460, width=3, fill='black')

        self.show_board()

        self.cv.bind("<Button-1>", self.on_left_click)  # 左键点击事件
        self.cv.bind("<Button-3>", self.on_right_click)  # 右键点击事件

        tk.Label(self, text="Author: MaoLongLong").pack(side=tk.BOTTOM)

    def print_chess(self, i, j, color, key, line='grey'):
        x1, y1 = j * 88 + 30, i * 88 + 30
        x2, y2 = x1 + 68, y1 + 68
        if color == 'empty':
            self.cv.create_oval(x1, y1, x2, y2, fill='grey', outline=line,
                                width=3)
        else:
            self.cv.create_oval(x1, y1, x2, y2, fill=color, outline=line,
                                width=3)
        Game.board[i][j] = key

    def show_board(self):
        for i in range(5):
            for j in range(5):
                if Game.board[i][j] != Game.empty:
                    color = 'red' if Game.board[i][j] > 0 else 'blue'
                    self.print_chess(i, j, color, Game.board[i][j])
                else:
                    self.print_chess(i, j, 'empty', 0)

    def on_left_click(self, event):
        i = (event.y - 20) // 88
        j = (event.x - 20) // 88
        if Game.board[i][j] != Game.empty:
            if Game._focus is not None:
                tp = Game._focus
                self.print_chess(tp[0], tp[1], tp[2], tp[3])
            if Game.board[i][j] > 0:
                Game._focus = (i, j, 'red', Game.board[i][j])
                self.print_chess(i, j, 'red', Game.board[i][j], 'black')
            else:
                Game._focus = (i, j, 'blue', Game.board[i][j])
                self.print_chess(i, j, 'blue', Game.board[i][j], 'black')

    @staticmethod
    def get_key():
        return np.random.randint(1, 7)

    @staticmethod
    def print_board():
        print(Game.board)

    def on_right_click(self, event):
        i = (event.y - 20) // 88
        j = (event.x - 20) // 88
        if Game._focus is not None:
            tp = Game._focus
            Game._focus = None
            self.print_chess(tp[0], tp[1], 'empty', 0)
            self.print_chess(i, j, tp[2], tp[3])
            self.print_board();
            key1 = input('对方色子: ')
            key2 = int(input('我方色子: '))
            state = State(Game.board, 1 if Game.first else -1, key2)
            node = MonteCarloTreeSearchNode(state)
            mcts = MonteCarloTreeSearch(node)
            Game.board = mcts.best_action()
            self.show_board()
            self.print_board()


if __name__ == '__main__':
    game = Game()
    game.mainloop()
