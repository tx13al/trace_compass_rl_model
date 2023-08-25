import pandas as pd


class SyscallAnalyzer:
    def __init__(self, trace_data, threshold):
        self.trace_data = trace_data
        self.duration = threshold
        self.valid_long_syscalls = []
        self.sequences = []

    @staticmethod
    def all_system_calls():
        return [
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

    def parse_timestamp(self, timestamp):
        time_parts = timestamp.split(':')
        hours, minutes, seconds = int(time_parts[0]), int(time_parts[1]), float(time_parts[2])
        return hours * 3600 + minutes * 60 + seconds

    def find_syscalls(self):
        # Initialize variables to keep track of the matched syscalls
        syscalls = []
        current_syscall_entry = None
        current_timestamp = 0

        # Iterate through the dataframe to find matched syscalls
        for index, row in trace_data.iterrows():
            timestamp = parse_timestamp(row['Timestamp'])
            event_name = row['Event Name']

            if 'syscall_entry' in event_name:
                current_syscall_entry = event_name
                current_timestamp = timestamp

            elif 'syscall_exit' in event_name and current_syscall_entry and event_name.replace('exit',
                                                                                               'entry') == current_syscall_entry:
                duration = timestamp - current_timestamp
                if duration > self.duration:
                    syscalls.append({
                        'syscall_entry': current_syscall_entry,
                        'syscall_exit': event_name,
                        'entry_timestamp': current_timestamp,
                        'exit_timestamp': timestamp,
                        'duration': duration
                    })
                current_syscall_entry = None

        # Convert syscalls to dataframe
        syscalls_df = pd.DataFrame(syscalls)
        pd.set_option('display.max_columns', None)
        print(syscalls_df)

    def find_available_syscalls(self):
        # Extract syscall names from both entry and exit, and remove the prefixes
        extracted_long_syscalls = syscalls_df['syscall_entry'].apply(
            lambda x: x.replace('syscall_entry_', '')).unique()

        all_syscalls = self.all_system_calls()
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

    # Function to find events between entry and exit timestamps for syscalls

    def find_events_between(self, entry_timestamp, exit_timestamp, original_data):
        events_between = []
        for index, row in original_data.iterrows():
            timestamp = parse_timestamp(row['Timestamp'])
            if entry_timestamp < timestamp < exit_timestamp:
                events_between.append(row.to_dict())
        return events_between

    # List to hold the sequences of events for the selected syscall
    sequences = []

    # Iterate through the matched syscalls for the selected syscall
    for index, row in syscalls_df.iterrows():
        if selected_long_syscall in row['syscall_entry']:
            entry_timestamp = row['entry_timestamp']
            exit_timestamp = row['exit_timestamp']

            # Find the events between the entry and exit timestamps
            events_between = find_events_between(entry_timestamp, exit_timestamp, trace_data)

            # Extract the event names (or other relevant information) into a sequence
            sequence = [event['Event Name'] for event in events_between]

            # Append the sequence to the list of sequences
            sequences.append(sequence)
