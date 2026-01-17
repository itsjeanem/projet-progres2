"""
port_scan.py
------------
Détecteur de Port Scan (TCP SYN).

Principe :
- Un même IP source tente de contacter
  plusieurs ports différents
- dans une courte fenêtre de temps
"""

import time
from collections import defaultdict, deque


class PortScanDetector:
    def __init__(self, time_window=10, port_threshold=10):
        """
        :param time_window: durée (en secondes) de la fenêtre d'observation
        :param port_threshold: nombre de ports distincts pour déclencher l'alerte
        """
        self.time_window = time_window
        self.port_threshold = port_threshold

        # Structure :
        # {
        #   "192.168.1.50": deque([(timestamp, port), ...])
        # }
        self.activity = defaultdict(deque)

    def analyze_packet(self, packet):
        """
        Analyse un paquet Scapy.
        Retourne une alerte (dict) ou None.
        """
        # Import ici pour éviter les dépendances inutiles au chargement
        from scapy.layers.inet import IP, TCP

        # On ne s'intéresse qu'aux paquets TCP SYN
        if not packet.haslayer(IP) or not packet.haslayer(TCP):
            return None

        tcp_layer = packet[TCP]
        ip_layer = packet[IP]

        # SYN = début de connexion TCP
        if tcp_layer.flags != "S":
            return None

        src_ip = ip_layer.src
        dst_port = tcp_layer.dport
        now = time.time()

        # Enregistrer l'activité
        self.activity[src_ip].append((now, dst_port))

        # Nettoyage des anciennes entrées (hors fenêtre de temps)
        while self.activity[src_ip] and now - self.activity[src_ip][0][0] > self.time_window:
            self.activity[src_ip].popleft()

        # Ports distincts contactés
        ports_contacted = {port for _, port in self.activity[src_ip]}

        # Détection
        if len(ports_contacted) >= self.port_threshold:
            alert = {
                "type": "PORT_SCAN",
                "source_ip": src_ip,
                "ports": list(ports_contacted),
                "count": len(ports_contacted),
                "time_window": self.time_window,
                "timestamp": now
            }

            # Réinitialiser pour éviter les alertes en boucle
            self.activity[src_ip].clear()

            return alert

        return None
