# TypeDefs: A Type Definition and Registry System

## Overview

TypeDefs is a Python-based system for defining, managing, and validating entity types, relationships, and attributes. It provides a robust framework for creating and maintaining complex data models with built-in validation and type checking.

## Key Components

### Models

1. **EntityDef**: Defines entity types with properties and relationships.
2. **RelationshipDef**: Defines relationships between entities, including cardinality and relationship types.
3. **AttributeDef**: Defines attributes for both entities and relationships.
4. **BuiltinType**: Enumerates the built-in data types supported by the system.

### Registry

The `TypeRegistry` class serves as a central repository for all type definitions. It ensures uniqueness of entity types, relationships, and attributes across the system.

### Validators

The system includes validators to ensure the integrity and consistency of entity and relationship definitions:

- `entity_definition_create_validator`: Validates new entity definitions.
- `entity_defition_update_validator`: Validates updates to existing entity definitions.
- `entity_definition_relationship_validator`: Validates relationships within entity definitions.

## Usage

1. Define your entity types, relationships, and attributes using the provided model classes.
2. Use the `TypeRegistry` to register and manage your type definitions.
3. Employ the validators to ensure the correctness of your definitions before adding them to the registry.

## Example
