from typedefs.models.entity_def import EntityDef
from typedefs.models.relationship_def import RelationshipDef
from typedefs.registry import TypeRegistry
from typing import List
from utils.logger import setup_logger

logger = setup_logger(__name__)

def entity_definition_create_validator(type_registry: TypeRegistry, entity_def: EntityDef) -> None:
    logger.debug(f"Validating creation of entity definition: {entity_def.name}")
    if type_registry.check_type_exists(entity_def.name):
        logger.error(f"Entity type '{entity_def.name}' already exists")
        raise ValueError(f"Entity type '{entity_def.name}' already exists")

    attr_defs = entity_def.get_properties()
    for attr_def in attr_defs:
        logger.debug(f"Checking attribute: {attr_def.name}")
        if type_registry.get_attribute_definition(attr_def.name):
            logger.error(f"Attribute '{attr_def.name}' already exists")
            raise ValueError(f"Attribute '{attr_def.name}' already exists")
    logger.info(f"Entity definition '{entity_def.name}' validated successfully for creation")

def entity_defition_update_validator(type_registry: TypeRegistry, entity_def: EntityDef) -> None:
    logger.debug(f"Validating update of entity definition: {entity_def.name}")
    if not type_registry.check_type_exists(entity_def.name):
        logger.error(f"Entity type '{entity_def.name}' does not exist")
        raise ValueError(f"Entity type '{entity_def.name}' does not exist")

    attr_defs = entity_def.get_properties()
    for attr_def in attr_defs:
        logger.debug(f"Checking attribute: {attr_def.name}")
        if not type_registry.get_attribute_definition(attr_def.name):
            logger.error(f"Attribute '{attr_def.name}' does not exist")
            raise ValueError(f"Attribute '{attr_def.name}' does not exist")
        
        # If index set true from false, unsupported
        if attr_def.index and not type_registry.get_attribute_definition(attr_def.name).index:
            logger.error(f"Cannot set index to true for attribute '{attr_def.name}'")
            raise NotImplementedError(f"Cannot set index to true for attribute '{attr_def.name}'")
        
    for relationship_def in entity_def.get_relationships():
        logger.debug(f"Checking relationship: {relationship_def.name}")
        if not type_registry.check_relationship_exists(relationship_def.name):
            logger.error(f"Relationship '{relationship_def.name}' does not exist")
            raise ValueError(f"Relationship '{relationship_def.name}' does not exist")
    logger.info(f"Entity definition '{entity_def.name}' validated successfully for update")

def entity_definition_relationship_validator(type_registry: TypeRegistry, entity_def: EntityDef) -> None:
    logger.debug(f"Validating relationships for entity definition: {entity_def.name}")
    relationship_defs: List[RelationshipDef] = entity_def.relationships
    if not relationship_defs:
        logger.info(f"No relationships found for entity definition: {entity_def.name}")
        return

    for relationship_def in relationship_defs:
        validate_relationship(type_registry, relationship_def)
    logger.info(f"Relationships for entity definition '{entity_def.name}' validated successfully")

def validate_relationship(type_registry: TypeRegistry, relationship_def: RelationshipDef) -> None:
    logger.debug(f"Validating relationship: {relationship_def.name}")
    if not type_registry.check_type_exists(relationship_def.type):
        logger.error(f"Relationship type '{relationship_def.type}' does not exist")
        raise ValueError(f"Relationship type '{relationship_def.type}' does not exist")

    if not type_registry.check_relationship_exists(relationship_def.name):
        logger.error(f"Relationship '{relationship_def.name}' does not exist")
        raise ValueError(f"Relationship '{relationship_def.name}' does not exist")

    validate_entity_type(type_registry, relationship_def.source_entity_type, "Source")
    validate_entity_type(type_registry, relationship_def.target_entity_type, "Target")
    logger.info(f"Relationship '{relationship_def.name}' validated successfully")

def validate_entity_type(type_registry: TypeRegistry, entity_type: str, entity_role: str) -> None:
    logger.debug(f"Validating {entity_role} entity type: {entity_type}")
    if not type_registry.check_type_exists(entity_type):
        logger.error(f"{entity_role} entity type '{entity_type}' does not exist")
        raise ValueError(f"{entity_role} entity type '{entity_type}' does not exist")
    logger.info(f"{entity_role} entity type '{entity_type}' validated successfully")