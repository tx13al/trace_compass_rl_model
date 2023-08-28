from Agent import Agent
from State import State
import numpy as np  # Make sure to import numpy
from tqdm import tqdm
import time
from collections import defaultdict
from collections import Counter


class RLModel:
    def __init__(self, syscalls, threshold):
        self.agent = None
        self.syscalls = syscalls
        self.threshold = threshold

        self.favorable_actions_for_short_syscalls = defaultdict(list)
        self.favorable_actions_for_long_syscalls = defaultdict(list)
        self.short_syscall_durations = defaultdict(list)
        self.long_syscall_durations = defaultdict(list)

    def get_reward(self, state):
        # Since state is an object, we use its attributes
        syscall_duration_type = state.duration_type

        reward = 0

        if syscall_duration_type == "long":
            # Placeholder logic for long syscalls
            reward += 3  # This could be more complex based on your actual logic
        elif syscall_duration_type == "short":
            # Placeholder logic for short syscalls
            reward -= 5  # This could be more complex based on your actual logic

        return reward

    def run(self):
        # Loop through the syscalls
        # Stop at second last to avoid IndexError for next_state
        for i in tqdm(range(len(self.syscalls) - 1)):

            # Current syscall
            syscall = self.syscalls[i]

            # Define state based on current syscall type and duration
            state_type = "long" if syscall.duration > self.threshold else "short"
            state = State(syscall.event_type, state_type)

            # Let the agent choose an action
            self.agent = Agent(syscall.events)
            action = self.agent.choose_action(state)
            if state.duration_type == "short":
                self.favorable_actions_for_short_syscalls[syscall.event_type].append(action)
                self.short_syscall_durations[syscall.event_type].append(syscall.duration)
            elif state.duration_type == "long":
                self.favorable_actions_for_long_syscalls[syscall.event_type].append(action)
                self.long_syscall_durations[syscall.event_type].append(syscall.duration)
            # Observe reward
            reward = self.get_reward(state)

            # Define next_state based on next syscall type and duration
            next_syscall = self.syscalls[i + 1]
            next_state_type = "long" if next_syscall.duration > self.threshold else "short"
            next_state = State(next_syscall.event_type, next_state_type)

            # Update Q-values based on observed reward and next_state
            self.agent.learn(state, action, reward, next_state)

    def save_top_actions(self, filename):
        with open(filename, 'w') as f:
            f.write("All favorable actions for each event type:\n")

            all_event_types = set(self.favorable_actions_for_short_syscalls.keys()) | set(
                self.favorable_actions_for_long_syscalls.keys())

            for event_type in all_event_types:
                f.write(f"Event Type: {event_type}\n")

                if event_type in self.favorable_actions_for_short_syscalls:
                    f.write("  For short syscalls:\n")
                    short_actions = self.favorable_actions_for_short_syscalls[event_type]
                    action_counts = Counter(short_actions)
                    sorted_actions = action_counts.most_common()  # Sort by count
                    avg_short_duration = sum(self.short_syscall_durations[event_type]) / len(
                        self.short_syscall_durations[event_type]) if self.short_syscall_durations[event_type] else 0
                    f.write(f"  Average duration: {round(avg_short_duration)}\n")

                    for action, count in sorted_actions:
                        f.write(f"    Action: {action}, Count: {count}\n")
                else:
                    f.write("  No short syscalls for this event type.\n")

                if event_type in self.favorable_actions_for_long_syscalls:
                    f.write(f"Event Type: {event_type}\n")
                    f.write("  For long syscalls:\n")
                    long_actions = self.favorable_actions_for_long_syscalls[event_type]
                    action_counts = Counter(long_actions)
                    sorted_actions = action_counts.most_common()  # Sort by count
                    avg_long_duration = sum(self.long_syscall_durations[event_type]) / len(
                        self.long_syscall_durations[event_type]) if self.long_syscall_durations[event_type] else 0
                    f.write(f"  Average duration: {round(avg_long_duration)}\n")

                    for action, count in sorted_actions:
                        f.write(f"    Action: {action}, Count: {count}\n")
                else:
                    f.write("  No long syscalls for this event type.\n")
