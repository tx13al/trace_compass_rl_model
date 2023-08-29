import subprocess
import time
import sys
import os  # Import the os module


def run(command):
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    if process.returncode != 0:
        print(f"Error executing command: {stderr.decode().strip()}")


# Get the directory where the script is located
current_dir = os.path.dirname(os.path.abspath(__file__))

# Define the path to the 'data' folder relative to the script's location
data_dir = os.path.join(os.path.dirname(current_dir), 'data')

trace_duration = 3
trace_path = data_dir  # Set trace_path to the data directory

try:
    number_traces = int(input("Please input the number of traces:"))
except ValueError:
    print("Invalid input. Please enter an integer value.")
    exit(1)

for i in range(number_traces):
    print(f"Starting trace {i + 1}...")
    run(f"lttng add-context --kernel --channel=my-channel --type=tid")
    run(f"lttng create my_session --output={trace_path}")
    run("lttng enable-event -k -a")
    run("lttng start")
    time.sleep(trace_duration)
    run("lttng stop")
    run("lttng destroy")
    print(f"Trace {i + 1} completed. \n")

print(f"All {number_traces} traces completed.")
run(f"babeltrace2 {trace_path} > {os.path.join(data_dir, f'output.txt')}")
