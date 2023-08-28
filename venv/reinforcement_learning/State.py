class State:
    def __init__(self, syscall_type, duration_type):
        self.syscall_type = syscall_type
        self.duration_type = duration_type

    def __hash__(self):
        return hash((self.syscall_type, self.duration_type))

    def __eq__(self, other):
        return (self.syscall_type, self.duration_type) == (other.syscall_type, other.duration_type)

    def __str__(self):
        return f"State(syscall_type={self.syscall_type}, duration_type={self.duration_type})"
