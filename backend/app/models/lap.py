from sqlalchemy import Column, Integer, Float, Boolean, ForeignKey, Index
from sqlalchemy.orm import relationship
from app.database.session import Base


class Lap(Base):
    __tablename__ = "laps"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    race_id = Column(Integer, ForeignKey("races.id", ondelete="CASCADE"), nullable=False, index=True)
    driver_id = Column(Integer, ForeignKey("drivers.id", ondelete="CASCADE"), nullable=False, index=True)
    lap_number = Column(Integer, nullable=False, index=True)
    lap_time = Column(Float, nullable=True)  # Lap time in seconds (e.g. 78.423)
    sector_1 = Column(Float, nullable=True)
    sector_2 = Column(Float, nullable=True)
    sector_3 = Column(Float, nullable=True)
    position = Column(Integer, nullable=True)
    pit_stop = Column(Boolean, default=False, nullable=False)
    is_valid = Column(Boolean, default=True, nullable=False)

    # Relationships
    race = relationship("Race", back_populates="laps")
    driver = relationship("Driver", back_populates="laps")

    __table_args__ = (
        Index("ix_laps_race_driver_lap", "race_id", "driver_id", "lap_number", unique=True),
        Index("ix_laps_race_lap", "race_id", "lap_number"),
    )
