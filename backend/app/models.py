from pydantic import BaseModel
from typing import Optional


class URLRequest(BaseModel):
    long_url: str
    custom_alias: Optional[str] = None


class LinkRequest(BaseModel):
    primary_user_id: str
    provider: str
    secondary_user_id: str
    connection_id: Optional[str] = None
