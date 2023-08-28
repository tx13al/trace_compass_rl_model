from collections import defaultdict
import random


class QTable:
    def __init__(self, possible_actions):
        self.q_values = defaultdict(lambda: defaultdict(lambda: random.uniform(-1, 1)))
        self.possible_actions = possible_actions  # Initialize with a list of all possible actions

    def update(self, state, action, reward, next_state, alpha=0.1, gamma=0.9):
        current_q = self.q_values[state][action]
        max_future_q = max(self.q_values[next_state].values(), default=0)
        new_q = (1 - alpha) * current_q + alpha * (reward + gamma * max_future_q)
        self.q_values[state][action] = new_q

    def get_best_action(self, state, epsilon=0.5):
        if state not in self.q_values or not self.q_values[state]:
            for action in self.possible_actions:
                self.q_values[state][action] = 0.0

        actions = list(self.q_values[state].keys())

        if actions:  # Check if actions list is not empty
            if random.random() < epsilon:
                chosen_action = random.choice(actions)
            else:
                chosen_action = max(self.q_values[state], key=self.q_values[state].get)
            return chosen_action
        else:
            # Handle the situation where the state-action list is empty.
            # Return a random action from the list of all possible actions.
            return random.choice(self.possible_actions) if self.possible_actions else None
