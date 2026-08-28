from sqlalchemy import Column, Integer, String, ForeignKey, Index
from sqlalchemy.orm import relationship
from app.database.session import Base


class RaceEvent(Base):
    __tablename__ = "race_events"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    race_id = Column(Integer, ForeignKey("races.id", ondelete="CASCADE"), nullable=False, index=True)
    lap = Column(Integer, nullable=False, index=True)
    start_lap = Column(Integer, nullable=True)
    end_lap = Column(Integer, nullable=True)
    event_type = Column(String(50), nullable=False)  # SAFETY_CAR, VSC, RED_FLAG, RAIN, OTHER
    description = Column(String(255), nullable=True)

    # Relationships
    race = relationship("Race", back_populates="race_events")

    __table_args__ = (
        Index("ix_race_events_race_type", "race_id", "event_type"),
    )
