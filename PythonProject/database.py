from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import DeclarativeBase  # Nouvel import
from sqlalchemy.exc import OperationalError
import os
from dotenv import load_dotenv
import urllib.parse

# Charger les variables d'environnement
load_dotenv()

# Définition de la classe Base
class Base(DeclarativeBase):
    pass

# Récupérer les informations sensibles depuis les variables d'environnement
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = urllib.parse.quote_plus(str(os.getenv("DB_PASSWORD", ""))) if os.getenv("DB_PASSWORD") else ""
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "quizApp")

# Construction de l'URL de la base de données avec échappement des caractères spéciaux
DATABASE_URL = "postgresql://{0}:{1}@{2}:{3}/{4}".format(
    DB_USER,
    DB_PASSWORD,
    DB_HOST,
    DB_PORT,
    DB_NAME
)

# Configuration du moteur avec des paramètres de connexion plus robustes
engine = create_engine(
    DATABASE_URL,
    pool_size=5,
    max_overflow=10,
    pool_timeout=30,
    pool_recycle=1800,
    echo=False,
    connect_args={"client_encoding": "utf8"}
)

# Configuration de la session
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Fonction pour obtenir une session de base de données
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Fonction pour tester la connexion
def test_connection():
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            result.scalar()
        print("Connexion à la base de données établie avec succès!")
        return True
    except OperationalError as e:
        print("Erreur de connexion à la base de données: {}".format(repr(e)))
        return False

# Test de la connexion au démarrage
if __name__ == "__main__":
    test_connection()