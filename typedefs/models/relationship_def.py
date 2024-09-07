from pydantic import BaseModel
from typing import List
from .attribute_def import AttributeDef
from .entity_def import EntityDef
from enum import Enum, auto


class RelationshipType(Enum):
    ASSOCIATION = auto()
    AGGREGATION = auto()
    COMPOSITION = auto()


class RelationshipDef(BaseModel):
    name: str
    guid: str
    description: str
    type: str
    properties: List[AttributeDef]
    
    source: EntityDef
    target: EntityDef
    
    relationship_type: RelationshipType