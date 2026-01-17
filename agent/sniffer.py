"""
sniffer.py
-----------
Capture de paquets réseau avec Scapy.
Étape 1 du projet NetGuard Pro.

Rôle :
- Écouter une interface réseau
- Capturer les paquets IP
- Afficher des informations simples (debug / validation)
"""

from scapy.all import sniff, IP, TCP, UDP
from datetime import datetime
import os


def packet_callback(packet):
    """
    Fonction appelée pour chaque paquet capturé
    """
    if IP in packet:
        timestamp = datetime.now().strftime("%H:%M:%S")

        src_ip = packet[IP].src
        dst_ip = packet[IP].dst
        proto = packet[IP].proto

        proto_name = "OTHER"
        if TCP in packet:
            proto_name = "TCP"
        elif UDP in packet:
            proto_name = "UDP"

        print(f"[{timestamp}] {src_ip} -> {dst_ip} | {proto_name}")


def start_sniffing(interface):
    """
    Démarre la capture réseau sur l’interface donnée
    """
    print("=" * 60)
    print("🕵️  NetGuard Pro — Sniffer réseau")
    print(f"📡 Interface utilisée : {interface}")
    print("⏳ Capture en cours... (Ctrl+C pour arrêter)")
    print("=" * 60)

    try:
        sniff(
            iface=interface,
            prn=packet_callback,
            store=False
        )
    except PermissionError:
        print("❌ Permission refusée.")
        print("👉 Lance VS Code / PowerShell en ADMINISTRATEUR.")
    except Exception as e:
        print(f"❌ Erreur pendant la capture : {e}")


if __name__ == "__main__":
    """
    Point d’entrée du script
    """

    # 🔴 Interface réseau
    # Priorité :
    # 1. Variable d’environnement INTERFACE
    # 2. Valeur par défaut (VMware VMnet8)

    INTERFACE = os.getenv(
        "INTERFACE",
        r"\Device\NPF_{54F162C9-8C24-4D2A-BD95-FD730014ED35}"  # VMnet8 (exemple)
    )

    start_sniffing(INTERFACE)
