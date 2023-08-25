class CompareSyscalls:
    def __init__(self, syscall_analyzer):
        self.syscall_analyzer = syscall_analyzer

    def analyze_syscalls(self):
        # Iterate through the matched syscalls
        for index, row in self.syscall_analyzer.syscalls_df.iterrows():
            syscall_entry = row['syscall_entry']
            entry_timestamp = row['entry_timestamp']
            exit_timestamp = row['exit_timestamp']

            # Find the events between the entry and exit timestamps
            events_between = self.syscall_analyzer.find_events_between(entry_timestamp, exit_timestamp, self.syscall_analyzer.trace_data)

            # Extract the event names (or other relevant information) into a sequence
            sequence = [event['Event Name'] for event in events_between]

            # Check if this syscall has been analyzed before
            syscall_name = syscall_entry.replace('syscall_entry_', '')
            if syscall_name in self.syscall_analyzer.sequences:
                self.syscall_analyzer.sequences[syscall_name].append(sequence)
            else:
                self.syscall_analyzer.sequences[syscall_name] = [sequence]

    def print_sequences(self):
        for syscall, sequences in self.syscall_analyzer.sequences.items():
            print(f"Syscall: {syscall}")
            if len(sequences) == 1:
                print(f"Only one occurrence found. Sequence: {sequences[0]}")
            else:
                print(f"Found {len(sequences)} occurrences:")
                for i, seq in enumerate(sequences):
                    print(f"Sequence {i + 1}: {seq}")
