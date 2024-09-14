import uuid
from typedefs.models.relationship_def import RelationshipDef
from psycopg2.extensions import connection
from utils.logger import setup_logger
from utils.db import row_to_dict
from psycopg2 import sql

LOGGER = setup_logger(__name__)


def create_relation_def(conn: connection, relation_def: RelationshipDef):
    with conn.cursor() as cur:
        query = sql.SQL("""
            INSERT INTO {table} ({fields})
            VALUES ({values})
        """).format(
            table=sql.Identifier("type_defs"),
            fields=sql.SQL(", ").join(map(sql.Identifier, [
                "guid", "name", "description", "definition", "version", "created_by", "updated_by"
            ])),
            values=sql.SQL(", ").join([sql.Literal(val) for val in [
                relation_def.guid,
                relation_def.name,
                relation_def.description,
                relation_def.get_json(),
                relation_def.version,
                relation_def.created_by,
                relation_def.updated_by,
            ]])
        )
        cur.execute(query)
        conn.commit()
        LOGGER.info(f"Relation definition created: {relation_def.name}")


def get_relation_def(conn: connection, name: str):
    with conn.cursor() as cur:
        query = sql.SQL("""
            SELECT * FROM {table} WHERE {field} = {value}
        """).format(
            table=sql.Identifier("type_defs"),
            field=sql.Identifier("name"),
            value=sql.Literal(name)
        )
        cur.execute(query)
        row = cur.fetchone()
        if row:
            return RelationshipDef(**row_to_dict(cur, row))
        else:
            return None


def update_relation_def(conn: connection, relation_def: RelationshipDef):
    pass
