from sqlalchemy import Column, Integer, String, Index
from sqlalchemy.orm import relationship
from app.database.session import Base


class Driver(Base):
    __tablename__ = "drivers"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    driver_code = Column(String(10), unique=True, index=True, nullable=False)
    full_name = Column(String(100), nullable=False)
    permanent_number = Column(Integer, nullable=True)
    team = Column(String(100), nullable=False)
    team_color = Column(String(10), nullable=True, default="#E10600")

    # Relationships
    laps = relationship("Lap", back_populates="driver")
    stints = relationship("Stint", back_populates="driver")
    pit_stops = relationship("PitStop", back_populates="driver")
