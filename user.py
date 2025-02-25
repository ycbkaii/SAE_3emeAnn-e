from datetime import datetime, timedelta, timezone
import secrets
import jwt
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from sqlmodel import Session, select
from models import User, UserCreate
from models import Token
from typing import Annotated,Any
from deps import SessionDep

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

def get_user(session : Session, username: str):
    statement = select(User).where(User.email == username)
    session_user = session.exec(statement).first()
    return session_user


def authenticate_user(session : Session, username: str, password: str):
    user = get_user(session, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def create_user(*, session: Session, user_create: UserCreate) -> User:
    db_obj = User.model_validate(
        user_create, update={"hashed_password": get_password_hash(user_create.password)}
    )
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj



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
        session=session, username=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    return Token(
        access_token=create_access_token(
            user.id_user, expires_delta=access_token_expires
        )
    )

# @user_router.get("/users/me/", response_model=User)
# async def read_users_me(
#     current_user: Annotated[User, Depends(get_current_user)],
# ):
#     return current_user


# @user_router.get("/users/me/items/")
# async def read_own_items(
#     current_user: Annotated[User, Depends(get_current_user)],
# ):
#     return [{"item_id": "Foo", "owner": current_user.username}]
