from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import func
from datetime import datetime, timedelta
import os

from server.database import engine, SessionLocal, Base
from server.models import Agent, Alert, Statistics, TrafficData
from server.routers import agents, traffic, alerts

# Créer les tables si elles n'existent pas
Base.metadata.create_all(bind=engine)

# Initialiser FastAPI
app = FastAPI(
    title="NetGuard Pro API",
    description="API de supervision et détection d'intrusions réseau",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Monter les fichiers statiques (si le dossier existe)
if os.path.exists("server/static"):
    app.mount("/static", StaticFiles(directory="server/static"), name="static")

# Templates Jinja2 (si le dossier existe)
if os.path.exists("server/templates"):
    templates = Jinja2Templates(directory="server/templates")
else:
    templates = None

# Inclure les routers
app.include_router(agents.router, prefix="/api/agents", tags=["Agents"])
app.include_router(traffic.router, prefix="/api/traffic", tags=["Traffic"])
app.include_router(alerts.router, prefix="/api/alerts", tags=["Alerts"])


@app.on_event("startup")
async def startup_event():
    """
    Événement de démarrage - initialisation des services
    """
    print("=" * 60)
    print("🚀 NetGuard Pro - Serveur Central FastAPI")
    print("=" * 60)
    print("📡 API REST: http://localhost:8000")
    print("📚 Documentation: http://localhost:8000/api/docs")
    print("🔍 ReDoc: http://localhost:8000/api/redoc")
    print("=" * 60)


@app.on_event("shutdown")
async def shutdown_event():
    """
    Événement d'arrêt propre
    """
    print("\n🛑 Arrêt du serveur NetGuard Pro...")


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    """
    Page d'accueil avec dashboard simple
    """
    if templates:
        return templates.TemplateResponse("dashboard.html", {"request": request})
    
    # Dashboard HTML simple si pas de template
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>NetGuard Pro - Dashboard</title>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: #333;
                min-height: 100vh;
                padding: 20px;
            }
            .container {
                max-width: 1200px;
                margin: 0 auto;
            }
            .header {
                background: white;
                padding: 30px;
                border-radius: 10px;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                margin-bottom: 20px;
            }
            h1 {
                color: #667eea;
                margin-bottom: 10px;
            }
            .card {
                background: white;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                margin-bottom: 20px;
            }
            .links {
                display: flex;
                gap: 15px;
                flex-wrap: wrap;
            }
            .link-btn {
                display: inline-block;
                padding: 12px 24px;
                background: #667eea;
                color: white;
                text-decoration: none;
                border-radius: 5px;
                transition: background 0.3s;
            }
            .link-btn:hover {
                background: #5568d3;
            }
            .status {
                display: inline-block;
                padding: 5px 15px;
                background: #10b981;
                color: white;
                border-radius: 20px;
                font-size: 14px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🛡️ NetGuard Pro</h1>
                <p>Plateforme Distribuée de Supervision et Détection d'Intrusions</p>
                <p><span class="status">🟢 Système Opérationnel</span></p>
            </div>
            
            <div class="card">
                <h2>📚 Documentation API</h2>
                <p style="margin: 15px 0;">Accédez à la documentation interactive de l'API :</p>
                <div class="links">
                    <a href="/api/docs" class="link-btn">📖 Swagger UI</a>
                    <a href="/api/redoc" class="link-btn">📘 ReDoc</a>
                </div>
            </div>
            
            <div class="card">
                <h2>🔗 Endpoints Principaux</h2>
                <ul style="margin-top: 15px; line-height: 1.8;">
                    <li>🤖 <strong>Agents:</strong> <code>/api/agents</code></li>
                    <li>📊 <strong>Trafic:</strong> <code>/api/traffic</code></li>
                    <li>🚨 <strong>Alertes:</strong> <code>/api/alerts</code></li>
                    <li>📈 <strong>Métriques:</strong> <code>/api/dashboard/metrics</code></li>
                    <li>💚 <strong>Health:</strong> <code>/api/health</code></li>
                </ul>
            </div>
        </div>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)


@app.get("/api/health")
async def health_check():
    """
    Vérification de santé du serveur
    """
    db = SessionLocal()
    try:
        # Test de connexion DB
        db.execute("SELECT 1")
        db_status = "connected"
    except Exception as e:
        db_status = f"error: {str(e)}"
    finally:
        db.close()
    
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "database": db_status,
        "version": "1.0.0"
    }


@app.get("/api/dashboard/metrics")
async def get_dashboard_metrics():
    """
    Métriques en temps réel pour le dashboard
    """
    db = SessionLocal()
    
    try:
        # Agents actifs (heartbeat dans les 5 dernières minutes)
        active_agents = db.query(Agent).filter(
            Agent.status == 'active',
            Agent.last_heartbeat > datetime.now() - timedelta(minutes=5)
        ).count()
        
        # Total agents
        total_agents = db.query(Agent).count()
        
        # Alertes dernières 24h
        alerts_24h = db.query(Alert).filter(
            Alert.timestamp > datetime.now() - timedelta(hours=24)
        ).count()
        
        # Alertes non résolues
        unresolved_alerts = db.query(Alert).filter(
            Alert.resolved == False
        ).count()
        
        # Alertes critiques non résolues
        critical_alerts = db.query(Alert).filter(
            Alert.resolved == False,
            Alert.severity == 'CRITICAL'
        ).count()
        
        # Paquets dernières 24h
        total_packets_24h = db.query(TrafficData).filter(
            TrafficData.timestamp > datetime.now() - timedelta(hours=24)
        ).count()
        
        # Statistiques récentes
        recent_stats = db.query(Statistics).order_by(
            Statistics.timestamp.desc()
        ).first()
        
        return {
            "agents": {
                "active": active_agents,
                "total": total_agents,
                "inactive": total_agents - active_agents
            },
            "alerts": {
                "last_24h": alerts_24h,
                "unresolved": unresolved_alerts,
                "critical": critical_alerts
            },
            "traffic": {
                "packets_24h": total_packets_24h,
                "packets_per_second": recent_stats.avg_packets_per_second if recent_stats else 0
            },
            "timestamp": datetime.now().isoformat()
        }
    
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"Erreur lors de la récupération des métriques: {str(e)}"}
        )
    finally:
        db.close()


# Point d'entrée pour exécution directe
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "server.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # Auto-reload en développement
        log_level="info"
    )