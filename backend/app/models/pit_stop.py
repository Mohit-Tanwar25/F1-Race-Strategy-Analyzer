from sqlalchemy import Column, Integer, Float, ForeignKey, Index
from sqlalchemy.orm import relationship
from app.database.session import Base


class PitStop(Base):
    __tablename__ = "pit_stops"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    race_id = Column(Integer, ForeignKey("races.id", ondelete="CASCADE"), nullable=False, index=True)
    driver_id = Column(Integer, ForeignKey("drivers.id", ondelete="CASCADE"), nullable=False, index=True)
    lap = Column(Integer, nullable=False, index=True)
    duration = Column(Float, nullable=True)  # Pit stop stationary/lane duration in seconds
    stop_number = Column(Integer, nullable=False)

    # Relationships
    race = relationship("Race", back_populates="pit_stops")
    driver = relationship("Driver", back_populates="pit_stops")

    __table_args__ = (
        Index("ix_pitstops_race_driver_stop", "race_id", "driver_id", "stop_number", unique=True),
    )
