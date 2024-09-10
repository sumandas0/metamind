from dotenv import load_dotenv
from psycopg2 import connect
import os
import uuid
from db.management.create_tables import execute_create_tables

from typedefs.storage.entity_def import create_entity_def, get_entity_def
from typedefs.models.entity_def import EntityDef
from typedefs.models.attribute_def import AttributeDef
from typedefs.models.builtins import BuiltinType

load_dotenv()

PG_CONN_STR = os.getenv("PG_CONN_STR")

# Connect to the database
conn = connect(PG_CONN_STR)

# execute_create_tables(conn, "db/sql")

entity_def = EntityDef(
    name="User",
    alias="User",
    description="A user in the system",
    guid=str(uuid.uuid4()),
    internal=False,
    properties=[
        AttributeDef(
            name="id",
            description="The ID of the user",
            type=BuiltinType.STRING,
            default="",
            required=True,
            index=True,
            unique=True,
        ),
        AttributeDef(
            name="name",
            description="The name of the user",
            type=BuiltinType.STRING,
            default="",
            required=True,
            index=True,
            unique=True,
        ),
    ],
    version=1,
    created_by="system",
    updated_by="system",
)

create_entity_def(conn, entity_def)

entity_def = get_entity_def(conn, "User")
print(entity_def)
