from typing import List
from .models.entity_def import EntityDef
from .models.relationship_def import RelationshipDef
from .models.attribute_def import AttributeDef


class TypeRegistry:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(TypeRegistry, cls).__new__(cls)
            cls._instance.type_registry = {}
        return cls._instance

    def add_entity_def(self, entityDef: EntityDef):
        if self.check_type_exists(entityDef.name):
            raise ValueError(f"Entity type {entityDef.name} already exists")
        self.type_registry[entityDef.name] = entityDef

    def add_relationship_def(self, relationshipDef: RelationshipDef):
        if self.check_type_exists(relationshipDef.name):
            raise ValueError(f"Relationship type {relationshipDef.name} already exists")
        self.type_registry[relationshipDef.name] = relationshipDef

    def check_type_exists(self, name: str) -> bool:
        return self.type_registry.get(name) is not None

    def get_type_definition(self, name: str) -> EntityDef | RelationshipDef:
        return self.type_registry.get(name)

    def get_resolved_attributes_type(self, name: str) -> List[AttributeDef]:
        ret = []
        current_type = name
        while current_type:
            type_def = self.get_type_definition(current_type)
            if type_def:
                ret.append(type_def.properties)
                current_type = type_def.super_type
            else:
                break
        return ret

    def remove_type(self, name: str):
        self.type_registry.pop(name, None)

    def clear(self):
        self.type_registry.clear()
