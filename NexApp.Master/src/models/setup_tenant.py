from sqlalchemy import Column, String, Integer,Boolean,DateTime
from .base import Base
from datetime import datetime

class SetupTenant(Base):
    __tablename__ = "setup_tenant"

    Id = Column(Integer, primary_key=True, index=True)
    IsDeleted = Column(Boolean, default=False)
    TenantId = Column(String(255), unique=True, nullable=False)
    ServerName = Column(String(255), nullable=False)
    DatabaseName = Column(String(255), nullable=False)
    ServerUsername = Column(String(255), nullable=False)
    ServerPassword = Column(String(255), nullable=False)
    CreatedBy = Column(Integer)
    CreatedOn = Column(DateTime, default=datetime.utcnow)
    UpdatedBy = Column(Integer)
    UpdatedOn = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    class Config:
        from_attributes = True
