import numpy as np

from nim.Nim import Nim
from nim.ai.Agent import Q_Learning, Random, q_mctsAgent, mctsAgent, GreedyMultiRow, SupervisedQAgent


def simulate_and_save():
    # Initialization
    q_agent_1 = Q_Learning(0.4, 0.3, 0.15)
    q_agent_2 = Q_Learning(0.5, 0.5, 0.15)
    random = Random()

    # training q agents
    q_vs_q_train = Nim(q_agent_1, q_agent_2, train=True)
    q_vs_q_train.play(5000)

    # play and export history
    q_agent_1.epsilon = 0
    q_agent_2.epsilon = 0
    q_vs_random = Nim(q_agent_1, random, train=False)
    q_vs_random.play(225_000, save_history=True)

    # q agent moves second
    random_vs_q = Nim(random, q_agent_2, train=False)
    random_vs_q.play(225_000, save_history=True)

    # logs
    print("### Q-Agent vs. Random ###\n")
    print("Q-Agent moves first")
    print(f"Train - Wins: {q_vs_random.wins_1} Losses: {q_vs_random.wins_2}")
    print("----------")
    print("Q-Agent moves second")
    print(f"Train - Wins: {random_vs_q.wins_1} Losses: {random_vs_q.wins_2}")


def print_playout_statistics(agent1, agent2):
    sorted_playouts_1 = {k: v for k, v in sorted(agent1.playout_counts.items(), key=lambda item: item[1][0])}

    for k in sorted_playouts_1.keys():
        print(k[0],
              int(np.mean(sorted_playouts_1[k])),
              int(np.mean(agent2.playout_counts[k])),
              sep=" & ",
              end="\\\\\n")


# NIM_SIZE = 1
# NIM_STONES = 30
# MODEL_PATH = 'nim/data/model1row.pth'

def experiment_1():
    random = Random()
    q_mcts = q_mctsAgent()
    mcts = mctsAgent()

    q_mcts_vs_random = Nim(q_mcts, random, train=False)
    q_mcts_vs_random.play(100)

    print("\n### Q MCTS vs. Random ###\n")
    print(f"Wins: {q_mcts_vs_random.wins_1} Losses: {q_mcts_vs_random.wins_2}")

    mcts_vs_random = Nim(mcts, random, train=False)
    mcts_vs_random.play(100)

    print("\n### MCTS vs. Random ###\n")
    print(f"Wins: {mcts_vs_random.wins_1} Losses: {mcts_vs_random.wins_2}")

    print_playout_statistics(q_mcts, mcts)


def experiment_1_2():
    random = Random()
    q_mcts = q_mctsAgent(1e-2)
    mcts = mctsAgent(1e-2)

    q_mcts_vs_random = Nim(q_mcts, random, train=False)
    q_mcts_vs_random.play(100)

    print("\n### Q MCTS vs. Random ###\n")
    print(f"Wins: {q_mcts_vs_random.wins_1} Losses: {q_mcts_vs_random.wins_2}")

    mcts_vs_random = Nim(mcts, random, train=False)
    mcts_vs_random.play(100)

    print("\n### MCTS vs. Random ###\n")
    print(f"Wins: {mcts_vs_random.wins_1} Losses: {mcts_vs_random.wins_2}")

    print_playout_statistics(q_mcts, mcts)


def experiment_2():
    q_mcts = q_mctsAgent()
    mcts = mctsAgent()

    q_mcts_vs_mcts = Nim(q_mcts, mcts, train=False)
    q_mcts_vs_mcts.play(100)

    print("\n### Q MCTS vs. MCTS ###\n")
    print(f"Wins: {q_mcts_vs_mcts.wins_1} Losses: {q_mcts_vs_mcts.wins_2}")


def experiment_3():
    q_mcts = q_mctsAgent()
    mcts = mctsAgent()

    q_mcts_vs_mcts = Nim(q_mcts, mcts, train=False)
    q_mcts_vs_mcts.play(100)

    print("\n### Q MCTS vs. MCTS ###\n")
    print(f"Wins: {q_mcts_vs_mcts.wins_1} Losses: {q_mcts_vs_mcts.wins_2}")


def experiment_4():
    q_mcts = q_mctsAgent(1e-2)
    mcts = mctsAgent(5e-2)

    q_mcts_vs_mcts = Nim(q_mcts, mcts, train=False)
    q_mcts_vs_mcts.play(100)

    print("\n### Q MCTS vs. MCTS ###\n")
    print(f"Wins: {q_mcts_vs_mcts.wins_1} Losses: {q_mcts_vs_mcts.wins_2}")


def experiment_5():
    q_mcts = q_mctsAgent(1e-2)
    mcts = mctsAgent(1e-1)

    q_mcts_vs_mcts = Nim(q_mcts, mcts, train=False)
    q_mcts_vs_mcts.play(100)

    print("\n### Q MCTS vs. MCTS ###\n")
    print(f"Wins: {q_mcts_vs_mcts.wins_1} Losses: {q_mcts_vs_mcts.wins_2}")


# NIM_SIZE = 3
# NIM_STONES = 10
# MODEL_PATH = 'nim/data/model3row_standard.pth'
def experiment_6():
    q_mcts = q_mctsAgent(5e-2, one_row=False)
    mcts = mctsAgent(5e-2)

    q_mcts_vs_mcts = Nim(q_mcts, mcts, train=False)
    q_mcts_vs_mcts.play(100)

    print("\n### Q MCTS vs. MCTS ###\n")
    print(f"Wins: {q_mcts_vs_mcts.wins_1} Losses: {q_mcts_vs_mcts.wins_2}")


def experiment_7():
    mcts = mctsAgent(5e-2)
    q_mcts = q_mctsAgent(5e-2, one_row=False)

    mcts_vs_q_mcts = Nim(mcts, q_mcts, train=False)
    mcts_vs_q_mcts.play(100)

    print("\n### MCTS vs. Q MCTS ###\n")
    print(f"Wins: {mcts_vs_q_mcts.wins_1} Losses: {mcts_vs_q_mcts.wins_2}")


def experiment_8():
    greedy = GreedyMultiRow()
    q_mcts = q_mctsAgent(5e-2, one_row=False)

    q_mcts_vs_greedy = Nim(q_mcts, greedy, train=False)
    q_mcts_vs_greedy.play(100)

    print("\n### Q MCTS vs. Greedy ###\n")
    print(f"Wins: {q_mcts_vs_greedy.wins_1} Losses: {q_mcts_vs_greedy.wins_2}")




if __name__ == '__main__':
    experiment_1_2()
