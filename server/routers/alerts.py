from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc, func
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime, timedelta

from server.database import get_db
from server.models import Alert

router = APIRouter()


# Schémas Pydantic
class AlertCreate(BaseModel):
    alert_type: str
    severity: str
    source_ip: str
    target_ip: Optional[str] = None
    description: str
    details: Optional[str] = None


class AlertResponse(BaseModel):
    id: int
    alert_type: str
    severity: str
    source_ip: str
    target_ip: Optional[str]
    description: str
    details: Optional[str]
    timestamp: str
    acknowledged: bool
    resolved: bool

    class Config:
        from_attributes = True


@router.post("", response_model=AlertResponse, status_code=201)
async def create_alert(alert: AlertCreate, db: Session = Depends(get_db)):
    """
    Crée une nouvelle alerte
    """
    new_alert = Alert(
        alert_type=alert.alert_type,
        severity=alert.severity,
        source_ip=alert.source_ip,
        target_ip=alert.target_ip,
        description=alert.description,
        details=alert.details
    )
    
    db.add(new_alert)
    db.commit()
    db.refresh(new_alert)
    
    return new_alert.to_dict()


@router.get("", response_model=List[AlertResponse])
async def list_alerts(
    limit: int = Query(default=50, ge=1, le=500),
    severity: Optional[str] = None,
    resolved: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    """
    Liste les alertes avec filtres optionnels
    """
    query = db.query(Alert)
    
    if severity:
        query = query.filter(Alert.severity == severity.upper())
    
    if resolved is not None:
        query = query.filter(Alert.resolved == resolved)
    
    alerts = query.order_by(desc(Alert.timestamp)).limit(limit).all()
    
    return [alert.to_dict() for alert in alerts]


@router.get("/{alert_id}", response_model=AlertResponse)
async def get_alert(alert_id: int, db: Session = Depends(get_db)):
    """
    Récupère les détails d'une alerte spécifique
    """
    alert = db.query(Alert).filter(Alert.id == alert_id).first()
    
    if not alert:
        raise HTTPException(status_code=404, detail="Alerte non trouvée")
    
    return alert.to_dict()


@router.post("/{alert_id}/acknowledge")
async def acknowledge_alert(alert_id: int, db: Session = Depends(get_db)):
    """
    Accuse réception d'une alerte
    """
    alert = db.query(Alert).filter(Alert.id == alert_id).first()
    
    if not alert:
        raise HTTPException(status_code=404, detail="Alerte non trouvée")
    
    alert.acknowledged = True
    db.commit()
    
    return {"message": "Alerte accusée réception", "alert_id": alert_id}


@router.post("/{alert_id}/resolve")
async def resolve_alert(alert_id: int, db: Session = Depends(get_db)):
    """
    Marque une alerte comme résolue
    """
    alert = db.query(Alert).filter(Alert.id == alert_id).first()
    
    if not alert:
        raise HTTPException(status_code=404, detail="Alerte non trouvée")
    
    alert.resolved = True
    alert.acknowledged = True
    db.commit()
    
    return {"message": "Alerte résolue", "alert_id": alert_id}


@router.get("/stats/summary")
async def get_alerts_summary(
    hours: int = Query(default=24, ge=1, le=168),
    db: Session = Depends(get_db)
):
    """
    Résumé des alertes sur une période
    """
    time_threshold = datetime.now() - timedelta(hours=hours)
    
    # Total des alertes
    total_alerts = db.query(func.count(Alert.id)).filter(
        Alert.timestamp >= time_threshold
    ).scalar()
    
    # Alertes par sévérité
    by_severity = db.query(
        Alert.severity,
        func.count(Alert.id).label('count')
    ).filter(
        Alert.timestamp >= time_threshold
    ).group_by(Alert.severity).all()
    
    # Alertes par type
    by_type = db.query(
        Alert.alert_type,
        func.count(Alert.id).label('count')
    ).filter(
        Alert.timestamp >= time_threshold
    ).group_by(Alert.alert_type).all()
    
    # Alertes non résolues
    unresolved = db.query(func.count(Alert.id)).filter(
        Alert.resolved == False,
        Alert.timestamp >= time_threshold
    ).scalar()
    
    # IPs sources les plus problématiques
    top_sources = db.query(
        Alert.source_ip,
        func.count(Alert.id).label('count')
    ).filter(
        Alert.timestamp >= time_threshold
    ).group_by(Alert.source_ip).order_by(desc('count')).limit(10).all()
    
    return {
        "period_hours": hours,
        "total_alerts": total_alerts,
        "unresolved_alerts": unresolved,
        "by_severity": {s: c for s, c in by_severity},
        "by_type": {t: c for t, c in by_type},
        "top_source_ips": [{"ip": ip, "count": c} for ip, c in top_sources]
    }


@router.delete("/{alert_id}")
async def delete_alert(alert_id: int, db: Session = Depends(get_db)):
    """
    Supprime une alerte (admin seulement)
    """
    alert = db.query(Alert).filter(Alert.id == alert_id).first()
    
    if not alert:
        raise HTTPException(status_code=404, detail="Alerte non trouvée")
    
    db.delete(alert)
    db.commit()
    
    return {"message": f"Alerte {alert_id} supprimée"}