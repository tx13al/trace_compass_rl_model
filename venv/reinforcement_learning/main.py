#from QLearning import QLearningClass
from TraceAnalyzer import TraceAnalyzer
from SyscallAnalyzer import SyscallAnalyzer
from CompareSyscalls import CompareSyscalls

def main():
    # File path
    file_path = input("Please enter the file path to analyze: ")
    # Create TraceAnalyzer object
    trace_analyzer = TraceAnalyzer(file_path)
    threshold = input("Please enter the threshold time to compare system calls: (ex.0.00050s is 500ms")
    system_call_analyzer = SyscallAnalyzer(trace_analyzer, threshold)
    # Create an instance of SyscallAnalyzer and find syscalls
    system_call_analyzer.find_syscalls()

    # Create an instance of CompareSyscalls and analyze syscalls
    syscall_comparator = CompareSyscalls(system_call_analyzer)
    syscall_comparator.analyze_syscalls()

    # Print the sequences
    syscall_comparator.print_sequences()
    # Apply Q-learning on sequences
    #q_learning_sequences = QLearningSequences(sequences, states, actions)


if __name__ == "__main__":
    main()
