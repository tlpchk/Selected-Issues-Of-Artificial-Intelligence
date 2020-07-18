import itertools
from abc import ABCMeta, abstractmethod

import torch

from nim.ai.Net import Net, Net1row
from nim.mcts.mcts import MCTS
from nim.model.State_Action import *


class Agent:
    __metaclass__ = ABCMeta

    @abstractmethod
    def policy(self, state): pass


class GreedyMultiRow(Agent):
    def policy(self, state):
        nonzero_rows = np.nonzero(state.state)[0]
        if len(nonzero_rows) == 2:
            return Action(np.argmax(state.state), 1)
        row = nonzero_rows[0]
        return Action(row, state.state[row])


class Random(Agent):
    def __init__(self):
        self.history = []

    def policy(self, state):
        move = np.random.choice(state.get_actions())
        self.history.append((state, move))
        return move


class Human(Agent):
    def policy(self, state):
        while True:
            print(state)
            user_input = input("Please enter your move: ")
            try:
                user_tokens = list(map(int, user_input.split(" ")))
                row, action = user_tokens
                row -= 1
                if not state.action_is_valid(Action(row, action)):
                    raise ValueError
                else:
                    return Action(row, action)

            except ValueError:
                print("Not a valid move. Try again..")


class QKey:
    def __init__(self, state, action):
        self.state = state
        self.action = action

    def __hash__(self):
        return hash((tuple(self.state.state), self.action.row, self.action.action))

    def __eq__(self, other):
        return (
                       self.state.state == other.state.state).all() and self.action.row == other.action.row and self.action.action == other.action.action

    def __str__(self):
        return f'{self.state.state, self.action.row, self.action.action}'

    def __repr__(self):
        return f'{self.state.state, self.action.row, self.action.action}'


class Q_Learning(Agent):
    def __init__(self, alpha, gamma, epsilon):
        self.Q = {}
        self.history = []
        self.WIN_REWARD, self.LOSS_REWARD = 1.0, -1.0
        self.alpha, self.gamma, self.epsilon = alpha, gamma, epsilon
        self.init_Q()

    def init_Q(self):
        states_list = itertools.product(*itertools.repeat([i for i in range(NIM_STONES + 1)], NIM_SIZE))
        for state_list in states_list:
            state = State(np.array(state_list))
            for action in state.get_actions():
                self.Q[QKey(state, action)] = 0

    def policy(self, curr_state):
        poss_actions = curr_state.get_actions()
        if np.random.random() > self.epsilon:
            q_val = [self.Q[QKey(curr_state, a)] for a in poss_actions]
            move = poss_actions[np.argmax(q_val)]
            self.history.append((curr_state, move))
            return move
        else:
            move = np.random.choice(poss_actions)
            self.history.append((curr_state, move))
            return move

    def move_with_policy(self, curr_state):
        poss_actions = curr_state.get_actions()
        q_val = [self.Q[QKey(curr_state, a)] for a in poss_actions]
        return poss_actions[np.argmax(q_val)]

    def update(self, win):
        reward = self.WIN_REWARD if win else self.LOSS_REWARD
        last_state, last_action = self.history[-1]
        self.Q[QKey(last_state, last_action)] = reward
        for i in reversed(range(len(self.history) - 1)):
            state, action = self.history[i]
            self.Q[QKey(state, action)] = (1 - self.alpha) * self.Q[QKey(state, action)]
            if i == len(self.history) - 2:
                next_state, next_action = last_state, last_action
            else:
                next_state, next_action = self.history[i + 1]
            self.Q[QKey(state, action)] += self.alpha * (reward +
                                                         np.max([self.Q[QKey(next_state, a_p)] for a_p in
                                                                 next_state.get_actions()]))


class SupervisedQAgent(Agent):
    def __init__(self):
        self._model = Net()
        self._model.load_state_dict(torch.load(MODEL_PATH))
        self._model.eval()
        self.history = []

    def policy(self, state):
        poss_actions = state.get_actions()
        inputs = [[*state.state, action.row, action.action] for action in state.get_actions()]
        inputs = torch.FloatTensor(inputs)
        q_values = self._model(inputs)
        return poss_actions[np.argmax(q_values)]


class q_mctsAgent(Agent):
    def __init__(self,t=5e-2,one_row=True):
        self._mcts = None
        self.history = []
        self.playout_counts = {}
        if one_row:
            self._model = Net1row()
        else:
            self._model = Net()
        self._model.load_state_dict(torch.load(MODEL_PATH))
        self._model.eval()
        self.time = t

    def policy(self, curr_state):
        self._mcts = MCTS(curr_state, model=self._model)
        child = self._mcts.best_action(self.time)
        self.update_playout_counts(curr_state.state)
        diff = np.subtract(curr_state.state, child.state.state)
        action_idx = diff.nonzero()[0]
        return Action(action_idx, diff[action_idx])

    def update_playout_counts(self, state):
        state = tuple(state)
        if not self.playout_counts.get(state):
            self.playout_counts[state] = []
        self.playout_counts[state].append(self._mcts.playout_count)


class mctsAgent(Agent):
    def __init__(self, t=5e-2):
        super().__init__()
        self.playout_counts = {}
        self.time = t

    def policy(self, curr_state):
        self._mcts = MCTS(curr_state)
        child = self._mcts.best_action(self.time)
        self.update_playout_counts(curr_state.state)
        diff = np.subtract(curr_state.state, child.state.state)
        action_idx = diff.nonzero()[0]
        return Action(action_idx, diff[action_idx])

    def update_playout_counts(self, state):
        state = tuple(state)
        if not self.playout_counts.get(state):
            self.playout_counts[state] = []
        self.playout_counts[state].append(self._mcts.playout_count)