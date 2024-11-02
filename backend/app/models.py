from sqlalchemy import Column, ForeignKey, Integer, String, Date, Time, Enum
from sqlalchemy.orm import relationship

from .database import Base


# Match
class Match(Base):
    __tablename__ = "matches"

    id = Column(Integer, primary_key=True, index=True)
    home_team_uid = Column(String(255))
    away_team_uid = Column(String(255))
    year = Column(Integer)
    month = Column(Integer)
    day = Column(Integer)
    start_time = Column(String(10))
    end_time = Column(String(10))
    location = Column(String(20))


# Team
class Team(Base):
    __tablename__ = "teams"

    id = Column(Integer, primary_key=True, index=True)
    uid = Column(String(255))
    name = Column(String(255))
    region = Column(String(10))
    prefecture = Column(String(10))
    category = Column(String(10))
    league = Column(String(20))
    instagram_user_name = Column(String(20), nullable=True)
    X_user_name = Column(String(20), nullable=True)


# Player
class Player(Base):
    __tablename__ = "players"

    id = Column(Integer, primary_key=True)
    uid = Column(String(255))
    position = Column(Enum("GK", "DF", "MF", "FW", name="positions"))
    number = Column(Integer)
    namae = Column(String(20))
    name = Column(String(20))
    height = Column(Integer)
    weight = Column(Integer)
    previous_team = Column(String(20))


# Recruitment
class Recruitment(Base):
    __tablename__ = "recruitments"

    id = Column(Integer, primary_key=True, index=True)
    uid = Column(String(255))
    status = Column(
        Enum("募集中", "申し込み受領", "マッチ済み", name="Recruitment_status"),
        default="募集中",
    )
    year = Column(Integer)
    month = Column(Integer)
    day = Column(Integer)
    start_time = Column(String(10))
    end_time = Column(String(10))
    location = Column(String(20))

    applications = relationship("Application", back_populates="recruitment")


# Application
class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)
    recruitment_id = Column(Integer, ForeignKey("recruitments.id"))
    uid = Column(String(255))
    status = Column(
        Enum("回答待ち", "承認", "辞退", name="application_status"), default="回答待ち"
    )

    recruitment = relationship("Recruitment", back_populates="applications")
