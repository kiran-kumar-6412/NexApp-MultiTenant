from sqlalchemy import Column, String, Integer, Boolean, DateTime
from datetime import datetime
from .base import Base

class SetupUser(Base):
    __tablename__ = "setup_user"

    Id = Column(Integer, primary_key=True, index=True)
    IsDeleted = Column(Boolean, default=False)
    Username = Column(String(255), unique=True, index=True, nullable=False)
    Password = Column(String(255), nullable=False)
    CreatedBy = Column(Integer)
    CreatedOn = Column(DateTime, default=datetime.utcnow)
    UpdatedBy = Column(Integer)
    UpdatedOn = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    class Config:
        from_attributes = True
