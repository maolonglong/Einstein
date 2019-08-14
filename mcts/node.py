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
        self.children = []

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
        action = self.untried_actions.pop()
        next_state = self.state.move(action)
        child_node = MonteCarloTreeSearchNode(next_state, self)
        self.children.append(child_node)
        return child_node

    def is_terminal_node(self):
        return self.state.is_game_over()

    def rollout_policy(self, possible_moves):
        return possible_moves[np.random.randint(len(possible_moves))]

    def rollout(self):
        current_rollout_state = self.state
        while not current_rollout_state.is_game_over():
            possible_moves = current_rollout_state.get_legal_actions()
            action = self.rollout_policy(possible_moves)
            current_rollout_state = current_rollout_state.move(action)
        return current_rollout_state.game_result

    def backpropagate(self, result):
        self._number_of_visits += 1
        self._results[result] += 1
        if self.parent:
            self.parent.backpropagate(result)

    def is_fully_expanded(self):
        return len(self.untried_actions) == 0

    def best_child(self, c_param=14.44):
        if c_param == 0:
            for c in self.children:
                print(c.n, end=' ')
        choices_weights = [
            (c.q / c.n) + c_param * np.sqrt(2 * np.log(self.n) / c.n)
            for c in self.children
        ]
        if c_param == 0:
            cc = self.children[np.argmax(choices_weights)]
            print(cc._results[-1] / cc.n * 100, '%')
        return self.children[np.argmax(choices_weights)]
