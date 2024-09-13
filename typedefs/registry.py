from typing import Dict, List, Optional, Union
from typedefs.models.entity_def import EntityDef
from typedefs.models.relationship_def import RelationshipDef
from typedefs.models.attribute_def import AttributeDef


class TypeRegistry:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(TypeRegistry, cls).__new__(cls)
            cls._instance._type_registry = {}
            cls._instance._relationship_registry = {}
            cls._instance._attribute_registry = {}
            cls._instance._relationship_attribute_registry = {}
        return cls._instance

    def add_entity_def(self, entity_def: EntityDef) -> None:
        if self.check_type_exists(entity_def.name):
            raise ValueError(f"Entity type {entity_def.name} already exists")

        attr_defs = entity_def.properties
        for attr_def in attr_defs:
            if self.check_attribute_exists(attr_def.name):
                raise ValueError(f"Attribute {attr_def.name} already exists")
            self._attribute_registry[attr_def.name] = attr_def

        self._type_registry[entity_def.name] = entity_def

    def add_relationship_def(self, relationship_def: RelationshipDef) -> None:
        if self.check_relationship_exists(relationship_def.name):
            raise ValueError(f"Relationship type {relationship_def.name} already exists")

        attr_defs = relationship_def.properties
        for attr_def in attr_defs:
            if self.check_relationship_attribute_exists(attr_def.name):
                raise ValueError(f"Relationship attribute {attr_def.name} already exists")
            self._relationship_attribute_registry[attr_def.name] = attr_def

        self._relationship_registry[relationship_def.name] = relationship_def
        self._type_registry[relationship_def.name] = relationship_def

    def check_type_exists(self, name: str) -> bool:
        return name in self._type_registry
    
    def check_relationship_exists(self, name: str) -> bool:
        return name in self._relationship_registry
    
    def check_relationship_attribute_exists(self, name: str) -> bool:
        return name in self._relationship_attribute_registry

    def check_attribute_exists(self, name: str) -> bool:
        return name in self._attribute_registry
    
    def get_entity_definition(self, name: str) -> Optional[EntityDef]:
        return self._type_registry.get(name) if isinstance(self._type_registry.get(name), EntityDef) else None

    def get_relationship_definition(self, name: str) -> Optional[RelationshipDef]:
        return self._relationship_registry.get(name)

    def get_relationship_attribute_definition(self, name: str) -> Optional[AttributeDef]:
        return self._relationship_attribute_registry.get(name)

    def get_type_definition(self, name: str) -> Optional[Union[EntityDef, RelationshipDef]]:
        return self._type_registry.get(name)

    def get_attribute_definition(self, name: str) -> Optional[AttributeDef]:
        return self._attribute_registry.get(name)

    def get_resolved_attributes_type(self, name: str) -> List[AttributeDef]:
        ret = []
        current_type = name
        while current_type:
            type_def = self.get_type_definition(current_type)
            if type_def:
                ret.extend(type_def.properties)
                current_type = type_def.super_type
            else:
                break
        return ret

    def remove_type(self, name: str) -> None:
        self._type_registry.pop(name, None)
        self._relationship_registry.pop(name, None)

    def remove_attribute(self, name: str) -> None:
        self._attribute_registry.pop(name, None)
        self._relationship_attribute_registry.pop(name, None)

    def clear(self) -> None:
        self._type_registry.clear()
        self._relationship_registry.clear()
        self._attribute_registry.clear()
        self._relationship_attribute_registry.clear()
