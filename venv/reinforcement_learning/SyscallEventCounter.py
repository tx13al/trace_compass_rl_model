from collections import defaultdict, Counter
from itertools import chain
from tqdm import tqdm


class SyscallEventCounter:
    def __init__(self, syscalls, threshold):
        self.syscalls = syscalls
        self.threshold = threshold
        self.events_in_long_syscalls = defaultdict(list)
        self.events_in_short_syscalls = defaultdict(list)
        self.syscall_frequency_counter = Counter()

    def categorize_events(self):
        for syscall in self.syscalls:
            self.syscall_frequency_counter[syscall.event_type] += 1  # Counting frequency
            if syscall.duration > self.threshold:
                self.events_in_long_syscalls[syscall.event_type].append(syscall.events)
            else:
                self.events_in_short_syscalls[syscall.event_type].append(syscall.events)

    def save_counting_events(self, filename):
        with open(filename, 'w') as f:
            all_event_types = set(self.events_in_short_syscalls.keys()) | set(self.events_in_long_syscalls.keys())
            for event_type in tqdm(all_event_types, desc="Saving events", bar_format='{l_bar}\033[90m{bar}\033[0m{r_bar}'):

                flat_long_events = list(chain.from_iterable(self.events_in_long_syscalls[event_type]))
                flat_short_events = list(chain.from_iterable(self.events_in_short_syscalls.get(event_type, [])))

                long_syscall_events = Counter(flat_long_events)
                short_syscall_events = Counter(flat_short_events)

                sorted_long = long_syscall_events.most_common()
                sorted_short = short_syscall_events.most_common()

                frequency = self.syscall_frequency_counter[event_type]

                f.write(f"For syscall type {event_type}:\n")
                f.write(f"{event_type} happens: {frequency} times\n")
                f.write(f"  Events in long syscalls: \n")
                for event, count in sorted_long:
                    f.write(f"    {event}: {count}\n")
                f.write(f"  Events in short syscalls: \n")
                for event, count in sorted_short:
                    f.write(f"    {event}: {count}\n")