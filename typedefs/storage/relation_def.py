import uuid
from typedefs.models.relationship_def import RelationshipDef
from psycopg2.extensions import connection
from utils.logger import setup_logger
from utils.db import row_to_dict

LOGGER = setup_logger(__name__)


def create_relation_def(conn: connection, relation_def: RelationshipDef):
    generated_guid = str(uuid.uuid4())
    with conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO type_defs (guid, name, description, definition, version, created_by, updated_by)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """,
            (
                relation_def.guid,
                relation_def.name,
                relation_def.description,
                relation_def.get_json(),
                relation_def.version,
                relation_def.created_by,
                relation_def.updated_by,
            ),
        )
        conn.commit()
        LOGGER.info(f"Relation definition created: {relation_def.name}")


def get_relation_def(conn: connection, name: str):
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT * FROM type_defs WHERE name = %s
        """,
            (name,),
        )
        row = cur.fetchone()
        if row:
            return RelationshipDef(**row)
        else:
            return None


def update_relation_def(conn: connection, relation_def: RelationshipDef):
    pass
