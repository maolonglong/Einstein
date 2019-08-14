# -*- coding: utf-8 -*-
# author: MaoLongLong
# date: 2019/8/13
from mcts.node import MonteCarloTreeSearchNode
from mcts.search import MonteCarloTreeSearch
from mcts.einstein import State
import numpy as np

init_board = np.array([[0, 0, 0, 0, 0], [0, 1, 2, 0, 0], [0, 3, 0, 0, 0],
                       [0, 0, 0, 0, 0], [0, 0, 0, 0, -2]])
init_state = State(init_board, 1, 1)
node = MonteCarloTreeSearchNode(init_state)
mcts = MonteCarloTreeSearch(node)
print(mcts.best_action().state.board)
