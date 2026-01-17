"""
test_port_scan_local.py
-----------------------
Test local du détecteur de Port Scan.

Objectif :
- Simuler un scan de ports TCP SYN
- Vérifier que le détecteur déclenche une alerte
"""

import time
from scapy.all import IP, TCP

# Import du détecteur
from agent.detectors.port_scan import PortScanDetector


def main():
    print("🧪 Test Port Scan Detector")

    # Initialiser le détecteur
    detector = PortScanDetector(
        time_window=5,      # secondes
        port_threshold=5    # ports distincts
    )

    src_ip = "192.168.1.100"
    dst_ip = "192.168.1.1"

    # Ports simulant un scan
    ports_to_scan = [22, 23, 80, 443, 8080]

    for port in ports_to_scan:
        print(f"➡️  Envoi SYN vers le port {port}")

        packet = IP(src=src_ip, dst=dst_ip) / TCP(
            dport=port,
            flags="S"
        )

        alert = detector.analyze_packet(packet)

        if alert:
            print("\n🚨 ALERTE DÉTECTÉE 🚨")
            print(alert)
            break

        time.sleep(0.5)

    print("\n✅ Test terminé")


if __name__ == "__main__":
    main()
