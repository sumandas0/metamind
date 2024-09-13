from typedefs.models.entity_def import EntityDef
from typedefs.models.relationship_def import RelationshipDef
from typedefs.registry import TypeRegistry
from typing import List


def entity_definition_create_validator(type_registry: TypeRegistry, entity_def: EntityDef) -> None:
    if type_registry.check_type_exists(entity_def.name):
        raise ValueError(f"Entity type '{entity_def.name}' already exists")

    attr_defs = entity_def.get_properties()
    for attr_def in attr_defs:
        if type_registry.get_attribute_definition(attr_def.name):
            raise ValueError(f"Attribute '{attr_def.name}' already exists")

def entity_defition_update_validator(type_registry: TypeRegistry, entity_def: EntityDef) -> None:
    if not type_registry.check_type_exists(entity_def.name):
        raise ValueError(f"Entity type '{entity_def.name}' does not exist")

    attr_defs = entity_def.get_properties()
    for attr_def in attr_defs:
        if not type_registry.get_attribute_definition(attr_def.name):
            raise ValueError(f"Attribute '{attr_def.name}' does not exist")
        
        # If index set true from false, unsupported
        if attr_def.index and not type_registry.get_attribute_definition(attr_def.name).index:
            raise NotImplementedError(f"Cannot set index to true for attribute '{attr_def.name}'")
        
    for relationship_def in entity_def.get_relationships():
        if not type_registry.check_relationship_exists(relationship_def.name):
            raise ValueError(f"Relationship '{relationship_def.name}' does not exist")


def entity_definition_relationship_validator(type_registry: TypeRegistry, entity_def: EntityDef) -> None:
    relationship_defs: List[RelationshipDef] = entity_def.relationships
    if not relationship_defs:
        return

    for relationship_def in relationship_defs:
        validate_relationship(type_registry, relationship_def)


def validate_relationship(type_registry: TypeRegistry, relationship_def: RelationshipDef) -> None:
    if not type_registry.check_type_exists(relationship_def.type):
        raise ValueError(f"Relationship type '{relationship_def.type}' does not exist")

    if not type_registry.check_relationship_exists(relationship_def.name):
        raise ValueError(f"Relationship '{relationship_def.name}' does not exist")

    validate_entity_type(type_registry, relationship_def.source_entity_type, "Source")
    validate_entity_type(type_registry, relationship_def.target_entity_type, "Target")


def validate_entity_type(type_registry: TypeRegistry, entity_type: str, entity_role: str) -> None:
    if not type_registry.check_type_exists(entity_type):
        raise ValueError(f"{entity_role} entity type '{entity_type}' does not exist")