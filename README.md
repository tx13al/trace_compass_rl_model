# Reinforcement Learning for System Trace Analysis

## Table of Contents

- [Environment Setup](#environment-setup)
- [Reinforcement Learning for System Trace Analysis](#reinforcement-learning-for-system-trace-analysis-1)
- [References](#references)

## Environment Setup

### Prerequisites

- Ubuntu 18.04
- VirtualBox


1. **Download Ubuntu 18.04:**
   Download the Ubuntu 18.04 LTS image from [this link](https://releases.ubuntu.com/18.04/).

2. **Install VirtualBox:**
   Follow the instructions on the [VirtualBox website](https://www.virtualbox.org/wiki/Downloads) to install VirtualBox.

3. **Create a VirtualBox virtual machine with Ubuntu 18.04:**
   Use the downloaded Ubuntu image to create a virtual machine inside VirtualBox.
   Follow the instructions on [this link](https://ubuntu.com/tutorials/how-to-run-ubuntu-desktop-on-a-virtual-machine-using-virtualbox#1-overview).
   
### Installation

1. ### Install LTTng:
   1. **Install Git:** For clone lttng repository from github
      Open a terminal inside the virtual machine and run:
      ```bash
      $ sudo apt-get update
      $ sudo apt-get install git
      ```

   2. **Installing Nautilus Admin Extension:**
      For open root files by using file explorer:
      ```bash
      $ sudo apt-get install nautilus-admin
      $ nautilus -q
      ```
   3. **Installing LTTng from Source:**
      For detailed instructions on installing LTTng from source, refer to this [guide by IBM](https://www.ibm.com/support/pages/howto-tracing-lttng).
      ```bash
      sudo apt-get install autoconf automake libtool pkg-config
      ```
      ```bash
      # Cloning LTTng source code
      $ git clone git://git.lttng.org/lttng-tools.git
      $ git clone git://git.lttng.org/lttng-modules.git
      $ git clone git://git.lttng.org/lttng-ust.git
      $ git clone git://git.lttng.org/userspace-rcu.git
      ```
      ```bash
      # Buiding and installing liburcu library
      $ cd userspace-rcu
      $ ./bootstrap
      $ ./configure
      $ make
      $ make install
      $ sudo ldconfig
      ```
      ```bash
      # Bulding and installing lttng-ust
      $ cd lttng-ust
      $ ./bootstrap
      $ ./configure
      $ make
      $ make install
      $ ldconfig
      ```
      ```bash
      # Building and installing lttng-tools
      $ cd lttng-tools
      $ ./bootstrap
      $ ./configure
      $ make
      $ make install
      $ ldconfig
      ```
      ```bash
      # Building and installing lttng-modules
      $ cd lttng-modules
      $ make
      $ sudo make modules_install
      $ sudo depmod -a
      ```
      ```bash
      # Check LTTng version
      $ lttng --version
      ```
   4. **Troubleshooting:**\
   Refer to the [official LTTng documentation](https://lttng.org/docs/v2.13/) and the GitHub repository's README for specific troubleshooting steps and additional configuration options.\
   **Errors that I occured and solutions:**\
   Error During ./configure:\
   Bison >= 2.4 Required\
      Solution: install Bison, verify version and rerun ./configure
      ```bash
      $ sudo apt-get install bison
      $ bison --version
      $ ./configure
      ```
      Flex >= 2.5.35 Required\
      Solution: install Flex, verify version and rerun ./configure
      ```bash
      $ sudo apt-get install flex
      $ flex --version
      $ ./configure
      ```
      Cannot Find libpopt:\
      Solution: install libpopt Library & rerun ./configure
      ```bash
      $ sudo apt-get install libpopt-dev
      $ ./configure
      ```
      libxml-2.0 >= 2.7.6 Not Found:\
      Solution: install libxml2 Library & rerun ./configure
      ```bash
      $ sudo apt-get install libxml2-dev
      $ ./configure
      ```
      liburcu Version Not Met:\
      Solution:
      ```bash
      $ sudo apt-get remove liburcu-dev # Uninstall the Existing liburcu Library
      $ sudo apt-get update # Update Package List
      $ sudo apt-get install liburcu-dev # Install the Required liburcu Library:
      $ ./configure # Rerun ./configure
      ```
2. **Run your first LTTng trace:**
   ```bash
   $ lttng create #create an auto lttng session
   $ lttng enable-event -k -a #enable kernal
   $ lttng start #start tracing
   $ lttng stop #stop tracing
   $ lttng destroy #lttng destroy session. This step WILL NOT destroy the lttng tracing data.
   ```
3. **Print your result by using Babeltrace2:**
   ```bash
    $ babeltrace2 /root/lttng-traces/auto-xxxxxxxx - xxxxxx #change this directory to your trace data file location
    ```
4. **Possible error: Kernel tracer not available**\
   Reinstall lttng-modules
   ```bash
   $ cd lttng-modules
   $ make
   $ sudo make modules_install
   $ sudo depmod -a
   ```
5. ### Installing Trace Compass on Ubuntu 
   Trace Compass/Development Environment Setup Guide follow [this website](https://wiki.eclipse.org/Trace_Compass/Development_Environment_Setup).

   1. **Download the latest Trace Compass from the official website:**
      You can find the latest Trace Compass releases [here](https://eclipse.dev/tracecompass/). 
      
   2. **Extract the downloaded archive:**
      Extract the downloaded tar.gz file to a location of your choice.
Or run following on commend line:
       ```bash
       $ tar xzvf eclipse-committers-2023-03-R-linux-gtk-x86_64.tar.gz 
       $ cd eclipse
       $ ./eclipse
      ```
   3. **Install required dependencies:**
      Trace Compass uses source compatibility to Java 11. However, to run the Trace Compass RCP and to develop it, Java 17 is required. Here is how to install Java 17 on recent Ubuntu:
      ```bash
      $ sudo apt-get install openjdk-17-jdk

6. ### Trace Compass Instruction
   Learn Trace Compass Main Features and how to import traces to the project from [this website](https://archive.eclipse.org/tracecompass/doc/stable/org.eclipse.tracecompass.doc.user/Trace-Compass-Main-Features.html#Project_Explorer_View).
   

## Reinforcement Learning for System Trace Analysis

### Introduction
This project utilizes Reinforcement Learning (RL) to analyze system traces, specifically focusing on system calls. The main goal is to understand the events happen between long system calls entry and exit, thus helping in system optimization.

### Requirements
- Python 3.8+
- pandas
- tqdm

### Usage
- Execute the lttng tracing script first under folder ../lttng_traces:
  ```bash
  python3 make_traces.py
  ```
   Then you will have tracing data in ../data/my_session and an output as ..data/output.txt
- Execute the main script to start the analysis:
    ```bash
  python3 main.py
  ```
### Modules Overview
- **/data**: all data output in this folder
  - **/my_session**: tracing data
  - **aggregated_syscalls.txt**: systems calls with average, min, and max durations and associated events that happened between each system call entry and exit.
  - **comparator.txt**: compare system call events in long and short syscalls by using threshold of 5000 nanoseconds. This file shows what events happen in long system calls but not in short system calls.
  - **counter.txt**: count how many times each system calls happen in the tracing data and how many times of the events happens in each system calls.
  - **output.txt**: babeltrace convert tracing data to a readable txt file.
  - **RL_actions.txt**: output of the model that shows lists of events that most likely happen in both long and short system calls.
  - **syscall_data.csv**: output for showing systems and their average, min, and max durations. Easy to use in an excel and analyze the syscalls.
  - **syscalls.txt**: result of all system calls with all information are sorted by timestamp and the events happen between system call entry and exit.
- **/lttng_traces**
  - **make_traces.py**: Utility script for generating traces.
- /original_code
  - archived
- **/reinforcement_learning**
  - **Action.py**: Action object. Defines actions in the RL model. 
  - **Agent.py**: Agent object. The RL agent that learns from actions and states. 
  - **Event.py**: Event object. Represents events in the tracing data. 
  - **main.py**: The entry point of the application. 
  - **QTable.py**: QTable object. Represents the Q-table for the Q-Learning algorithm. 
  - **RLModel.py**: The main RL model that holding the reward function, train the model and print a result as **RL_actions.txt**. 
    - **reward function**: 
    - get 3 points when the state is a long system call
    - get -5 point when the state is a short system call
  - **State.py**: State object. Represents states in the RL model. 
  - **Syscall.py**: Syscall object. Represents system calls. 
  - **SyscallAggregator.py**: Utility for aggregating system call data. Calculate average, min, and max duration of each system calls and the associated events of the system call. Output as **aggregated_syscalls.txt**.
  - **SyscallAnalyzer.py**: Analyzes system calls and export the data as **syscalls.txt**. Another result file named **syscall_data.csv** uses to show the list of system calls happen in the tracing and the average, min, and max duration of each system syscall.
  - **SyscallEventComparator.py**: Compares system call events. Compare which events are in long system calls but not in short system calls and vice versa. Export data as **comparator.txt**.
  - **SyscallEventCounter.py**: Counts system call event. Count how many times the events happen in the trace. Export data as **counter.txt**.
  - **TraceAnalyzer.py**: Analyzes traces by using **output.txt** from **make_traces.py**.
      

    


## References
https://releases.ubuntu.com/18.04/ \
https://www.virtualbox.org/wiki/Downloads \
https://ubuntu.com/tutorials/how-to-run-ubuntu-desktop-on-a-virtual-machine-using-virtualbox#1-overview \
https://www.ibm.com/support/pages/howto-tracing-lttng \
https://lttng.org/docs/v2.13/ \
https://babeltrace.org/docs/v2.0/python/bt2/examples.html \
https://github.com/tracecompass/tracecompass \
https://tracingsummit.org/ts/2019/files/Tracingsummit2019-babeltrace2-marchi.pdf \
https://ardupilot.org/dev/docs/using-linux-trace-toolkit-ng-lttng-to-trace-ardupilot-in-realtime.html# \
https://www.efficios.com/pub/lfcs2013/collab-2013-slides.pdf \
https://tracingsummit.org/ts/2014/files/Tracingsummit2014-gbastien.pdf \
https://eclipse.dev/tracecompass/ \
https://wiki.eclipse.org/Trace_Compass/Development_Environment_Setup \
https://archive.eclipse.org/tracecompass/doc/stable/org.eclipse.tracecompass.doc.user/Trace-Compass-Main-Features.html#Project_Explorer_View