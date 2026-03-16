# Simulating Controlled-Channel Page Fault Side-Channel Attacks

**Overview**

This project demonstrates a controlled-channel side-channel attack in which secret information is inferred through memory page access patterns. By simulating secret-dependent execution behavior and observing which memory pages are accessed, the attacker reconstructs the secret without directly reading protected data. The experiment illustrates how low-level system interactions can create deterministic information leakage.

**Requirements**

Python 3.8 or higher
Linux (Ubuntu recommended)
Python libraries:
numpy
matplotlib

**Instructions to run Controlled-Channel**

1) Open Terminal
2) python3 --version
Make sure that you see Python 3.8+

if not run...
sudo apt update
sudo apt install python3

3) pip install numpy matplotlib
4) chmod +x controlled_channel_demo.py
5) python3 controlled_channel_demo.py
If you want to choose your own secret follow the format below (replace HI)
7) python3 controlled_channel_demo.py --secret HI
8) page_trace.png
View it --> xdg-open page_trace.png

**In the case something fails**

Error: matplotlib not found
do this!
pip install matplotlib

Error: numpy not found
do this!
pip install numpy

Python command not found
do this!
sudo apt install python3
