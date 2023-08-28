# Importing necessary libraries
import numpy as np
import re
import pandas as pd

file_path = '/Users/terryxu/Downloads/newtraces.txt'

# Regular expression to match the pattern
pattern = r'\[(.*?)\] \((.*?)\)(.*?) (.*?) (.*?): \{(.*)\}'

# Lists to hold the extracted data
timestamps = []
time_diffs = []
computer_names = []
event_names = []
other_info = []

# Reading the file and extracting the details
with open(file_path, 'r') as file:
    for line in file:
        match = re.match(pattern, line)
        if match:
            timestamps.append(match.group(1))
            time_diffs.append(match.group(2))
            computer_names.append(match.group(4).strip())
            event_names.append(match.group(5))
            other_info.append(match.group(6))

# Creating a DataFrame
trace_data = pd.DataFrame({
    'Timestamp': timestamps,
    'Time Diff': time_diffs,
    'Event Name': event_names,
})

# Displaying the first few rows to see the structure
trace_data.head()


# Function to parse the timestamp and convert to seconds
def parse_timestamp(timestamp):
    time_parts = timestamp.split(':')
    hours, minutes, seconds = int(time_parts[0]), int(time_parts[1]), float(time_parts[2])
    return hours * 3600 + minutes * 60 + seconds


# Define threshold for long syscalls
threshold_duration = 0.000050

# Initialize variables to keep track of the syscalls
matched_syscalls = []
current_syscall_entry = None
current_timestamp = 0

# Iterate through the dataframe to find syscalls
for index, row in trace_data.iterrows():
    timestamp = parse_timestamp(row['Timestamp'])
    event_name = row['Event Name']

    if 'syscall_entry' in event_name:
        current_syscall_entry = event_name
        current_timestamp = timestamp

    elif 'syscall_exit' in event_name and current_syscall_entry and event_name.replace('exit',
                                                                                       'entry') == current_syscall_entry:
        duration = timestamp - current_timestamp
        if duration > threshold_duration:
            matched_syscalls.append({
                'syscall_entry': current_syscall_entry,
                'syscall_exit': event_name,
                'entry_timestamp': current_timestamp,
                'exit_timestamp': timestamp,
                'duration': duration
            })
        current_syscall_entry = None

# Convert matched syscalls to dataframe
matched_syscalls_df = pd.DataFrame(matched_syscalls)
pd.set_option('display.max_columns', None)
# print(matched_syscalls_df)

# List of all syscalls
all_syscalls = [
    "_sysctl",
    "accept",
    "accept4",
    "access",
    "acct",
    "add_key",
    "adjtimex",
    "afs_syscall",
    "alarm",
    "arch_prctl",
    "bind",
    "bpf",
    "brk",
    "capget",
    "capset",
    "chdir",
    "chmod",
    "chown",
    "chroot",
    "clock_adjtime",
    "clock_getres",
    "clock_gettime",
    "clock_nanosleep",
    "clock_settime",
    "clone",
    "close",
    "connect",
    "copy_file_range",
    "creat",
    "create_module",
    "delete_module",
    "dup",
    "dup2",
    "dup3",
    "epoll_create",
    "epoll_create1",
    "epoll_ctl",
    "epoll_ctl_old",
    "epoll_pwait",
    "epoll_wait",
    "epoll_wait_old",
    "eventfd",
    "eventfd2",
    "execve",
    "execveat",
    "exit",
    "exit_group",
    "faccessat",
    "fadvise64",
    "fallocate",
    "fanotify_init",
    "fanotify_mark",
    "fchdir",
    "fchmod",
    "fchmodat",
    "fchown",
    "fchownat",
    "fcntl",
    "fdatasync",
    "fgetxattr",
    "finit_module",
    "flistxattr",
    "flock",
    "fork",
    "fremovexattr",
    "fsetxattr",
    "fstat",
    "fstatfs",
    "fsync",
    "ftruncate",
    "futex",
    "futimesat",
    "get_kernel_syms",
    "get_mempolicy",
    "get_robust_list",
    "get_thread_area",
    "getcpu",
    "getcwd",
    "getdents",
    "getdents64",
    "getegid",
    "geteuid",
    "getgid",
    "getgroups",
    "getitimer",
    "getpeername",
    "getpgid",
    "getpgrp",
    "getpid",
    "getpmsg",
    "getppid",
    "getpriority",
    "getrandom",
    "getresgid",
    "getresuid",
    "getrlimit",
    "getrusage",
    "getsid",
    "getsockname",
    "getsockopt",
    "gettid",
    "gettimeofday",
    "getuid",
    "getxattr",
    "init_module",
    "inotify_add_watch",
    "inotify_init",
    "inotify_init1",
    "inotify_rm_watch",
    "io_cancel",
    "io_destroy",
    "io_getevents",
    "io_setup",
    "io_submit",
    "ioctl",
    "ioperm",
    "iopl",
    "ioprio_get",
    "ioprio_set",
    "kcmp",
    "kexec_file_load",
    "kexec_load",
    "keyctl",
    "kill",
    "lchown",
    "lgetxattr",
    "link",
    "linkat",
    "listen",
    "listxattr",
    "llistxattr",
    "lookup_dcookie",
    "lremovexattr",
    "lseek",
    "lsetxattr",
    "lstat",
    "madvise",
    "mbind",
    "membarrier",
    "memfd_create",
    "migrate_pages",
    "mincore",
    "mkdir",
    "mkdirat",
    "mknod",
    "mknodat",
    "mlock",
    "mlock2",
    "mlockall",
    "mmap",
    "modify_ldt",
    "mount",
    "move_pages",
    "mprotect",
    "mq_getsetattr",
    "mq_notify",
    "mq_open",
    "mq_timedreceive",
    "mq_timedsend",
    "mq_unlink",
    "mremap",
    "msgctl",
    "msgget",
    "msgrcv",
    "msgsnd",
    "msync",
    "munlock",
    "munlockall",
    "munmap",
    "name_to_handle_at",
    "nanosleep",
    "newfstatat",
    "nfsservctl",
    "open",
    "open_by_handle_at",
    "openat",
    "pause",
    "perf_event_open",
    "personality",
    "pipe",
    "pipe2",
    "pivot_root",
    "pkey_alloc",
    "pkey_free",
    "pkey_mprotect",
    "poll",
    "ppoll",
    "prctl",
    "pread64",
    "preadv",
    "preadv2",
    "prlimit64",
    "process_vm_readv",
    "process_vm_writev",
    "pselect6",
    "ptrace",
    "putpmsg",
    "pwrite64",
    "pwritev",
    "pwritev2",
    "query_module",
    "quotactl",
    "read",
    "readahead",
    "readlink",
    "readlinkat",
    "readv",
    "reboot",
    "recvfrom",
    "recvmmsg",
    "recvmsg",
    "remap_file_pages",
    "removexattr",
    "rename",
    "renameat",
    "renameat2",
    "request_key",
    "restart_syscall",
    "rmdir",
    "rt_sigaction",
    "rt_sigpending",
    "rt_sigprocmask",
    "rt_sigqueueinfo",
    "rt_sigreturn",
    "rt_sigsuspend",
    "rt_sigtimedwait",
    "rt_tgsigqueueinfo",
    "sched_get_priority_max",
    "sched_get_priority_min",
    "sched_getaffinity",
    "sched_getattr",
    "sched_getparam",
    "sched_getscheduler",
    "sched_rr_get_interval",
    "sched_setaffinity",
    "sched_setattr",
    "sched_setparam",
    "sched_setscheduler",
    "sched_yield",
    "seccomp",
    "security",
    "select",
    "semctl",
    "semget",
    "semop",
    "semtimedop",
    "sendfile",
    "sendmmsg",
    "sendmsg",
    "sendto",
    "set_mempolicy",
    "set_robust_list",
    "set_thread_area",
    "set_tid_address",
    "setdomainname",
    "setfsgid",
    "setfsuid",
    "setgid",
    "setgroups",
    "sethostname",
    "setitimer",
    "setns",
    "setpgid",
    "setpriority",
    "setregid",
    "setresgid",
    "setresuid",
    "setreuid",
    "setrlimit",
    "setsid",
    "setsockopt",
    "settimeofday",
    "setuid",
    "setxattr",
    "shmat",
    "shmctl",
    "shmdt",
    "shmget",
    "shutdown",
    "sigaltstack",
    "signalfd",
    "signalfd4",
    "socket",
    "socketpair",
    "splice",
    "stat",
    "statfs",
    "statx",
    "swapoff",
    "swapon",
    "symlink",
    "symlinkat",
    "sync",
    "sync_file_range",
    "syncfs",
    "sysfs",
    "sysinfo",
    "syslog",
    "tee",
    "tgkill",
    "time",
    "timer_create",
    "timer_delete",
    "timer_getoverrun",
    "timer_gettime",
    "timer_settime",
    "timerfd_create",
    "timerfd_gettime",
    "timerfd_settime",
    "times",
    "tkill",
    "truncate",
    "tuxcall",
    "umask",
    "umount2",
    "uname",
    "unlink",
    "unlinkat",
    "unshare",
    "uselib",
    "userfaultfd",
    "ustat",
    "utime",
    "utimensat",
    "utimes",
    "vfork",
    "vhangup",
    "vmsplice",
    "vserver",
    "wait4",
    "waitid",
    "write",
    "writev"
]

# Extract syscall names from both entry and exit, and remove the prefixes
extracted_long_syscalls = matched_syscalls_df['syscall_entry'].apply(lambda x: x.replace('syscall_entry_', '')).unique()

# Filter long syscalls that are in the list of all syscalls
valid_long_syscalls = [syscall for syscall in extracted_long_syscalls if syscall in all_syscalls]

# Print the valid long syscalls and ask the user to select one
print("Available long syscalls for analysis:")
for index, syscall in enumerate(valid_long_syscalls):
    print(f"{index}. {syscall}")

# Get user input for syscall selection
selected_index = int(input("Please select the long syscall to analyze (enter the index number): "))
selected_long_syscall = valid_long_syscalls[selected_index]

# Print the selected long syscall
print(f"You have selected the long syscall: {selected_long_syscall}")


# Function to find events between entry and exit timestamps for matched syscalls
def find_events_between(entry_timestamp, exit_timestamp, original_data):
    events_between = []
    for index, row in original_data.iterrows():
        timestamp = parse_timestamp(row['Timestamp'])
        if entry_timestamp < timestamp < exit_timestamp:
            events_between.append(row.to_dict())
    return events_between


# List to hold the sequences of events for the selected syscall
sequences = []

# Iterate through the matched syscalls for the selected syscall
for index, row in matched_syscalls_df.iterrows():
    if selected_long_syscall in row['syscall_entry']:
        entry_timestamp = row['entry_timestamp']
        exit_timestamp = row['exit_timestamp']

        # Find the events between the entry and exit timestamps
        events_between = find_events_between(entry_timestamp, exit_timestamp, trace_data)

        # Extract the event names (or other relevant information) into a sequence
        sequence = [event['Event Name'] for event in events_between]

        # Append the sequence to the list of sequences
        sequences.append(sequence)

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

Q = np.zeros((len(states), len(actions)))


def reward_function(state, action_index):
    # Form the tuple and check if it's in actions
    action_tuple = actions[action_index]

    if action_tuple in action_indices:  # Check if this transition exists in the actions
        reward = 3
    else:
        reward = -5

    return reward


def choose_action(state, Q, epsilon=0.5):
    # With probability 1 - epsilon, choose the action that has the maximum Q-value in the current state
    if np.random.rand() > epsilon:
        action = np.argmax(Q[state, :])
    # With probability epsilon, choose a random action
    else:
        action = np.random.choice(len(Q[state, :]))

    return action


def update_q_value(current_q_value, reward, next_max_q_value, learning_rate=0.1, discount_factor=0.9):
    return current_q_value + learning_rate * (reward + discount_factor * next_max_q_value - current_q_value)


def take_action(state, action):
    # Determine the next state based on the chosen action
    next_state = get_next_state(state, action)

    # Determine the reward based on the transition
    reward = reward_function(state, action)

    # Check if the end of the sequence has been reached
    done = is_done(next_state)

    return next_state, reward, done


def get_next_state(state, action):
    # Identify the current event based on the state index
    current_event = states[state]

    # Identify the next event based on the action
    next_event = actions[action][1]  # Assuming actions are tuples representing transitions

    # Find the index of the next event in the states list
    next_state = states.index(next_event)

    return next_state


def is_done(state):
    # Check if the current state is the last event in any of the sequences
    for sequence in sequences:
        if states[state] == sequence[-1]:
            return True
    return False


def get_initial_state():
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
    best_event = actions[best_action][1]

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
