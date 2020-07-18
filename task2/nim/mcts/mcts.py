import time
from nim.mcts.qnode import QNode, Node


class MCTS:
    def __init__(self, state=None, node=None, model=None):
        self.playout_count = 0
        if state:
            if model:
                self.root = QNode(state)
            else:
                self.root = Node(state)
        elif node:
            self.root = node
        else:
            raise ValueError
        self._model = model

    def best_action(self, timeout):
        start = time.time()
        while time.time() - start < timeout:
            node = self._search_and_expand()
            if self._model:
                reward = node.playout(self._model)
                node.backpropagate(reward, node.parent.state.player_turn)
            else:
                reward = node.playout()
                node.backpropagate(reward)
            self.playout_count += 1

        return self.root.best_child(c_param=0.)

    def _search_and_expand(self):
        node = self.root
        while not node.is_terminal():
            if not node.is_fully_expanded():
                return node.expand()
            else:
                node = node.best_child()
        return node
