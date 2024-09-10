from typing import Optional
from typedefs.models.entity_def import EntityDef
from psycopg2.extensions import connection
from utils.logger import setup_logger
from psycopg2 import sql
from typedefs.storage.common import definition_exists

LOGGER = setup_logger(__name__)


def create_entity_def(conn: connection, entity_def: EntityDef) -> None:
    """
    Create a new entity definition in the database.

    Args:
        conn (connection): Database connection object.
        entity_def (EntityDef): Entity definition to be created.

    Raises:
        ValueError: If the entity definition already exists.
    """
    if definition_exists(conn, entity_def.name):
        error_msg = f"Entity definition already exists: {entity_def.name}"
        LOGGER.error(error_msg)
        raise ValueError(error_msg)

    with conn.cursor() as cur:
        sql_stmt = sql.SQL(
            """
            INSERT INTO {table_name} (
                guid, name, super_type, alias, description, type_def_type,
                properties, version, created_by, updated_by
            )
            VALUES (
                {guid}, {name}, {super_type}, {alias}, {description}, {type},
                {properties}, {version}, {created_by}, {updated_by}
            )
            """
        ).format(
            table_name=sql.Identifier("type_defs"),
            guid=sql.Literal(entity_def.guid),
            name=sql.Literal(entity_def.name),
            super_type=sql.Literal(entity_def.super_type),
            alias=sql.Literal(entity_def.alias),
            description=sql.Literal(entity_def.description),
            type=sql.Literal("entity"),
            properties=sql.Literal(entity_def.get_json()),
            version=sql.Literal(entity_def.version),
            created_by=sql.Literal(entity_def.created_by),
            updated_by=sql.Literal(entity_def.updated_by),
        )
        cur.execute(sql_stmt)

    conn.commit()
    LOGGER.info(f"Entity definition created: {entity_def.name}")


def get_entity_def(conn: connection, name: str) -> Optional[EntityDef]:
    """
    Retrieve an entity definition from the database.

    Args:
        conn (connection): Database connection object.
        name (str): Name of the entity definition to retrieve.

    Returns:
        Optional[EntityDef]: The retrieved entity definition, or None if not found.
    """
    with conn.cursor() as cur:
        sql_stmt = sql.SQL(
            """
            SELECT properties FROM type_defs WHERE name = {name}
            """
        ).format(name=sql.Literal(name))
        cur.execute(sql_stmt)
        row = cur.fetchone()
        return EntityDef(**row[0]) if row else None
