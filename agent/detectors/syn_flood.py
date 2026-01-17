"""
syn_flood.py
------------
Détecteur d'attaque SYN Flood.

Principe :
- Un même IP source envoie un grand nombre de paquets TCP SYN
- dans une fenêtre de temps courte
- vers une ou plusieurs destinations
"""

import time
from collections import defaultdict, deque


class SynFloodDetector:
    def __init__(self, time_window=5, syn_threshold=50):
        """
        :param time_window: durée (en secondes) de la fenêtre d'observation
        :param syn_threshold: nombre de SYN pour déclencher l'alerte
        """
        self.time_window = time_window
        self.syn_threshold = syn_threshold

        # Structure :
        # {
        #   "192.168.1.50": deque([timestamp, timestamp, ...])
        # }
        self.syn_activity = defaultdict(deque)

    def analyze_packet(self, packet):
        """
        Analyse un paquet Scapy.
        Retourne une alerte (dict) ou None.
        """
        from scapy.layers.inet import IP, TCP

        # On ne s'intéresse qu'aux paquets TCP SYN
        if not packet.haslayer(IP) or not packet.haslayer(TCP):
            return None

        tcp_layer = packet[TCP]
        ip_layer = packet[IP]

        # SYN seul (pas ACK)
        if tcp_layer.flags != "S":
            return None

        src_ip = ip_layer.src
        now = time.time()

        # Enregistrer le SYN
        self.syn_activity[src_ip].append(now)

        # Nettoyage des anciennes entrées
        while (
            self.syn_activity[src_ip]
            and now - self.syn_activity[src_ip][0] > self.time_window
        ):
            self.syn_activity[src_ip].popleft()

        # Détection
        syn_count = len(self.syn_activity[src_ip])

        if syn_count >= self.syn_threshold:
            alert = {
                "type": "SYN_FLOOD",
                "source_ip": src_ip,
                "syn_count": syn_count,
                "time_window": self.time_window,
                "timestamp": now,
            }

            # Réinitialiser pour éviter les alertes en boucle
            self.syn_activity[src_ip].clear()

            return alert

        return None
