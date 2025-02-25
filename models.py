from pydantic import EmailStr, BaseModel
from typing import Optional
from sqlmodel import Field, MetaData, SQLModel


metaData = MetaData(schema="masterbook")

# Shared properties
class _utilisateur(SQLModel, table=True):
    metadata = metaData
    id_user: int = Field(default=None, primary_key=True)
    age: Optional[int] = None
    id_selection: int
    id_vitesse_lecture: int
    id_secteur: Optional[int] = None
    id_genre_sex: int
    id_prefere_lire: int
    # email: str


# Properties to receive via API on creation
class UserCreate(_utilisateur):
    password: str = Field(min_length=8, max_length=40)


class UserRegister(SQLModel):
    email: EmailStr = Field(max_length=255)
    password: str = Field(min_length=8, max_length=40)
    full_name: str | None = Field(default=None, max_length=255)


# Properties to receive via API on update, all are optional
class UserUpdate(_utilisateur):
    email: EmailStr | None = Field(default=None, max_length=255)  # type: ignore
    password: str | None = Field(default=None, min_length=8, max_length=40)


class UserUpdateMe(SQLModel):
    full_name: str | None = Field(default=None, max_length=255)
    email: EmailStr | None = Field(default=None, max_length=255)


class UpdatePassword(SQLModel):
    current_password: str = Field(min_length=8, max_length=40)
    new_password: str = Field(min_length=8, max_length=40)


# Database model, database table inferred from class name
class User(_utilisateur):
    hashed_password: str


class _livre(SQLModel, table=True):
    metadata = metaData
    id_livre: int = Field(default=None, primary_key=True)
    title: str
    description: Optional[str] = None
    number_of_page: int
    date_published: Optional[str] = None
    isbn: Optional[str] = None
    nom_de_la_saga: Optional[str] = None
    numero_opus: Optional[int] = None
    review_count: int
    rating_count: int
    average_rating: float
    five_star_ratings: int
    four_star_ratings: int
    three_star_ratings: int
    two_star_ratings: int
    one_star_ratings: int
    cover_link: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenPayload(SQLModel):
    sub: str | None = None
