from pydantic import BaseModel
from typing import Dict, Any, Optional
from datetime import datetime
from assets.models.entity import Entity


class Relationship(BaseModel):
    type: str
    name: str
    source: Entity
    target: Entity
    properties: Dict[str, Any] = {}
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    created_by: Optional[str] = None
    updated_by: Optional[str] = None