import os
import orjson
import psycopg2
from typedefs.models.entity_def import EntityDef
from typedefs.registry import TypeRegistry
from typedefs.storage.entity_def import create_entity_def
from db.management.create_typedefs_tables import execute_create_tables


conn = psycopg2.connect(os.environ["PG_CONN_STR"])
type_registry = TypeRegistry()

execute_create_tables(conn, "db/sql")

def load_types(parent_folder: str):
    typedefs = []
    for root, _, files in os.walk(parent_folder):
        for file in files:
            if file.endswith(".json"):
                with open(os.path.join(root, file), "rb") as f:
                    data = orjson.loads(f.read())
                    entity_def = EntityDef(**data)
                    typedefs.append(entity_def)
    return typedefs


entity_defs = load_types("types")
for entity_def in entity_defs:
    create_entity_def(conn, type_registry, entity_def)