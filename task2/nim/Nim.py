import numpy as np
import pandas as pd
from sklearn.utils import shuffle

from nim.ai.Agent import Q_Learning, State

history_path = 'nim/data/history_test.csv'


class Nim:
    wins_1 = wins_2 = 0

    def __init__(self, player1, player2, train=True):
        self.players = [player1, player2]
        self.train = train

    def update(self, player, save_history):
        if player == self.players[0]:
            self.wins_1 += 1
            if type(self.players[0]) is Q_Learning: self.players[0].update(True)
            if type(self.players[1]) is Q_Learning: self.players[1].update(False)
            rewards = [1, -1]
        else:
            self.wins_2 += 1
            if type(self.players[0]) is Q_Learning: self.players[0].update(False)
            if type(self.players[1]) is Q_Learning: self.players[1].update(True)
            rewards = [-1, 1]
        if save_history:
            history_update = pd.DataFrame()
            for i, player in enumerate(self.players):
                for move in player.history:
                    history_item = np.append(move[0].state, [move[1].row, move[1].action, rewards[i]])
                    history_item = pd.DataFrame([history_item])
                    history_update = history_update.append(history_item)
            history_update = shuffle(history_update)
            history_update.to_csv(history_path, mode='a+', header=False, index=None)

        for player in self.players:
            if hasattr(player, 'player'):
                player.history.clear()

    def play(self, no_games, init_state=None, save_history=False):
        log_intervals = np.linspace(0, no_games, num=20, dtype=int)
        for i in range(no_games):
            if i in log_intervals:
                print('.', end='')

            state = State(init_state)
            while not state.is_terminal():
                for player in self.players:
                    action_p = player.policy(state)
                    state = state.peek_action(action_p)

                    if state.is_terminal():
                        self.update(player, save_history)
                        break
