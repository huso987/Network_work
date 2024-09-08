from scapy.all import *
import logging

# Log dosyası ayarları
logging.basicConfig(filename="advanced_firewall_log.txt", level=logging.INFO, format='%(asctime)s - %(message)s')

# Firewall kuralları
ALLOWED_IPS = ["192.168.1.100"]  # İzin verilen IP adresleri
BLOCKED_IPS = ["192.168.1.200"]  # Engellenen IP adresleri
ALLOWED_PORTS = [80, 443]  # İzin verilen portlar (HTTP, HTTPS)
BLOCKED_PORTS = [22, 23]  # Engellenen portlar (SSH, Telnet)
MAX_PACKET_SIZE = 1500  # Maksimum izin verilen paket boyutu (bytes)

def packet_callback(packet):
    # IP adres kontrolü
    if IP in packet:
        src_ip = packet[IP].src
        dst_ip = packet[IP].dst

        # IP adresi engellenmiş mi?
        if src_ip in BLOCKED_IPS or dst_ip in BLOCKED_IPS:
            logging.info(f"Blocked IP packet from {src_ip} to {dst_ip}")
            return

        # Paket boyutu ayarlama
        if len(packet) > MAX_PACKET_SIZE:
            logging.info(f"Blocked oversized packet from {src_ip} to {dst_ip} - Size: {len(packet)}")
            return

        # TCP veya UDP paketleri için port kontrolü
        if TCP in packet or UDP in packet:
            sport = packet[TCP].sport if TCP in packet else packet[UDP].sport
            dport = packet[TCP].dport if TCP in packet else packet[UDP].dport

            if sport in BLOCKED_PORTS or dport in BLOCKED_PORTS:
                logging.info(f"Blocked packet from {src_ip}:{sport} to {dst_ip}:{dport} (Blocked Port)")
                return

            if sport not in ALLOWED_PORTS and dport not in ALLOWED_PORTS:
                logging.info(f"Blocked packet from {src_ip}:{sport} to {dst_ip}:{dport} (Not Allowed Port)")
                return

        # İzin verilen paket
        logging.info(f"Allowed packet from {src_ip} to {dst_ip}")

# Ağ trafiğini dinle
print("[*] Advanced Firewall is running...")
sniff(prn=packet_callback, store=0)
