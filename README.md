# Reinforcement Learning to analyst system calls 

## Table of Contents

- [Environment Setup](#environment-setup)
- [Training the Model](#training-the-model)
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
   

## Training the Model
- Python codes that used to train the Reinfocement Learning model
   - gather the tracing data (traces.py)
   - parse the data (parseoutput.py)
   - Q-learing reinforcement learning model (qlearn.py)
 

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