from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime, timedelta

from server.database import get_db
from server.models import TrafficData

router = APIRouter()


# Schémas Pydantic
class TrafficSubmit(BaseModel):
    agent_id: str
    source_ip: str
    dest_ip: str
    protocol: str
    port: int
    packet_size: int
    flags: Optional[str] = None


class TrafficResponse(BaseModel):
    id: int
    agent_id: str
    timestamp: str
    source_ip: str
    dest_ip: str
    protocol: str
    port: int
    packet_size: int
    flags: Optional[str]

    class Config:
        from_attributes = True


@router.post("/submit", status_code=201)
async def submit_traffic_data(traffic: TrafficSubmit, db: Session = Depends(get_db)):
    """
    Soumet des données de trafic capturées par un agent
    """
    traffic_entry = TrafficData(
        agent_id=traffic.agent_id,
        source_ip=traffic.source_ip,
        dest_ip=traffic.dest_ip,
        protocol=traffic.protocol,
        port=traffic.port,
        packet_size=traffic.packet_size,
        flags=traffic.flags
    )
    
    db.add(traffic_entry)
    db.commit()
    db.refresh(traffic_entry)
    
    return {"message": "Données de trafic enregistrées", "id": traffic_entry.id}


@router.post("/submit/batch", status_code=201)
async def submit_traffic_batch(traffic_list: List[TrafficSubmit], db: Session = Depends(get_db)):
    """
    Soumet un lot de données de trafic (plus efficace)
    """
    traffic_entries = [
        TrafficData(
            agent_id=traffic.agent_id,
            source_ip=traffic.source_ip,
            dest_ip=traffic.dest_ip,
            protocol=traffic.protocol,
            port=traffic.port,
            packet_size=traffic.packet_size,
            flags=traffic.flags
        )
        for traffic in traffic_list
    ]
    
    db.bulk_save_objects(traffic_entries)
    db.commit()
    
    return {
        "message": f"{len(traffic_list)} entrées de trafic enregistrées",
        "count": len(traffic_list)
    }


@router.get("/stats")
async def get_traffic_stats(
    hours: int = Query(default=24, ge=1, le=168),
    db: Session = Depends(get_db)
):
    """
    Statistiques du trafic sur une période donnée
    """
    time_threshold = datetime.now() - timedelta(hours=hours)
    
    # Statistiques générales
    total_packets = db.query(func.count(TrafficData.id)).filter(
        TrafficData.timestamp >= time_threshold
    ).scalar()
    
    # Protocoles les plus utilisés
    protocol_stats = db.query(
        TrafficData.protocol,
        func.count(TrafficData.id).label('count')
    ).filter(
        TrafficData.timestamp >= time_threshold
    ).group_by(TrafficData.protocol).all()
    
    # Ports les plus scannés
    port_stats = db.query(
        TrafficData.port,
        func.count(TrafficData.id).label('count')
    ).filter(
        TrafficData.timestamp >= time_threshold
    ).group_by(TrafficData.port).order_by(desc('count')).limit(10).all()
    
    # IPs sources les plus actives
    source_ip_stats = db.query(
        TrafficData.source_ip,
        func.count(TrafficData.id).label('count')
    ).filter(
        TrafficData.timestamp >= time_threshold
    ).group_by(TrafficData.source_ip).order_by(desc('count')).limit(10).all()
    
    return {
        "period_hours": hours,
        "total_packets": total_packets,
        "protocols": [{"protocol": p, "count": c} for p, c in protocol_stats],
        "top_ports": [{"port": p, "count": c} for p, c in port_stats],
        "top_source_ips": [{"ip": ip, "count": c} for ip, c in source_ip_stats]
    }


@router.get("/recent", response_model=List[TrafficResponse])
async def get_recent_traffic(
    limit: int = Query(default=100, ge=1, le=1000),
    agent_id: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Récupère les données de trafic récentes
    """
    query = db.query(TrafficData)
    
    if agent_id:
        query = query.filter(TrafficData.agent_id == agent_id)
    
    traffic = query.order_by(desc(TrafficData.timestamp)).limit(limit).all()
    
    return [t.to_dict() for t in traffic]


@router.get("/by-ip/{ip_address}")
async def get_traffic_by_ip(
    ip_address: str,
    hours: int = Query(default=24, ge=1, le=168),
    db: Session = Depends(get_db)
):
    """
    Récupère le trafic associé à une IP spécifique
    """
    time_threshold = datetime.now() - timedelta(hours=hours)
    
    # Trafic où l'IP est source
    as_source = db.query(TrafficData).filter(
        TrafficData.source_ip == ip_address,
        TrafficData.timestamp >= time_threshold
    ).count()
    
    # Trafic où l'IP est destination
    as_dest = db.query(TrafficData).filter(
        TrafficData.dest_ip == ip_address,
        TrafficData.timestamp >= time_threshold
    ).count()
    
    # Ports contactés
    ports_contacted = db.query(
        TrafficData.port,
        func.count(TrafficData.id).label('count')
    ).filter(
        TrafficData.source_ip == ip_address,
        TrafficData.timestamp >= time_threshold
    ).group_by(TrafficData.port).all()
    
    return {
        "ip_address": ip_address,
        "period_hours": hours,
        "packets_as_source": as_source,
        "packets_as_destination": as_dest,
        "total_packets": as_source + as_dest,
        "ports_contacted": [{"port": p, "count": c} for p, c in ports_contacted]
    }