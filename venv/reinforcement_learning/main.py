from TraceAnalyzer import TraceAnalyzer
from SyscallAnalyzer import SyscallAnalyzer
from SyscallAggregator import SyscallAggregator
from RLModel import RLModel
from SyscallEventComparator import SyscallEventComparator
from SyscallEventCounter import SyscallEventCounter


def main():
    # File path
    file_path = "/Users/terryxu/Downloads/newtraces.txt"
    # (input("Please enter the file path to analyze: "))

    # Create TraceAnalyzer object
    print(f"start analyzing trace:", flush=True)
    trace_analyzer = TraceAnalyzer(file_path)
    trace_data = trace_analyzer.read_trace_file()

    # Create SyscallAnalyzer object
    print(f"start analyzing syscalls:")
    system_call_analyzer = SyscallAnalyzer(trace_data)
    syscalls = system_call_analyzer.find_syscalls()

    # Create SyscallAggregator object
    print(f"start aggregating system calls:")
    syscall_aggregator = SyscallAggregator(syscalls)
    syscall_aggregator.show_aggregated_data('aggregated_syscalls.txt')
    syscall_aggregator.save_to_csv('syscall_data.csv')

    # Initialize RLModel
    print(f"start RL training:")
    # threshold = float(input("Please enter the threshold time to compare system calls in nanoseconds: "))
    rl_model = RLModel(syscalls, threshold=5000)
    rl_model.run()  # run the model
    rl_model.save_top_actions('RL_actions.txt')

    # Create SyscallEventCounter object
    print(f"start counting events")
    syscall_counter = SyscallEventCounter(syscalls, threshold=5000)
    syscall_counter.categorize_events()
    syscall_counter.save_counting_events('counter.txt')

    # Create SyscallEventComparator object
    print(f"start comparing events")
    syscall_comparator = SyscallEventComparator(syscalls, threshold=5000)
    syscall_comparator.categorize_events()
    syscall_comparator.save_compare_events('comparator.txt')


if __name__ == "__main__":
    main()
