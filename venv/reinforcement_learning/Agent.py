import random
from QTable import QTable
import json

class Agent:
    def __init__(self, possible_actions):
        self.q_table = QTable(possible_actions)

    def choose_action(self, state):
        return self.q_table.get_best_action(state)

    def learn(self, state, action, reward, next_state):
        self.q_table.update(state, action, reward, next_state)


