import pandas as pd
from Syscall import Syscall
from Event import Event
from tqdm import tqdm


class SyscallAnalyzer:
    def __init__(self, trace_data):
        self.syscalls = []
        self.events = trace_data

    def parse_timestamp(self, timestamp):
        time_parts = timestamp.split(':')
        hours, minutes, seconds = int(time_parts[0]), int(time_parts[1]), float(time_parts[2])
        return hours * 3600 + minutes * 60 + seconds

    def find_syscalls(self):
        current_syscall = None

        for event in tqdm(self.events, desc="Finding syscalls", bar_format='{l_bar}\033[90m{bar}\033[0m{r_bar}'):
            timestamp = self.parse_timestamp(event.timestamp)

            if 'syscall_entry' in event.event_type:
                current_syscall = Syscall(
                    event.event_type,
                    event.cpu_id.replace("cpu_id = ", ""),
                    event.tid,
                    event.prio,
                    timestamp,
                    0,
                    event.timestamp,
                    None,
                    event.content)
            elif current_syscall and 'syscall_exit' in event.event_type and event.event_type.replace('exit',
                                                                                                     'entry') == current_syscall.event_type:
                current_syscall.end_time = event.timestamp
                current_syscall.parsed_end_time = timestamp
                current_syscall.duration = (timestamp - current_syscall.parsed_start_time) * 1000000000
                current_syscall.event_type = current_syscall.event_type.replace("syscall_entry_", "")

                self.syscalls.append(current_syscall)
                current_syscall = None
            else:
                if current_syscall:
                    current_syscall.add_event(event.event_type)
        return self.syscalls

    def print_syscalls(self, filename):
        with open(filename, 'w') as f:
            for syscall in self.syscalls:
                f.write(f"Syscall type: {syscall}\n")
                for event in syscall.events:
                    f.write(f"    Event: {event}\n")
