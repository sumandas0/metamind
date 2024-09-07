from pydantic import BaseModel
from typing import List
from .attribute_def import AttributeDef


class EntityDef(BaseModel):
    name: str
    type: str
    qualified_name: str
    alias: str
    description: str
    
    properties: List[AttributeDef]
    