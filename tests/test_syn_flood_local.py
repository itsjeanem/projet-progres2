"""
test_syn_flood_local.py
----------------------
Test local du détecteur SYN Flood.
"""

import time
from scapy.all import IP, TCP
from agent.detectors.syn_flood import SynFloodDetector


def main():
    print("🧪 Test SYN Flood Detector")

    detector = SynFloodDetector(
        time_window=3,     # secondes
        syn_threshold=20   # SYN
    )

    src_ip = "10.0.0.99"
    dst_ip = "10.0.0.1"

    # Simuler une rafale de SYN
    for i in range(25):
        packet = IP(src=src_ip, dst=dst_ip) / TCP(dport=80, flags="S")
        alert = detector.analyze_packet(packet)

        if alert:
            print("\n🚨 ALERTE DÉTECTÉE 🚨")
            print(alert)
            break

        time.sleep(0.05)  # rafale rapide

    print("\n✅ Test terminé")


if __name__ == "__main__":
    main()
