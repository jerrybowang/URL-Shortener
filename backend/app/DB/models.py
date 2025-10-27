from sqlalchemy import Column, String, DateTime
from app.DB.database import Base
import datetime

class URL(Base):
    __tablename__ = "urls"

    short_key = Column(String, primary_key=True, index=True)
    long_url = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.now(datetime.timezone.utc), nullable=False)
    user = Column(String, nullable=True)