class QLearning:
    def __init__(self, sequences, states, actions):
        self.sequences = sequences
        self.states = states
        self.actions = actions
        self.Q = np.zeros((len(states), len(actions)))

        # Iterate through the sequences and print each one
        for index, sequence in enumerate(sequences):
            print(f"Sequence {index + 1}:")
            for event in sequence:
                print(f"  - {event}")
            print("=" * 50)

            # Defining states as unique events
            states = list(set(event for sequence in sequences for event in sequence))

            # Defining transitions between events as actions
            actions = []
            for sequence in sequences:
                for i in range(len(sequence) - 1):
                    actions.append((sequence[i], sequence[i + 1]))  # Transition from event i to event i+1

            # Removing duplicates and encoding actions
            actions = list(set(actions))
            action_indices = {action: index for index, action in enumerate(actions)}

    def reward_function(self, state, action_index):
        # Form the tuple and check if it's in actions
        action_tuple = actions[action_index]

        if action_tuple in action_indices:  # Check if this transition exists in the actions
            reward = 3
        else:
            reward = -5

        return reward

    def choose_action(self, state, Q, epsilon=0.9):
        # With probability 1 - epsilon, choose the action that has the maximum Q-value in the current state
        if np.random.rand() > epsilon:
            action = np.argmax(Q[state, :])
        # With probability epsilon, choose a random action
        else:
            action = np.random.choice(len(Q[state, :]))

        return action

    def update_q_value(self, current_q_value, reward, next_max_q_value, learning_rate=0.1, discount_factor=0.9):
        return current_q_value + learning_rate * (reward + discount_factor * next_max_q_value - current_q_value)

    def take_action(self, state, action):
        # Determine the next state based on the chosen action
        next_state = get_next_state(state, action)

        # Determine the reward based on the transition
        reward = reward_function(state, action)

        # Check if the end of the sequence has been reached
        done = is_done(next_state)

        return next_state, reward, done

    def get_next_state(self, state, action):
        # Identify the current event based on the state index
        current_event = states[state]

        # Identify the next event based on the action
        next_event = actions[action][1]  # Assuming actions are tuples representing transitions

        # Find the index of the next event in the states list
        next_state = states.index(next_event)

        return next_state

    def is_done(self, state):
        # Check if the current state is the last event in any of the sequences
        for sequence in sequences:
            if states[state] == sequence[-1]:
                return True
        return False

    def get_initial_state(self):
        # Define the possible starting events
        possible_starting_events = [sequence[0] for sequence in sequences]

        # Choose a random starting event from the possible starting events
        starting_event = np.random.choice(possible_starting_events)

        # Find the index of the starting event in the states list
        initial_state = states.index(starting_event)

        return initial_state

    num_episodes = 100  # Set to the number of sequences

    # Loop through episodes
    for episode in range(num_episodes):
        # Reset environment, get initial state
        state = get_initial_state()
        done = False

        # Loop through steps in episode
        while not done:
            # Choose action based on policy (e.g., epsilon-greedy)
            action = choose_action(state, Q)

            # Take action, observe new state and reward
            next_state, reward, done = take_action(state, action)

            # Update Q-value using Q-learning update rule
            Q[state, action] = update_q_value(Q[state, action], reward, np.max(Q[next_state, :]))

            # Move to next state
            state = next_state

    # Print the Q-table for analysis
    print("Trained Q-table:")
    print(Q)

    # Identify the highest Q-value for each state (event)
    best_actions = np.argmax(Q, axis=1)

    # Print the best action for each state
    for state, action_index in enumerate(best_actions):
        print(
            f"For the event {states[state]}, the best next event is {actions[action_index][1]} with Q-value {Q[state, action_index]}")

    best_sequence_of_events = []
    max_sequence_length = 10

    # Traverse the Q-table to find the best sequence
    for _ in range(max_sequence_length):
        # Find the action with the highest Q-value in the current state
        best_action = np.argmax(Q[state, :])

        # Extract the corresponding event
        best_event = actions[best_action][1]  # Assuming actions are tuples representing transitions

        # Append the event to the sequence
        best_sequence_of_events.append(best_event)

        # Get the next state
        next_state = get_next_state(state, best_action)

        # Check if the end of the sequence has been reached
        if is_done(next_state):  # Define this function to check for the end condition
            break

        # Update the current state
        state = next_state

    # Print the best sequence of events
    print("Sequence of first 10 events that will happen the selected long syscall:")
    for event in best_sequence_of_events:
        print(f"  - {event}")
