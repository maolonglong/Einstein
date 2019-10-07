# -*- coding: utf-8 -*-
# author: MaoLongLong
# date: 2019/8/13
from mcts.node import MonteCarloTreeSearchNode
import time


class MonteCarloTreeSearch:
    def __init__(self, node: MonteCarloTreeSearchNode):
        self.root = node

    def best_action(self):
        start_time = time.time()
        a = 0
        while time.time() - start_time < 8:
        # for i in range(10000):
            v = self.tree_policy()
            if type(v) is list:
                for i in v:
                    reward = i.rollout()
                    i.backpropagate(reward)
                    a += 1
            else:
                reward = v.rollout()
                v.backpropagate(reward)
                a += 1
        print(a)
        return self.root.best_child(0)

    def tree_policy(self):
        current_node = self.root
        while not current_node.is_terminal_node():
            if not current_node.is_fully_expanded():
                return current_node.expand()
            else:
                current_node = current_node.best_child()
        return current_node
