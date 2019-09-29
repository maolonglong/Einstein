# -*- coding: utf-8 -*-
# author: MaoLongLong
# date: 2019/8/13
from collections import defaultdict
import numpy as np
from mcts.einstein import State


class MonteCarloTreeSearchNode:
    def __init__(self, state: State, parent=None):
        self._number_of_visits = 0
        self._results = defaultdict(int)
        self.state = state
        self.parent = parent
        self.children = [[], [], [], [], [], [], []]

    @property
    def untried_actions(self):
        if not hasattr(self, '_untried_actions'):
            self._untried_actions = self.state.get_legal_actions()
        return self._untried_actions

    @property
    def q(self):
        wins = self._results[self.parent.state.next_to_move]
        loses = self._results[-1 * self.parent.state.next_to_move]
        return wins - loses

    @property
    def n(self):
        return self._number_of_visits

    def expand(self):
        _children = []
        action = self.untried_actions.pop()
        state = self.state.move(action)
        for key in range(1, 7):
            next_state = State(state.board, state.next_to_move, key)
            child = MonteCarloTreeSearchNode(next_state, self)
            _children.append(child)
            self.children[key].append(child)
        return _children

    def is_terminal_node(self):
        return self.state.is_game_over()

    def rollout_policy(self, possible_moves):
        return possible_moves[np.random.randint(len(possible_moves))]

    def rollout(self):
        current_rollout_state = self.state
        key = current_rollout_state.key
        while not current_rollout_state.is_game_over():
            possible_moves = current_rollout_state.get_legal_actions(key)
            action = self.rollout_policy(possible_moves)
            current_rollout_state = current_rollout_state.move(action)
            key = np.random.randint(1, 7)
        return current_rollout_state.game_result

    def backpropagate(self, result):
        self._number_of_visits += 1
        self._results[result] += 1
        if self.parent:
            self.parent.backpropagate(result)

    def is_fully_expanded(self):
        return len(self.untried_actions) == 0

    def best_child(self, c_param=1.44):
        if c_param == 0:
            # cc = self.children[key][np.argmax(choices_weights)]
            # print(cc._results[self.state.next_to_move] / cc.n * 100, '%')
            print(self._results[self.state.next_to_move] / self.n * 100, '%')
            dk = []
            max_cnt = 0
            ret = None
            for i in range(1, 7):
                choices_weights = [
                    (c.q / c.n) + c_param * np.sqrt(2 * np.log(self.n) / c.n)
                    for c in self.children[i]
                ]
                best_chi = self.children[i][np.argmax(choices_weights)].state.board
                tmp_cnt = 1
                for i in dk:
                    if (best_chi == i).all():
                        tmp_cnt += 1
                dk.append(best_chi)
                if tmp_cnt > max_cnt:
                    max_cnt = tmp_cnt
                    ret = dk[-1]
            print(dk)
            print('cnt:', max_cnt)
            return ret

        key = np.random.randint(1, 7)
        choices_weights = [
            (c.q / c.n) + c_param * np.sqrt(2 * np.log(self.n) / c.n)
            for c in self.children[key]
        ]

        return self.children[key][np.argmax(choices_weights)]

# if __name__ == '__main__':
#     a = np.array([
#         [1, 2, 3, 0, 0],
#         [4, 5, 0, 0, 0],
#         [6, 0, 0, 0, -1],
#         [0, 0, 0, -2, -3],
#         [0, 0, -4, -5, -6]
#     ])
#     s = State(a, 1, 5)
#     node = MonteCarloTreeSearchNode(s)
#     for i in node.expand():
#         print(i.state.board)
