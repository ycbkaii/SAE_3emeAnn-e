from datetime import datetime, timedelta, timezone
import secrets
import jwt
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
import psycopg2
from pydantic import BaseModel
from sqlmodel import Session, select
from models import User, UserCreate
from models import Token
from typing import Annotated, Any
from deps import CurrentUser, SessionDep
from typing import List, Optional

import bcrypt
print(bcrypt.__version__)


# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = secrets.token_urlsafe(32)
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

user_router = APIRouter(prefix="/usr")


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/usr/token")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)


def get_db_connection():
    return psycopg2.connect(
        database="masterbook",
        port="5433",
        user="root",
        host="localhost",
        password="root"
    )


# Pydantic model pour l'utilisateur
class UserCreate(BaseModel):
    email: str
    password: str
    age: int
    id_selection: int  # Humeur
    id_vitesse_lecture: int  # Vitesse de lecture
    id_secteur: Optional[int] = None  # Secteur d'activité (optionnel)
    id_genre_sex: int  # Genre
    genres: List[int]  # Genres préférés (liste d'IDs de genres)
    book_criteria: List[int]  # Critères pour choisir un livre (liste d'IDs de critères)
    favorite_authors: List[int]  # Auteurs favoris (liste d'IDs d'auteurs)
    id_prefere_lire: int  # Préférence de lecture


@user_router.post("/register")
def register_user(user: UserCreate):
    """Créer un nouvel utilisateur avec un mot de passe haché"""
    print(user)
    
    hashed_password = get_password_hash(user.password)  # Hachage du mot de passe
    conn = get_db_connection()
    cur = conn.cursor()

    try:
        # Insertion de l'utilisateur dans la table _utilisateur
        query = """
            INSERT INTO masterbook._utilisateur 
            (email, passwd, age, id_genre_sex, id_secteur, id_prefere_lire, id_vitesse_lecture, id_selection)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id_user;
        """
        
        cur.execute(query, (
            user.email, 
            hashed_password, 
            user.age, 
            user.id_genre_sex, 
            user.id_secteur, 
            user.id_prefere_lire,  # Ajout de l'attribut 'id_prefere_lire'
            user.id_vitesse_lecture, 
            user.id_selection
        ))

        # Récupérer l'id de l'utilisateur
        user_id = cur.fetchone()[0]  # Récupère l'id généré
        conn.commit()

        # Insérer les genres favoris de l'utilisateur dans la table _genre_aime
        for genre_id in user.genres:
            query_genre = """
                INSERT INTO masterbook._genre_aime (id_user, id_genre)
                VALUES (%s, %s);
            """
            cur.execute(query_genre, (user_id, genre_id))
        
        # Insérer les critères de l'utilisateur dans la table _critere_de_utilisateur
        for criterion_id in user.book_criteria:
            query_criteria = """
                INSERT INTO masterbook._critere_de_utilisateur (id_user, id_critere)
                VALUES (%s, %s);
            """
            cur.execute(query_criteria, (user_id, criterion_id))
        
        # Insérer les auteurs favoris de l'utilisateur dans la table _aime_auteur
        for author_id in user.favorite_authors:
            query_author = """
                INSERT INTO masterbook._aime_auteur (id_user, id_auteur)
                VALUES (%s, %s);
            """
            cur.execute(query_author, (user_id, author_id))
        
        conn.commit()

        return {"message": "Utilisateur créé avec succès", "id_user": user_id}
    
    except psycopg2.Error as e:
        conn.rollback()  # Annule la transaction en cas d'erreur
        raise HTTPException(status_code=400, detail=f"Erreur SQL : {e.pgcode} - {e.pgerror}")
    
    finally:
        cur.close()
        conn.close()

@user_router.post("/login")
def login_user(form_data: OAuth2PasswordRequestForm = Depends()):
    """Connexion utilisateur et génération du token JWT"""
    
    conn = psycopg2.connect(database="masterbook",
                            port="5433",
                            user="admin",
                            host="localhost",
                            password="root")
    cur = conn.cursor()

    query = "SELECT id_user, passwd FROM masterbook._utilisateur WHERE email = %s"
    cur.execute(query, (form_data.username,))
    user = cur.fetchone()

    cur.close()
    conn.close()

    if not user:
        raise HTTPException(status_code=400, detail="Email incorrect")

    user_id, hashed_password = user

    if not verify_password(form_data.password, hashed_password):
        raise HTTPException(status_code=400, detail="Mot de passe incorrect")

    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(user_id, access_token_expires)

    return {"access_token": access_token, "token_type": "bearer"}


class Token(BaseModel):
    access_token: str
    token_type: str

def create_access_token(subject: str, expires_delta: timedelta):
    """Crée un token JWT"""
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode = {"exp": expire, "sub": str(subject)}  # <-- Convertit `sub` en string
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: str = Depends(oauth2_scheme)):
    """Décode le Token et retourne l'utilisateur connecté"""
    """Décode le Token et retourne l'utilisateur connecté"""
    print(f"🔎 Token extrait par OAuth2 : {token}")  # <-- Affiche le token reçu

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Identifiants invalides",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        print(f"🔍 Token reçu : {token}")  # <-- Vérifier le token reçu
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print(f"📌 Contenu du token décodé : {payload}")  # <-- Voir le contenu exact

        user_id = payload.get("sub")
        if user_id is None:
            print("⚠️ Erreur : `sub` est None")
            raise credentials_exception

        print(f"✅ ID utilisateur récupéré : {user_id}")
        return user_id
    except jwt.ExpiredSignatureError:
        print("❌ Token expiré")
        raise HTTPException(status_code=401, detail="Token expiré")
    except jwt.InvalidTokenError:
        print("❌ Token invalide")
        raise credentials_exception
    

@user_router.get("/me")
def get_user_profile(current_user: int = Depends(get_current_user)):
    """Renvoie l'ID de l'utilisateur connecté"""
    return {"id_user": current_user}