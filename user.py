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


def get_user(session: Session, email: str,passwd):
    statement = select(User).where(User.id_user == email)
    session_user = session.exec(statement).first()
    return session_user


def authenticate_user(session: Session, email: str, password: str):
    user = get_user(session, email,password)
    if not user:
        return False
    # if not verify_password(password, user.hashed_password):
    #     return False
    # user : User = User(id_user=5)
    return user


def create_user(user_create: UserCreate):
    db_obj = User.model_validate(
        user_create, update={"passwd": get_password_hash(user_create.password)}
    )
    conn = psycopg2.connect(
        database="masterbook",
        port="5432",
        user="root",
        # host="localhost",
        host="localhost",
        password="root",
    )
    cursor = conn.cursor()
    query = f"INSERT INTO masterbook._utilisateur(age, email, passwd, id_selection, id_vitesse_lecture, id_secteur, id_genre_sex, id_prefere_lire) VALUES ('{db_obj.age}', '{db_obj.email}', '{db_obj.passwd}', {db_obj.id_selection}, {db_obj.id_vitesse_lecture}, {db_obj.id_secteur}, {db_obj.id_genre_sex}, {db_obj.id_prefere_lire});"

    cursor.execute(query)


def create_access_token(subject: str | Any, expires_delta: timedelta) -> str:
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


@user_router.post("/token")
def login_access_token(
    session: SessionDep, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> Token:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = authenticate_user(
        session=session, email=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    return Token(
        access_token=create_access_token(
            user.id_user, expires_delta=access_token_expires
        )
    )


class Form_data_create_user(BaseModel) :
    email : str
    password : str
    age : int
    id_genre_sex : int
    id_secteur : int
    id_prefere_lire : int
    id_vitesse_lecture : int
    id_selection : int


@user_router.post("/create")
def create_user_route(session: SessionDep,form_data : Annotated[Form_data_create_user,Depends()]) :
    create_user(user_create=form_data )
    return True

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id = payload.get("sub")
        if id is None:
            raise credentials_exception
        return id
    except InvalidTokenError:
        raise credentials_exception

@user_router.get("/get_id")
def get_id(current_user: Annotated[int, Depends(get_current_user)]) :
    return current_user


# @user_router.get("/users/me/items/")
# async def read_own_items(
#     current_user: Annotated[User, Depends(get_current_user)],
# ):
#     return [{"item_id": "Foo", "owner": current_user.username}]
