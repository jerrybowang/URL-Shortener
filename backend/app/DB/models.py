from app.DB.database import Base

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, DateTime
import datetime


class URL(Base):
    __tablename__ = "urls"

    short_key: Mapped[str] = mapped_column(String, primary_key=True, index=True)
    long_url: Mapped[str] = mapped_column(String, nullable=False)
    long_url_hash: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, default=datetime.datetime.now(datetime.timezone.utc), nullable=False
    )
    user: Mapped[str | None] = mapped_column(String, nullable=True)
