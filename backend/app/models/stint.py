from sqlalchemy import Column, Integer, String, ForeignKey, Index
from sqlalchemy.orm import relationship
from app.database.session import Base


class Stint(Base):
    __tablename__ = "stints"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    race_id = Column(Integer, ForeignKey("races.id", ondelete="CASCADE"), nullable=False, index=True)
    driver_id = Column(Integer, ForeignKey("drivers.id", ondelete="CASCADE"), nullable=False, index=True)
    stint_number = Column(Integer, nullable=False)
    start_lap = Column(Integer, nullable=False)
    end_lap = Column(Integer, nullable=False)
    compound = Column(String(50), nullable=False)  # SOFT, MEDIUM, HARD, INTERMEDIATE, WET
    tyre_age_start = Column(Integer, default=0, nullable=False)
    tyre_age_end = Column(Integer, default=0, nullable=False)

    # Relationships
    race = relationship("Race", back_populates="stints")
    driver = relationship("Driver", back_populates="stints")

    __table_args__ = (
        Index("ix_stints_race_driver_stint", "race_id", "driver_id", "stint_number", unique=True),
    )
