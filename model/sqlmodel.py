from sqlmodel import create_engine


# engine = create_engine("postgres-sae:5432")
engine = create_engine("localhost:5432", echo=True)
