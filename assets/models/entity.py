from pydantic import BaseModel
from typing import Dict, Any, Optional
from datetime import datetime



class Entity(BaseModel):
    type: str
    guid: Optional[str] = None
    qualified_name: Optional[str] = None
    properties: Dict[str, Any] = {}
    relationship_properties: Dict[str, Any] = {}
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    created_by: Optional[str] = None
    updated_by: Optional[str] = None
    
    def is_identifier_present(self) -> bool:
        return self.guid is not None or (self.qualified_name is not None and self.type is not None)