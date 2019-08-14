# -*- coding: utf-8 -*-
# author: MaoLongLong
# date: 2019/8/13
import numpy as np


class Move:
    def __init__(self, from_x, from_y, to_x, to_y):
        self.from_x = from_x
        self.from_y = from_y
        self.to_x = to_x
        self.to_y = to_y

    def __repr__(self):
        return 'from:[{}, {}]'.format(self.from_x, self.from_y) + \
               ' to:[{}, {}]'.format(self.to_x, self.to_y)


class State:
    red = 1
    blue = -1

    def __init__(self, board, next_to_move=1, key=None):
        self.board = board
        self.next_to_move = next_to_move
        self.num_of_red = np.sum(self.board > 0)
        self.num_of_blue = np.sum(self.board < 0)
        if key is not None:
            self.key = key

    @property
    def game_result(self):
        if self.board[4][4] > 0 or self.num_of_blue == 0:
            return 1
        elif self.board[0][0] < 0 or self.num_of_red == 0:
            return -1
        else:
            return None

    def is_game_over(self):
        return self.game_result is not None

    def move(self, move: Move):
        new_board = np.copy(self.board)
        new_board[move.to_x][move.to_y] = new_board[move.from_x][move.from_y]
        new_board[move.from_x][move.from_y] = 0
        next_to_move = State.red if self.next_to_move == State.blue \
            else State.blue
        return State(new_board, next_to_move)

    def get_legal_actions(self):
        # TODO 完善功能
        actions = []
        if hasattr(self, 'key'):
            key = self.key
            temp = np.where(self.board == key * self.next_to_move)
            if len(temp[0]) != 0:
                x, y = temp[0][0], temp[1][0]
                if self.next_to_move == State.red:
                    if x + 1 < 5:
                        actions.append(Move(x, y, x + 1, y))
                    if y + 1 < 5:
                        actions.append(Move(x, y, x, y + 1))
                    if x + 1 < 5 and y + 1 < 5:
                        actions.append(Move(x, y, x + 1, y + 1))
                else:
                    if x - 1 > -1:
                        actions.append(Move(x, y, x - 1, y))
                    if y - 1 > -1:
                        actions.append(Move(x, y, x, y - 1))
                    if x - 1 > -1 and y - 1 > -1:
                        actions.append(Move(x, y, x - 1, y - 1))
            else:
                low = key - 1
                while True:
                    if low == 0:
                        break
                    temp = np.where(self.board == low * self.next_to_move)
                    if len(temp[0]) != 0:
                        x, y = temp[0][0], temp[1][0]
                        if self.next_to_move == State.red:
                            if x + 1 < 5:
                                actions.append(Move(x, y, x + 1, y))
                            if y + 1 < 5:
                                actions.append(Move(x, y, x, y + 1))
                            if x + 1 < 5 and y + 1 < 5:
                                actions.append(Move(x, y, x + 1, y + 1))
                        else:
                            if x - 1 > -1:
                                actions.append(Move(x, y, x - 1, y))
                            if y - 1 > -1:
                                actions.append(Move(x, y, x, y - 1))
                            if x - 1 > -1 and y - 1 > -1:
                                actions.append(Move(x, y, x - 1, y - 1))
                        break
                    low -= 1

                high = key + 1
                while True:
                    if high == 7:
                        break
                    temp = np.where(self.board == high * self.next_to_move)
                    if len(temp[0]) != 0:
                        x, y = temp[0][0], temp[1][0]
                        if self.next_to_move == State.red:
                            if x + 1 < 5:
                                actions.append(Move(x, y, x + 1, y))
                            if y + 1 < 5:
                                actions.append(Move(x, y, x, y + 1))
                            if x + 1 < 5 and y + 1 < 5:
                                actions.append(Move(x, y, x + 1, y + 1))
                        else:
                            if x - 1 > -1:
                                actions.append(Move(x, y, x - 1, y))
                            if y - 1 > -1:
                                actions.append(Move(x, y, x, y - 1))
                            if x - 1 > -1 and y - 1 > -1:
                                actions.append(Move(x, y, x - 1, y - 1))
                        break
                    high += 1
            return actions

        if self.next_to_move == State.red:
            for i in range(1, 7):
                num = i
                temp = np.where(self.board == num)
                if len(temp[0]) != 0:
                    x, y = temp[0][0], temp[1][0]
                    if x + 1 < 5:
                        actions.append(Move(x, y, x + 1, y))
                    if y + 1 < 5:
                        actions.append(Move(x, y, x, y + 1))
                    if x + 1 < 5 and y + 1 < 5:
                        actions.append(Move(x, y, x + 1, y + 1))
        else:
            for i in range(-6, 0):
                num = i
                temp = np.where(self.board == num)
                if len(temp[0]) != 0:
                    x, y = temp[0][0], temp[1][0]
                    if x - 1 > -1:
                        actions.append(Move(x, y, x - 1, y))
                    if y - 1 > -1:
                        actions.append(Move(x, y, x, y - 1))
                    if x - 1 > -1 and y - 1 > -1:
                        actions.append(Move(x, y, x - 1, y - 1))
        return actions
