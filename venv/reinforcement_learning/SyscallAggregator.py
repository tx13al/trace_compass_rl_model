import csv
from collections import defaultdict
from tqdm import tqdm

class SyscallAggregator:
    def __init__(self, syscalls):
        self.syscalls = syscalls
        self.syscall_groups = defaultdict(list)
        self.aggregate_syscalls()

    def aggregate_syscalls(self):
        for syscall in tqdm(self.syscalls, desc="Aggregating syscalls",
                            bar_format='{l_bar}\033[90m{bar}\033[0m{r_bar}'):
            self.syscall_groups[syscall.event_type].append(syscall)

    def show_aggregated_data(self, filename):
        with open(filename, 'w') as f:
            for syscall_type, syscalls in self.syscall_groups.items():
                f.write(f"Syscall Type: {syscall_type}\n")

                durations = [syscall.duration for syscall in syscalls]
                avg_duration = sum(durations) / len(durations)
                min_duration = min(durations)
                max_duration = max(durations)

                f.write(f"  Average Duration: {round(avg_duration)}\n")
                f.write(f"  Min Duration: {round(min_duration)}\n")
                f.write(f"  Max Duration: {round(max_duration)}\n")

                f.write("  Associated Events:\n")
                for syscall in syscalls:
                    f.write(f"    System_call: {syscall}\n")
                    for event in syscall.events:
                        f.write(f"      {event}\n")

    def save_to_csv(self, filename):
        with open(filename, 'w', newline='') as csvfile:
            fieldnames = ['Syscall Type', 'Average Duration in nanosecond', 'Min Duration in nanosecond', 'Max Duration in nanosecond']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for syscall_type, syscalls in self.syscall_groups.items():
                durations = [syscall.duration for syscall in syscalls]
                avg_duration = sum(durations) / len(durations)
                min_duration = min(durations)
                max_duration = max(durations)

                writer.writerow({
                    'Syscall Type': syscall_type,
                    'Average Duration in nanosecond': round(avg_duration),
                    'Min Duration in nanosecond': round(min_duration),
                    'Max Duration in nanosecond': round(max_duration)
                })
