from typedefs.models.entity_def import EntityDef
from typedefs.registry import TypeRegistry


def entity_definition_create_validator(type_registry: TypeRegistry, entity_def: EntityDef):
    if type_registry.check_type_exists(entity_def.name):
        raise ValueError(f"Entity type {entity_def.name} already exists")

    attr_defs = entity_def.properties.get("attributes", [])
    if len(attr_defs) > 0:
        raise ValueError("Attributes not supported for entity definitions")
    for attr_def in attr_defs:
        if type_registry.check_attribute_exists(attr_def.name):
            raise ValueError(f"Attribute {attr_def.name} already exists")
