from typing import Dict, List, Optional, Union
from typedefs.models.entity_def import EntityDef
from typedefs.models.relationship_def import RelationshipDef
from typedefs.models.attribute_def import AttributeDef
from utils.logger import setup_logger

logger = setup_logger(__name__)

class TypeRegistry:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(TypeRegistry, cls).__new__(cls)
            cls._instance._type_registry = {}
            cls._instance._relationship_registry = {}
            cls._instance._attribute_registry = {}
            cls._instance._relationship_attribute_registry = {}
            logger.debug("New TypeRegistry instance created")
        return cls._instance

    def add_entity_def(self, entity_def: EntityDef) -> None:
        logger.debug(f"Attempting to add entity definition: {entity_def.name}")
        if self.check_type_exists(entity_def.name):
            logger.error(f"Entity type {entity_def.name} already exists")
            raise ValueError(f"Entity type {entity_def.name} already exists")

        attr_defs = entity_def.properties
        for attr_def in attr_defs:
            logger.debug(f"Checking attribute: {attr_def.name}")
            if self.check_attribute_exists(attr_def.name):
                logger.error(f"Attribute {attr_def.name} already exists")
                raise ValueError(f"Attribute {attr_def.name} already exists")
            self._attribute_registry[attr_def.name] = attr_def
            logger.debug(f"Added attribute: {attr_def.name}")

        self._type_registry[entity_def.name] = entity_def
        logger.info(f"Successfully added entity definition: {entity_def.name}")

    def add_relationship_def(self, relationship_def: RelationshipDef) -> None:
        logger.debug(f"Attempting to add relationship definition: {relationship_def.name}")
        if self.check_relationship_exists(relationship_def.name):
            logger.error(f"Relationship type {relationship_def.name} already exists")
            raise ValueError(f"Relationship type {relationship_def.name} already exists")

        attr_defs = relationship_def.properties
        for attr_def in attr_defs:
            logger.debug(f"Checking relationship attribute: {attr_def.name}")
            if self.check_relationship_attribute_exists(attr_def.name):
                logger.error(f"Relationship attribute {attr_def.name} already exists")
                raise ValueError(f"Relationship attribute {attr_def.name} already exists")
            self._relationship_attribute_registry[attr_def.name] = attr_def
            logger.debug(f"Added relationship attribute: {attr_def.name}")

        self._relationship_registry[relationship_def.name] = relationship_def
        self._type_registry[relationship_def.name] = relationship_def
        logger.info(f"Successfully added relationship definition: {relationship_def.name}")

    def check_type_exists(self, name: str) -> bool:
        exists = name in self._type_registry
        logger.debug(f"Checking if type {name} exists: {exists}")
        return exists
    
    def check_relationship_exists(self, name: str) -> bool:
        exists = name in self._relationship_registry
        logger.debug(f"Checking if relationship {name} exists: {exists}")
        return exists
    
    def check_relationship_attribute_exists(self, name: str) -> bool:
        exists = name in self._relationship_attribute_registry
        logger.debug(f"Checking if relationship attribute {name} exists: {exists}")
        return exists

    def check_attribute_exists(self, name: str) -> bool:
        exists = name in self._attribute_registry
        logger.debug(f"Checking if attribute {name} exists: {exists}")
        return exists
    
    def get_entity_definition(self, name: str) -> Optional[EntityDef]:
        entity_def = self._type_registry.get(name) if isinstance(self._type_registry.get(name), EntityDef) else None
        logger.debug(f"Getting entity definition for {name}: {'Found' if entity_def else 'Not found'}")
        return entity_def

    def get_relationship_definition(self, name: str) -> Optional[RelationshipDef]:
        rel_def = self._relationship_registry.get(name)
        logger.debug(f"Getting relationship definition for {name}: {'Found' if rel_def else 'Not found'}")
        return rel_def

    def get_relationship_attribute_definition(self, name: str) -> Optional[AttributeDef]:
        attr_def = self._relationship_attribute_registry.get(name)
        logger.debug(f"Getting relationship attribute definition for {name}: {'Found' if attr_def else 'Not found'}")
        return attr_def

    def get_type_definition(self, name: str) -> Optional[Union[EntityDef, RelationshipDef]]:
        type_def = self._type_registry.get(name)
        logger.debug(f"Getting type definition for {name}: {'Found' if type_def else 'Not found'}")
        return type_def

    def get_attribute_definition(self, name: str) -> Optional[AttributeDef]:
        attr_def = self._attribute_registry.get(name)
        logger.debug(f"Getting attribute definition for {name}: {'Found' if attr_def else 'Not found'}")
        return attr_def

    def get_resolved_attributes_type(self, name: str) -> List[AttributeDef]:
        logger.debug(f"Resolving attributes for type: {name}")
        ret = []
        current_type = name
        while current_type:
            type_def = self.get_type_definition(current_type)
            if type_def:
                logger.debug(f"Found type definition for {current_type}")
                ret.extend(type_def.properties)
                current_type = type_def.super_type
            else:
                logger.debug(f"No type definition found for {current_type}")
                break
        logger.debug(f"Resolved {len(ret)} attributes for type {name}")
        return ret

    def remove_type(self, name: str) -> None:
        logger.debug(f"Removing type: {name}")
        self._type_registry.pop(name, None)
        self._relationship_registry.pop(name, None)
        logger.info(f"Removed type: {name}")

    def remove_attribute(self, name: str) -> None:
        logger.debug(f"Removing attribute: {name}")
        self._attribute_registry.pop(name, None)
        self._relationship_attribute_registry.pop(name, None)
        logger.info(f"Removed attribute: {name}")

    def clear(self) -> None:
        logger.debug("Clearing all registries")
        self._type_registry.clear()
        self._relationship_registry.clear()
        self._attribute_registry.clear()
        self._relationship_attribute_registry.clear()
        logger.info("All registries cleared")
