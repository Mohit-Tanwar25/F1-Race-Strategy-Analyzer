from sqlalchemy import Column, Integer, String, Date, Index
from sqlalchemy.orm import relationship
from app.database.session import Base


class Race(Base):
    __tablename__ = "races"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    season = Column(Integer, nullable=False, index=True)
    round = Column(Integer, nullable=False)
    name = Column(String(150), nullable=False)
    circuit = Column(String(150), nullable=False)
    country = Column(String(100), nullable=False)
    date = Column(String(50), nullable=False)
    total_laps = Column(Integer, nullable=True)
    winner_name = Column(String(100), nullable=True)

    # Relationships
    laps = relationship("Lap", back_populates="race", cascade="all, delete-orphan")
    stints = relationship("Stint", back_populates="race", cascade="all, delete-orphan")
    pit_stops = relationship("PitStop", back_populates="race", cascade="all, delete-orphan")
    race_events = relationship("RaceEvent", back_populates="race", cascade="all, delete-orphan")

    __table_args__ = (
        Index("ix_races_season_round", "season", "round", unique=True),
    )
