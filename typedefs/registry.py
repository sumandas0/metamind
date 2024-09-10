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
            cls._instance.attribute_registry = {}
        return cls._instance

    def add_entity_def(self, entityDef: EntityDef):
        if self.check_type_exists(entityDef.name):
            raise ValueError(f"Entity type {entityDef.name} already exists")

        attr_defs = entityDef.properties.get("attributes", [])
        for attr_def in attr_defs:
            if self.check_attribute_exists(attr_def.name):
                raise ValueError(f"Attribute {attr_def.name} already exists")
            self.attribute_registry[attr_def.name] = attr_def

        self.type_registry[entityDef.name] = entityDef

    def add_relationship_def(self, relationshipDef: RelationshipDef):
        if self.check_type_exists(relationshipDef.name):
            raise ValueError(f"Relationship type {relationshipDef.name} already exists")

        attr_defs = relationshipDef.properties.get("attributes", [])
        for attr_def in attr_defs:
            if self.check_attribute_exists(attr_def.name):
                raise ValueError(f"Attribute {attr_def.name} already exists")
            self.attribute_registry[attr_def.name] = attr_def

        self.type_registry[relationshipDef.name] = relationshipDef

    def check_type_exists(self, name: str) -> bool:
        return self.type_registry.get(name) is not None

    def check_attribute_exists(self, name: str) -> bool:
        return self.attribute_registry.get(name) is not None

    def get_type_definition(self, name: str) -> EntityDef | RelationshipDef:
        return self.type_registry.get(name)

    def get_attribute_definition(self, name: str) -> AttributeDef:
        return self.attribute_registry.get(name)

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

    def remove_attribute(self, name: str):
        self.attribute_registry.pop(name, None)

    def clear(self):
        self.type_registry.clear()
        self.attribute_registry.clear()
