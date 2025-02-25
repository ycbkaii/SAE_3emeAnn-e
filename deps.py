from collections.abc import Generator
from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from pydantic import ValidationError
from sqlmodel import Session, create_engine
import secrets

from models import TokenPayload, User

SECRET_KEY = secrets.token_urlsafe(32)
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


engine = create_engine("postgresql://root:root@localhost:5432/masterbook", echo=True)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/usr/token")


def get_db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


# Permet d'avoir une session dans la BDD
SessionDep = Annotated[Session, Depends(get_db)]

TokenDep = Annotated[str, Depends(oauth2_scheme)]


def get_current_user(session: SessionDep, token: TokenDep) -> User:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        token_data = TokenPayload(**payload)
    except (InvalidTokenError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    user = session.get(User, token_data.sub)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


CurrentUser = Annotated[User, Depends(get_current_user)]

def get_current_user_id(user : CurrentUser) -> int:
    return user.id_user

CurrentUserId = Annotated[int,Depends(get_current_user_id)]