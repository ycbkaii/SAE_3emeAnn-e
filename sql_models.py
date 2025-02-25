from datetime import datetime
from sqlmodel import Column, Date, Integer, SQLModel, String, ForeignKey, TIMESTAMP,MetaData ,Relationship

metaData =  MetaData(schema="masterbook")

class PossedePersonnage(SQLModel, table = True):
    __tablename__ = '_possede_personnage'
    metadata =  metaData
    id_books = Column(Integer, ForeignKey('_livre.id_livre'), primary_key=True)
    id_personnage = Column(Integer, ForeignKey('_personnage.id_personnage'), primary_key=True)

class APublie(SQLModel, table = True):
    __tablename__ = '_a_publie'
    metadata =  metaData
    id_publisher = Column(Integer, ForeignKey('_publisher.id_publisher'), primary_key=True)
    id_book = Column(Integer, ForeignKey('_livre.id_livre'), primary_key=True)

class GenresDuLivre(SQLModel, table = True):
    __tablename__ = '_genres_du_livre'
    metadata =  metaData
    id_genre = Column(Integer, ForeignKey('_genre.id_genre'), primary_key=True)
    id_livre = Column(Integer, ForeignKey('_livre.id_livre'), primary_key=True)

class RecompenseEn(SQLModel, table = True):
    __tablename__ = '_recompense_en'
    metadata =  metaData
    id_livre = Column(Integer, ForeignKey('_livre.id_livre'), primary_key=True)
    id_awards = Column(Integer, ForeignKey('_awards.id_awards'), primary_key=True)
    date = Column(Date, default=datetime.now().date())

class VitesseDeLecture(SQLModel, table = True):
    __tablename__ = '_vitesse_de_lecture'
    metadata =  metaData
    id_vitesse_lecture = Column(Integer, primary_key=True)
    nom_categorie = Column(String(50), nullable=False)

class CriteresPourChoisirLivre(SQLModel, table = True):
    __tablename__ = '_critere_pour_choisir_livre'
    metadata =  metaData
    id_critere = Column(Integer, primary_key=True)
    critere = Column(String(50), nullable=False)

class SecteurDeTravail(SQLModel, table = True):
    __tablename__ = '_secteur_de_travail'
    metadata =  metaData
    id_secteur = Column(Integer, primary_key=True)
    nom_secteur = Column(String(50), nullable=False)

class LieuxLecture(SQLModel, table = True):
    __tablename__ = '_lieux_lecture'
    metadata =  metaData
    id_lieux = Column(Integer, primary_key=True)
    nom_lieux = Column(String(50), nullable=False)

class MoodSelection(SQLModel, table = True):
    __tablename__ = '_mood_selection'
    metadata =  metaData
    id_selection = Column(Integer, primary_key=True)
    nom_humeur = Column(String)
    date_selection = Column(TIMESTAMP)

class PreferenceLecture(SQLModel, table = True):
    __tablename__ = '_preference_lecture'
    metadata =  metaData
    id_preference = Column(Integer, primary_key=True)
    preference = Column(String)

class Utilisateur(SQLModel, table = True):
    __tablename__ = '_utilisateur'
    metadata =  metaData
    id_user = Column(Integer, primary_key=True)
    age = Column(Integer)
    id_selection = Column(Integer, ForeignKey('_mood_selection.id_selection'), nullable=False)
    id_vitesse_lecture = Column(Integer, ForeignKey('_vitesse_de_lecture.id_vitesse_lecture'), nullable=False)
    id_secteur = Column(Integer, ForeignKey('_secteur_de_travail.id_secteur'))
    id_raison_lecture = Relationship("CategoriesRaisonLecture", secondary="_utilisateur_raison")

class CategoriesRaisonLecture(SQLModel, table = True):
    __tablename__ = '_categories_raison_lecture'
    metadata =  metaData
    id_raison_lecture = Column(Integer, primary_key=True)
    categorie = Column(String)

class UserReasonRelation(SQLModel, table = True):
    __tablename__ = '_utilisateur_raison'
    metadata =  metaData
    id_user = Column(Integer, ForeignKey('_utilisateur.id_user'), primary_key=True)
    id_raison_lecture = Column(Integer, ForeignKey('_categories_raison_lecture.id_raison_lecture'), primary_key=True)