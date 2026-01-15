from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List
from datetime import datetime

from server.database import get_db
from server.models import Agent

router = APIRouter()


# Schémas Pydantic
class AgentRegister(BaseModel):
    agent_id: str
    hostname: str
    ip_address: str


class AgentResponse(BaseModel):
    id: int
    agent_id: str
    hostname: str
    ip_address: str
    status: str
    last_heartbeat: str
    created_at: str

    class Config:
        from_attributes = True


@router.post("/register", response_model=AgentResponse, status_code=201)
async def register_agent(agent_data: AgentRegister, db: Session = Depends(get_db)):
    """
    Enregistre un nouvel agent de supervision
    """
    # Vérifier si l'agent existe déjà
    existing_agent = db.query(Agent).filter(Agent.agent_id == agent_data.agent_id).first()
    
    if existing_agent:
        # Mettre à jour l'agent existant
        existing_agent.hostname = agent_data.hostname
        existing_agent.ip_address = agent_data.ip_address
        existing_agent.status = 'active'
        existing_agent.last_heartbeat = datetime.now()
        db.commit()
        db.refresh(existing_agent)
        return existing_agent.to_dict()
    
    # Créer un nouvel agent
    new_agent = Agent(
        agent_id=agent_data.agent_id,
        hostname=agent_data.hostname,
        ip_address=agent_data.ip_address,
        status='active'
    )
    
    db.add(new_agent)
    db.commit()
    db.refresh(new_agent)
    
    return new_agent.to_dict()


@router.get("", response_model=List[AgentResponse])
async def list_agents(db: Session = Depends(get_db)):
    """
    Liste tous les agents enregistrés
    """
    agents = db.query(Agent).all()
    return [agent.to_dict() for agent in agents]


@router.get("/{agent_id}/status")
async def get_agent_status(agent_id: str, db: Session = Depends(get_db)):
    """
    Récupère le statut d'un agent spécifique
    """
    agent = db.query(Agent).filter(Agent.agent_id == agent_id).first()
    
    if not agent:
        raise HTTPException(status_code=404, detail="Agent non trouvé")
    
    # Calculer le temps depuis le dernier heartbeat
    time_since_heartbeat = (datetime.now() - agent.last_heartbeat).total_seconds()
    is_online = time_since_heartbeat < 300  # 5 minutes
    
    return {
        **agent.to_dict(),
        'is_online': is_online,
        'seconds_since_heartbeat': int(time_since_heartbeat)
    }


@router.put("/{agent_id}/heartbeat")
async def update_heartbeat(agent_id: str, db: Session = Depends(get_db)):
    """
    Met à jour le heartbeat d'un agent
    """
    agent = db.query(Agent).filter(Agent.agent_id == agent_id).first()
    
    if not agent:
        raise HTTPException(status_code=404, detail="Agent non trouvé")
    
    agent.last_heartbeat = datetime.now()
    agent.status = 'active'
    db.commit()
    
    return {"message": "Heartbeat mis à jour", "timestamp": agent.last_heartbeat.isoformat()}


@router.delete("/{agent_id}")
async def delete_agent(agent_id: str, db: Session = Depends(get_db)):
    """
    Supprime un agent
    """
    agent = db.query(Agent).filter(Agent.agent_id == agent_id).first()
    
    if not agent:
        raise HTTPException(status_code=404, detail="Agent non trouvé")
    
    db.delete(agent)
    db.commit()
    
    return {"message": f"Agent {agent_id} supprimé avec succès"}