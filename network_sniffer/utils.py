from scapy.all import IP, TCP, UDP, ICMP
from datetime import datetime

def parse_packet(pkt, protocol_filter=None):
    proto = "Other"

    if IP in pkt:
        if TCP in pkt:
            proto = "TCP"
        elif UDP in pkt:
            proto = "UDP"
        elif ICMP in pkt:
            proto = "ICMP"

    # Filter Uygulaması
    if protocol_filter and proto not in protocol_filter:
        return None

    time = datetime.now().strftime("%H:%M:%S")
    src = pkt[IP].src if IP in pkt else "Unknown"
    dst = pkt[IP].dst if IP in pkt else "Unknown"
    length = len(pkt)

    return [time, src, dst, proto, length]
