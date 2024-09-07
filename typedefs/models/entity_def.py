from pydantic import BaseModel
from typing import List, Optional
from .attribute_def import AttributeDef
from .relationship_def import RelationshipDef


class EntityDef(BaseModel):
    name: str
    type: str
    qualified_name: str
    alias: str
    description: str
    guid: Optional[str] = None

    properties: List[AttributeDef]
    relationships: List[RelationshipDef]
