from pydantic import BaseModel
from typing import List, Optional
from typedefs.models.attribute_def import AttributeDef
from enum import Enum, auto


class RelationshipType(Enum):
    ASSOCIATION = auto()
    AGGREGATION = auto()
    COMPOSITION = auto()


class RelationshipDef(BaseModel):
    name: str
    guid: Optional[str] = None
    description: Optional[str] = None
    properties: List[AttributeDef] = []

    source_entity_type: str
    target_entity_type: str

    relationship_type: RelationshipType

    version: int = 1

    created_by: str = "system"
    updated_by: str = "system"

    def get_json(self):
        return self.model_dump_json()
