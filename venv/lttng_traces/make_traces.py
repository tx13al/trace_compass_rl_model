import subprocess
import time
import sys


def run(command):
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    if process.returncode != 0:
        print(f"Error executing command: {stderr.decode().strip()}")


if len(sys.argv) < 2:
    print("Please provide the trace path as the command-line")
    exit(1)

trace_duration = 3
trace_path = sys.argv[1]

try:
    number_traces = int(input("Please input the number of traces:"))
except ValueError:
    print("Invalid input. Please enter an integer value.")
    exit(1)

for i in range(number_traces):
    print(f"Starting trace {i + 1}...")
    run(f"lttng create my_session --output={trace_path}")
    run("lttng enable-event -k -a")
    run("lttng start")
    time.sleep(trace_duration)
    run("lttng stop")
    run("lttng destroy")
    print(f"Trace {i + 1} completed. \n")
print(f"All {number_traces} traces completed.")
run(f"babeltrace2 {trace_path} > output{number_traces}.txt")
