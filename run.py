# -*- coding: utf-8 -*-
# author: MaoLongLong
# date: 2019/9/12
import os
import time
import tkinter as tk
from multiprocessing import Pool

import numpy as np

from mcts.einstein import State
from mcts.node import MonteCarloTreeSearchNode
from mcts.search import MonteCarloTreeSearch


class Game(tk.Tk):  # TODO 增加先手
    first = None
    board = None
    empty = 0
    _focus = None
    i_dir = [5, 4, 3, 2, 1]
    j_dir = ['A', 'B', 'C', 'D', 'E']
    index = 1
    txt_strs = []

    def __init__(self):
        super(Game, self).__init__()
        self.cv = tk.Canvas(self)
        self.setup_board()
        self.setup_ui()

    @classmethod
    def chess_dir(cls, i, j):
        return '{}{}'.format(cls.j_dir[j], cls.i_dir[i])

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
            Game.txt_strs.append(
                'R:A5-{};B5-{};C5-{};A4-{};B4-{};A3-{}'.format(
                    Game.board[0][0], Game.board[0][1], Game.board[0][2],
                    Game.board[1][0], Game.board[1][1], Game.board[2][0]))
            Game.txt_strs.append('B:E3{};D2{};E2{};C1{};D1{};E1{}'.format(
                Game.board[2][4], Game.board[3][3], Game.board[3][4],
                Game.board[4][2], Game.board[4][3], Game.board[4][4]))
            key = int(input('我方色子: '))
            state1 = State(Game.board.copy(), 1 if Game.first else -1, key)
            state2 = State(Game.board.copy(), 1 if Game.first else -1, key)
            state3 = State(Game.board.copy(), 1 if Game.first else -1, key)
            state4 = State(Game.board.copy(), 1 if Game.first else -1, key)
            node1 = MonteCarloTreeSearchNode(state1)
            node2 = MonteCarloTreeSearchNode(state2)
            node3 = MonteCarloTreeSearchNode(state3)
            node4 = MonteCarloTreeSearchNode(state4)
            mcts1 = MonteCarloTreeSearch(node1)
            mcts2 = MonteCarloTreeSearch(node2)
            mcts3 = MonteCarloTreeSearch(node3)
            mcts4 = MonteCarloTreeSearch(node4)

            pool = Pool(4)
            ress = pool.map(MonteCarloTreeSearch.best_action,
                            [mcts1, mcts2, mcts3, mcts4])
            pool.close()
            pool.join()

            max_cnt, best_res = 0, None
            for res in ress:
                cnt = 0
                for i in ress:
                    if (res == i).all():
                        cnt += 1
                if cnt > max_cnt:
                    max_cnt = cnt
                    best_res = res
            tmp = np.where((Game.board == best_res) == False)
            C = 'R{}'.format(best_res[tmp[0][1]][tmp[1][1]])
            Game.txt_strs.append(
                '{}:{};({},{})'.format(Game.index, key, C,
                                       self.chess_dir(tmp[0][1],
                                                      tmp[1][1])))
            Game.index += 1
            Game.board = best_res
            self.show_board()
            os.system('clear')
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
            Game.txt_strs.append(
                'R:A5-{};B5-{};C5-{};A4-{};B4-{};A3-{}'.format(
                    Game.board[0][0], Game.board[0][1], Game.board[0][2],
                    Game.board[1][0], Game.board[1][1], Game.board[2][0]))
            Game.txt_strs.append(
                'B:E3{};D2{};E2{};C1{};D1{};E1{}'.format(
                    Game.board[2][4], Game.board[3][3], Game.board[3][4],
                    Game.board[4][2], Game.board[4][3], Game.board[4][4]))

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
            self.cv.create_text((x1 + x2) / 2, (y1 + y2) / 2,
                                text=str(abs(key)),
                                font=('Fira Code Medium', 30), fill='white')
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

    @classmethod
    def game_over(cls):
        if cls.board[4][4] > 0 or np.sum(cls.board < 0) == 0:
            return 1
        elif cls.board[0][0] < 0 or np.sum(cls.board > 0) == 0:
            return -1
        else:
            return None

    def get_txt_file(self):
        a = input('先手队名: ')
        b = input('后手队名: ')
        c = input('先手胜利?[y/n]: ')
        c = '先手胜' if c == 'y' else '后手胜'
        # time.strftime("%Y.%m.%d %H:%M", time.localtime())
        with open('./WTN-{}vs{}-{}{}.txt'.format(a, b, c,
                                                 time.strftime("%Y%m%d%H%M",
                                                               time.localtime())),
                  'w') as fp:
            fp.write(
                '#[WTN][{} R][{} B][{}][{} 北京][2019CCGC];'.format(a, b, c,
                                                                  time.strftime(
                                                                      "%Y.%m.%d %H:%M",
                                                                      time.localtime())) + '\n')
            for i in Game.txt_strs:
                fp.write(i + '\n')

    def on_right_click(self, event):
        os.system('clear')
        i = (event.y - 20) // 88
        j = (event.x - 20) // 88
        if Game._focus is not None:
            tp = Game._focus
            Game._focus = None
            self.print_chess(tp[0], tp[1], 'empty', 0)
            self.print_chess(i, j, tp[2], tp[3])
            self.print_board();
            key1 = input('对方色子: ')
            C = 'B{}'.format(abs(tp[3])) if Game.first else 'R{}'.format(
                abs(tp[3]))
            Game.txt_strs.append('{}:{};({},{})'.format(Game.index, key1, C,
                                                        self.chess_dir(i, j)))
            Game.index += 1
            if self.game_over() is not None:
                if self.game_over() == 1:
                    print('先手方胜')
                else:
                    print('后手方胜')
                self.get_txt_file()
                return
            key2 = int(input('我方色子: '))
            state1 = State(Game.board.copy(), 1 if Game.first else -1, key2)
            state2 = State(Game.board.copy(), 1 if Game.first else -1, key2)
            state3 = State(Game.board.copy(), 1 if Game.first else -1, key2)
            state4 = State(Game.board.copy(), 1 if Game.first else -1, key2)
            node1 = MonteCarloTreeSearchNode(state1)
            node2 = MonteCarloTreeSearchNode(state2)
            node3 = MonteCarloTreeSearchNode(state3)
            node4 = MonteCarloTreeSearchNode(state4)
            mcts1 = MonteCarloTreeSearch(node1)
            mcts2 = MonteCarloTreeSearch(node2)
            mcts3 = MonteCarloTreeSearch(node3)
            mcts4 = MonteCarloTreeSearch(node4)

            pool = Pool(4)
            ress = pool.map(MonteCarloTreeSearch.best_action,
                            [mcts1, mcts2, mcts3, mcts4])
            pool.close()
            pool.join()

            max_cnt, best_res = 0, None
            for res in ress:
                cnt = 0
                for i in ress:
                    if (res == i).all():
                        cnt += 1
                if cnt > max_cnt:
                    max_cnt = cnt
                    best_res = res
            tmp = np.where((Game.board == best_res) == False)
            if Game.first:
                C = 'R{}'.format(best_res[tmp[0][1]][tmp[1][1]])
                Game.txt_strs.append(
                    '{}:{};({},{})'.format(Game.index, key2, C,
                                           self.chess_dir(tmp[0][1],
                                                          tmp[1][1])))
            else:
                C = 'B{}'.format(-best_res[tmp[0][0]][tmp[1][0]])
                Game.txt_strs.append(
                    '{}:{};({},{})'.format(Game.index, key2, C,
                                           self.chess_dir(tmp[0][0],
                                                          tmp[1][0])))
            Game.index += 1
            Game.board = best_res
            self.show_board()
            self.print_board()
            if self.game_over() is not None:
                if self.game_over() == 1:
                    print('先手方胜')
                else:
                    print('后手方胜')
                self.get_txt_file()
                return


if __name__ == '__main__':
    game = Game()
    game.mainloop()
