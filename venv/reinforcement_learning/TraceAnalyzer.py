import re
import pandas as pd
from Event import Event
from tqdm import tqdm


class TraceAnalyzer:
    def __init__(self, file_path):
        self.file_path = file_path
        self.pattern = r'\[(.*?)\] \((.*?)\)(.*?) (.*?) (.*?): \{(.*)\},\ \{(.*)\},\ \{(.*)\}'

    def read_trace_file(self):

        # Variables to hold the last tid and prio
        last_tid, last_prio = None, None
        events = []
        total_lines = sum(1 for _ in open(self.file_path))

        # Reading the file and extracting the details
        with open(self.file_path, 'r') as file:
            for line in tqdm(file, total=total_lines, desc="Reading file", bar_format='{l_bar}\033[90m{bar}\033[0m{r_bar}'):
                match = re.match(self.pattern, line)
                if match:
                    timestamp = match.group(1)
                    event_type = match.group(5)
                    cpu_id = match.group(6).replace("cpu_id = ", "")
                    tid = match.group(7)
                    content = match.group(8)

                    # Extracting tid and prio from content if available
                    prio = re.search(r'prio\s*=\s*(\d+)', content)

                    prio = prio.group(1) if prio else last_prio

                    # Update last_prio
                    last_prio = prio

                    event = Event(timestamp, event_type, cpu_id, tid, prio, content)
                    events.append(event)
        return events

    def print_events(self):
        for event in self.read_trace_file():
            print(event)
