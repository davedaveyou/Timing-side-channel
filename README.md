# Simulating Controlled-Channel Page Fault Side-Channel Attacks

Overview

This project demonstrates a controlled-channel side-channel attack in which secret information is inferred through memory page access patterns. By simulating secret-dependent execution behavior and observing which memory pages are accessed, the attacker reconstructs the secret without directly reading protected data. The experiment illustrates how low-level system interactions can create deterministic information leakage.

Requirements

Python 3.8 or higher
Linux (Ubuntu recommended)
Python libraries:
numpy
matplotlib

Setup Instructions

Clone the repository and install dependencies:

pip install -r requirements.txt

If using a virtual environment:

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

Run the attack simulation using:

python3 controlled_channel_demo.py --secret HI

Example (slower execution for visualization):

python3 controlled_channel_demo.py --secret KEY --delay 0.4

Expected output includes:

Observed memory page access sequence

Reconstructed secret bits

Recovered plaintext secret

Visualization of page access trace (saved as page_trace.png)
