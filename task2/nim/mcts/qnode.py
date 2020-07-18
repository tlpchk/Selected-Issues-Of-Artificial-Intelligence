from collections import defaultdict

import numpy as np
import torch


class QNode:
    def __init__(self, state, parent=None):
        self.state = state
        self.parent = parent
        self.children = []
        self._no_visits = 0
        self._result = 0
        self._untried_actions = None

    @property
    def untried_actions(self):
        if self._untried_actions is None:
            self._untried_actions = self.state.get_actions()
        return self._untried_actions

    @property
    def q(self):
        # loses = self._results[-1 * self.parent.state.player_turn]
        return self._result

    @property
    def n(self):
        return self._no_visits

    def is_fully_expanded(self):
        return len(self.untried_actions) == 0

    def is_terminal(self):
        return self.state.is_terminal()

    def best_child(self, c_param=1.2):
        choices_weights = [
            (child.q / child.n) + c_param * np.sqrt((2 * np.log(self.n) / child.n))
            for child in self.children
        ]
        return self.children[np.argmax(choices_weights)]

    def expand(self):
        untried_action = self.untried_actions.pop()
        child_state = self.state.peek_action(untried_action)
        child_node = QNode(child_state, parent=self)
        self.children.append(child_node)
        return child_node

    def playout(self, net):
        state = self.state
        if state.is_terminal():
            return -1.0

        inputs = [[*state.state, action.row, action.action] for action in state.get_actions()]
        inputs = torch.FloatTensor(inputs)
        q_values = net(inputs)

        return torch.max(q_values).item()

    def backpropagate(self, reward, player):
        self._no_visits += 1.
        if self.state.player_turn == player:
            self._result += reward
        else:
            self._result -= reward
        if self.parent:
            self.parent.backpropagate(reward, player)


class Node:
    def __init__(self, state, parent=None):
        self.state = state
        self.parent = parent
        self.children = []
        self._no_visits = 0
        self._results = defaultdict(int)
        self._untried_actions = None

    @property
    def untried_actions(self):
        if self._untried_actions is None:
            self._untried_actions = self.state.get_actions()
        return self._untried_actions

    @property
    def q(self):
        wins = self._results[self.parent.state.player_turn]
        loses = self._results[-1 * self.parent.state.player_turn]
        return wins - loses

    @property
    def n(self):
        return self._no_visits

    def is_fully_expanded(self):
        return len(self.untried_actions) == 0

    def is_terminal(self):
        return self.state.is_terminal()

    def best_child(self, c_param=1.6):
        choices_weights = [
            (child.q / child.n) + c_param * np.sqrt((2 * np.log(self.n) / child.n))
            for child in self.children
        ]
        return self.children[np.argmax(choices_weights)]

    def playout_policy(self, possible_moves):
        return possible_moves[np.random.randint(len(possible_moves))]

    def expand(self):
        untried_action = self.untried_actions.pop()
        child_state = self.state.peek_action(untried_action)
        child_node = Node(child_state, parent=self)
        self.children.append(child_node)
        return child_node

    def playout(self):
        state = self.state
        while not state.is_terminal():
            possible_moves = state.get_actions()
            action = self.playout_policy(possible_moves)
            state = state.peek_action(action)
        return -state.player_turn

    def backpropagate(self, player):
        self._no_visits += 1.
        self._results[player] += 1.
        if self.parent:
            self.parent.backpropagate(player)
