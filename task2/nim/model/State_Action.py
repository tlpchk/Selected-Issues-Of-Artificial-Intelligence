from copy import deepcopy

import numpy as np

NIM_SIZE = 1
NIM_STONES = 30
MODEL_PATH = 'nim/data/model1row.pth'


# (s,a), where s is number of row, and a is number of peels
class Action:
    def __init__(self, row, action):
        self.row = row
        self.action = action

    def __repr__(self):
        return f'{self.row} {self.action}'


# (s1,s2,s3) - state of Nim with 3 rows
class State:
    def __init__(self, state=None, random=False, player_turn=None):
        if state is not None:
            if type(state) is (not list or not tuple):
                raise TypeError("Argument not a list or tuple")
            self.state = state
        else:
            if random:
                self.state = np.random.randint(1, NIM_STONES, NIM_SIZE)
            else:
                self.state = np.ones(NIM_SIZE, dtype=np.int) * NIM_STONES
        if player_turn:
            self.player_turn = player_turn
        else:
            self.player_turn = 1

    def __repr__(self):
        return f'{[stones for stones in self.state]}'

    def is_terminal(self):
        return np.sum(self.state) == 0

    def action_is_valid(self, action):
        return self.state[action.row] > 0 and action.action <= self.state[action.row]

    def get_actions(self):
        if self.is_terminal():
            return []
        else:
            if NIM_SIZE > 1:
                return [Action(row, a) for row in range(NIM_SIZE) for a in range(1, self.state[row] + 1)]
            else:
                return [Action(row, a) for row in range(NIM_SIZE) for a in range(1, 4) if self.state[row] >= a]

    def do_action(self, a):
        if a is not None:
            self.state[a.row] -= a.action

    def peek_action(self, a):
        new_state = State(deepcopy(self.state), player_turn=self.player_turn)
        new_state.do_action(a)
        new_state.player_turn *= -1
        return new_state
