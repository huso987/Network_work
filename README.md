# Network Work
![image](https://github.com/user-attachments/assets/504ec568-caf4-4061-8fd5-c0daef64ea9e)



## firewall.py 

This project implements an advanced firewall using Python and the Scapy library. The firewall monitors incoming and outgoing network traffic, blocking or allowing packets based on predefined rules, such as IP addresses, port numbers, and packet size.

### Features
- IP-based traffic filtering.
- Port-based traffic filtering (TCP and UDP).
- Block oversized packets.
- Real-time logging of allowed and blocked packets.

### Prerequisites
- Python 3.x
- Scapy Library
- Linux (for iptables functionality)

### Install Scapy
To install the Scapy library, run:

pip install scapy

### Usage

sudo python3 firewall.py

----------------------------------------------------------------------------------------------
## ospfrouter.py 

This project sets up a dynamic routing network topology using Mininet and Quagga routing software. It demonstrates the configuration of routers with OSPF (Open Shortest Path First) protocol, allowing dynamic routing across a three-router network.

By implementing dynamic routing, the project showcases optimized network traffic flow and the flexibility of using routing protocols to adjust to network changes in real-time.

### Prerequisites
- Mininet (recommended OS: Ubuntu)
- Quagga
- Python 3.x

