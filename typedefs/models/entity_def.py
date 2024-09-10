from pydantic import BaseModel
from typing import List, Optional
from .attribute_def import AttributeDef
from .relationship_def import RelationshipDef


class EntityDef(BaseModel):
    name: str
    super_type: Optional[str] = None
    alias: Optional[str] = None
    description: Optional[str] = None
    guid: Optional[str] = None
    internal: bool = False

    properties: List[AttributeDef] = []
    relationships: List[RelationshipDef] = []

    version: int = 1
    created_by: str = "system"
    updated_by: str = "system"

    def get_json(self):
        return self.model_dump_json()
