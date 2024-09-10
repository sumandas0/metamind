import configparser
from psycopg2.extensions import connection
from typedefs.models.attribute_def import AttributeDef
from typedefs.models.builtins import BuiltinType
from typedefs.models.entity_def import EntityDef
from utils.logger import get_logger
from psycopg2 import sql

LOGGER = get_logger(__name__)


class PostgresIndexStore:
    def __init__(self, conn: connection):
        self.conn = conn

    def init_index(self) -> None:
        index_stmt = """
            CREATE TABLE IF NOT EXISTS attributes_index (
                guid VARCHAR(255) PRIMARY KEY,
                type_name VARCHAR(255) NOT NULL,
                qualified_name VARCHAR(1024) NOT NULL
            );

            CREATE UNIQUE INDEX IF NOT EXISTS attributes_index_type_name_qualified_name ON attributes_index (type_name, qualified_name);
            CREATE UNIQUE INDEX IF NOT EXISTS attributes_index_guid ON attributes_index (guid);
        """
        with self.conn.cursor() as cur:
            cur.execute(sql.SQL(index_stmt))
            self.conn.commit()

    def get_attribute_type_name(self, attribute: AttributeDef) -> str:
        # TODO: Implement this
        return "VARCHAR"
    
    def get_index_creation_stmt(self,attribute: AttributeDef, index_name: str) -> str:
        index_config = configparser.ConfigParser()
        index_config.read("index.config")
        match attribute.type:
            case BuiltinType.VECTOR:
                provider = index_config["Vector"]["provider"]
                vector_index_type = index_config["Vector"]["index_type"]
                if provider == "pgvector":
                    vector_ops = index_config["Vector"]["vector_ops"]
                    return f"USING {vector_index_type}({index_name} {vector_ops})"
                else:
                    return f"USING {vector_index_type}({index_name})"
            case _:
                return f"({index_name})"
                

    def add_attribute_index(self, entity_def: EntityDef, attribute: AttributeDef) -> None:
        if self.attribute_index_exists(entity_def, attribute):
            LOGGER.info(f"Index for {entity_def.name}.{attribute.name} already exists")
            return

        index_name = self.generate_index_name(entity_def, attribute)
        index_type = self.get_attribute_type_name(attribute)
        add_column_stmt = sql.SQL("""
            ALTER TABLE {table_name}
            ADD COLUMN {index_name} {index_type};
        """).format(
            table_name=sql.Identifier("attributes_index"),
            index_name=sql.Identifier(index_name),
            index_type=sql.SQL(index_type),
        )
        
        create_index_stmt = sql.SQL("""
            CREATE INDEX {index_name} ON {table_name} ({index_stmt});
        """).format(
            table_name=sql.Identifier("attributes_index"),
            index_name=sql.Identifier(index_name),
            index_stmt=sql.SQL(self.get_index_creation_stmt(attribute, index_name))
        )

        LOGGER.info(f"Adding index {index_name} to table {entity_def.name}")
        with self.conn.cursor() as cur:
            cur.execute(add_column_stmt)
            cur.execute(create_index_stmt)
            self.conn.commit()

    def generate_index_name(self, entity_def: EntityDef, attribute: AttributeDef) -> str:
        return f"{entity_def.name}_{attribute.name}"

    def attribute_index_exists(self, entity_def: EntityDef, attribute: AttributeDef) -> bool:
        index_name = self.generate_index_name(entity_def, attribute)
        # Check if column with index_name exists else return false
        with self.conn.cursor() as cur:
            cur.execute(f"SELECT EXISTS (SELECT 1 FROM pg_class WHERE relname = '{index_name}');")
            return cur.fetchone()[0]
