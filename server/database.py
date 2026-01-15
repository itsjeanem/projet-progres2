import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# URL de connexion à la base de données
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:0987654321@localhost:5432/netguard"
)

# Créer le moteur SQLAlchemy
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,  # Vérifier la connexion avant utilisation
    pool_size=10,        # Taille du pool de connexions
    max_overflow=20      # Connexions supplémentaires max
)

# Session locale
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base pour les modèles
Base = declarative_base()


def get_db():
    """
    Dependency pour obtenir une session de base de données
    Utilisé dans les endpoints FastAPI
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """
    Initialise la base de données (crée toutes les tables)
    """
    
    print("🔨 Création des tables dans la base de données...")
    Base.metadata.create_all(bind=engine)
    print("✅ Tables créées avec succès!")


if __name__ == "__main__":
    # Permet d'initialiser la DB via: python -m server.database init
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "init":
        init_db()
    else:
        print("Usage: python -m server.database init")