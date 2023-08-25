class TraceAnalyzer:
    def __init__(self, file_path):
        self.file_path = file_path
        self.pattern = r'\[(.*?)\] \((.*?)\)(.*?) (.*?) (.*?): \{(.*)\}'
        self.all_syscalls = all_syscalls
        self.trace_data = self.read_trace_file()
        self.matched_syscalls_df = None

    def read_trace_file(self):
        # Lists to hold the extracted data
        timestamps, time_diffs, computer_names, event_names, other_info = [], [], [], [], []

        # Reading the file and extracting the details
        with open(self.file_path, 'r') as file:
            for line in file:
                match = re.match(self.pattern, line)
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

        return trace_data

