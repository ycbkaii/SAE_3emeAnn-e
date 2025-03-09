from pydantic import EmailStr, BaseModel
from typing import Optional
from sqlmodel import Column, Field, Integer, MetaData, SQLModel, Sequence, func


metaData = MetaData(schema="masterbook")

# Shared properties
class User(SQLModel, table=True):
    __tablename__ = "_utilisateur"
    metadata = metaData
    id_user: Optional[int] = Field(default=None, primary_key=True)
    age: Optional[int] = None
    id_selection: int
    id_vitesse_lecture: int
    id_secteur: Optional[int] = None
    id_genre_sex: int
    id_prefere_lire: int
    


# Properties to receive via API on creation
class UserCreate(User):
    password: str = Field(min_length=8, max_length=40)


class UserRegister(SQLModel):
    email: EmailStr = Field(max_length=255)
    password: str = Field(min_length=8, max_length=40)
    full_name: str | None = Field(default=None, max_length=255)


class UserUpdateMe(SQLModel):
    full_name: str | None = Field(default=None, max_length=255)
    email: EmailStr | None = Field(default=None, max_length=255)


class UpdatePassword(SQLModel):
    current_password: str = Field(min_length=8, max_length=40)
    new_password: str = Field(min_length=8, max_length=40)

class _livre(SQLModel, table=True):
    metadata = metaData
    id_livre: int = Field(default=None, primary_key=True)
    title: str
    description: Optional[str] = None
    number_of_page: int
    date_published: Optional[str] = None
    isbn: Optional[str] = None
    nom_de_la_saga: Optional[str] = None
    numéro_opus: Optional[int] = None
    review_count: int
    rating_count: int
    average_rating: float
    five_star_ratings: int
    four_star_ratings: int
    three_star_ratings: int
    two_star_ratings: int
    one_star_ratings: int
    # cover_link: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    sub: str | None = None
