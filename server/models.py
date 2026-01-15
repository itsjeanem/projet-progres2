from sqlalchemy import Column, Integer, String, DateTime, Float, Text, Boolean
from datetime import datetime
from server.database import Base


class Agent(Base):
    """Modèle pour les agents de supervision"""
    __tablename__ = 'agents'
    
    id = Column(Integer, primary_key=True, index=True)
    agent_id = Column(String(50), unique=True, nullable=False, index=True)
    hostname = Column(String(100))
    ip_address = Column(String(45))
    status = Column(String(20), default='active')  # active, inactive, error
    last_heartbeat = Column(DateTime, default=datetime.now)
    created_at = Column(DateTime, default=datetime.now)
    
    def to_dict(self):
        """Convertir en dictionnaire"""
        return {
            'id': self.id,
            'agent_id': self.agent_id,
            'hostname': self.hostname,
            'ip_address': self.ip_address,
            'status': self.status,
            'last_heartbeat': self.last_heartbeat.isoformat() if self.last_heartbeat else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class TrafficData(Base):
    """Modèle pour les données de trafic réseau"""
    __tablename__ = 'traffic_data'
    
    id = Column(Integer, primary_key=True, index=True)
    agent_id = Column(String(50), index=True)
    timestamp = Column(DateTime, default=datetime.now, index=True)
    source_ip = Column(String(45))
    dest_ip = Column(String(45))
    protocol = Column(String(20))
    port = Column(Integer)
    packet_size = Column(Integer)
    flags = Column(String(20))
    
    def to_dict(self):
        """Convertir en dictionnaire"""
        return {
            'id': self.id,
            'agent_id': self.agent_id,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None,
            'source_ip': self.source_ip,
            'dest_ip': self.dest_ip,
            'protocol': self.protocol,
            'port': self.port,
            'packet_size': self.packet_size,
            'flags': self.flags
        }


class Alert(Base):
    """Modèle pour les alertes de sécurité"""
    __tablename__ = 'alerts'
    
    id = Column(Integer, primary_key=True, index=True)
    alert_type = Column(String(50), index=True)  # PORT_SCAN, SYN_FLOOD, etc.
    severity = Column(String(20))  # LOW, MEDIUM, HIGH, CRITICAL
    source_ip = Column(String(45))
    target_ip = Column(String(45))
    description = Column(Text)
    details = Column(Text)  # JSON avec détails techniques
    timestamp = Column(DateTime, default=datetime.now, index=True)
    acknowledged = Column(Boolean, default=False)
    resolved = Column(Boolean, default=False)
    
    def to_dict(self):
        """Convertir en dictionnaire"""
        return {
            'id': self.id,
            'alert_type': self.alert_type,
            'severity': self.severity,
            'source_ip': self.source_ip,
            'target_ip': self.target_ip,
            'description': self.description,
            'details': self.details,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None,
            'acknowledged': self.acknowledged,
            'resolved': self.resolved
        }


class Statistics(Base):
    """Modèle pour les statistiques système"""
    __tablename__ = 'statistics'
    
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.now, index=True)
    total_packets = Column(Integer, default=0)
    total_alerts = Column(Integer, default=0)
    active_agents = Column(Integer, default=0)
    avg_packets_per_second = Column(Float, default=0.0)
    
    def to_dict(self):
        """Convertir en dictionnaire"""
        return {
            'id': self.id,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None,
            'total_packets': self.total_packets,
            'total_alerts': self.total_alerts,
            'active_agents': self.active_agents,
            'avg_packets_per_second': self.avg_packets_per_second
        }