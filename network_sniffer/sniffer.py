import threading
from scapy.all import sniff
from utils import parse_packet

class PacketSniffer:
    def __init__(self, callback, iface="your_interface", protocol_filter=None):
        self.callback = callback
        self.running = False
        self.iface = iface
        self.thread = None
        self.protocol_filter = protocol_filter

    def _sniff_packets(self):
        sniff(
            iface=self.iface,
            prn=self._handle_packet,
            stop_filter=lambda pkt: not self.running,
            store=False
        )

    def _handle_packet(self, pkt):
        info = parse_packet(pkt, self.protocol_filter)
        if info:
            self.callback(info)

    def start_sniffing(self):
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self._sniff_packets, daemon=True)
            self.thread.start()
            print(f"✅ Sniffing Started on: {self.iface}")

    def stop_sniffing(self):
        self.running = False
        print("🛑 Sniffing Stopped")
