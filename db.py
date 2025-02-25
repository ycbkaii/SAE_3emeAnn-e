from sqlmodel import create_engine


# engine = create_engine("postgres-sae:5432")
engine = create_engine("postgresql://root:root@localhost:5433/masterbook", echo=True)
