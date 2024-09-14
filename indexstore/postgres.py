import configparser
from psycopg2.extensions import connection
from typedefs.models.attribute_def import AttributeDef
from typedefs.models.builtins import BuiltinType
from typedefs.models.entity_def import EntityDef
from typedefs.models.enum_def import EnumDef
from utils.logger import get_logger
from psycopg2 import sql
from indexstore.models import Index

LOGGER = get_logger(__name__)


class PostgresIndexStore:
    def __init__(self, conn: connection):
        self.conn = conn
        LOGGER.info("PostgresIndexStore initialized with connection")

    def init_index(self) -> None:
        LOGGER.info("Initializing index")
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
        LOGGER.info("Index initialized successfully")

    def get_attribute_type_name(self, attribute: AttributeDef) -> str:
        LOGGER.info(f"Getting attribute type name for {attribute.name}")
        match attribute.type:
            case BuiltinType.STRING:
                return f"VARCHAR({attribute.max_length})"
            case BuiltinType.TEXT:
                return f"TEXT"
            case BuiltinType.INT | BuiltinType.FLOAT:
                return f"NUMERIC"
            case BuiltinType.BOOLEAN:
                return f"BOOLEAN"
            case BuiltinType.DATE:
                return f"DATE"
            case BuiltinType.JSON:
                return f"JSONB"
            case BuiltinType.VECTOR:
                return f"VECTOR({attribute.vector_dimensions})"
            case EnumDef():
                return f"VARCHAR(255)"
            case _:
                LOGGER.error(f"Unsupported attribute type: {attribute.type}")
                raise ValueError(f"Unsupported attribute type: {attribute.type}")

    def get_index_creation_stmt(self, attribute: AttributeDef, index_name: str) -> str:
        LOGGER.info(f"Getting index creation statement for {attribute.name}")
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
            case BuiltinType.JSON:
                return f"USING GIN({index_name})"
            case BuiltinType.TEXT:
                return f"USING GIN(to_tsvector('english', {index_name}))"
            case _:
                return f"({index_name})"

    def add_attribute_index(self, entity_def: EntityDef, attribute: AttributeDef) -> None:
        LOGGER.info(f"Adding attribute index for {entity_def.name}.{attribute.name}")
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
            index_stmt=sql.SQL(self.get_index_creation_stmt(attribute, index_name)),
        )

        LOGGER.info(f"Adding index {index_name} to table {entity_def.name}")
        with self.conn.cursor() as cur:
            cur.execute(add_column_stmt)
            cur.execute(create_index_stmt)
            self.conn.commit()
        LOGGER.info(f"Index {index_name} added successfully")

    def generate_index_name(self, entity_def: EntityDef, attribute: AttributeDef) -> str:
        index_name = f"{entity_def.name}_{attribute.name}"
        LOGGER.info(f"Generated index name: {index_name}")
        return index_name

    def attribute_index_exists(self, entity_def: EntityDef, attribute: AttributeDef) -> bool:
        LOGGER.info(f"Checking if index exists for {entity_def.name}.{attribute.name}")
        index_name = self.generate_index_name(entity_def, attribute)
        with self.conn.cursor() as cur:
            cur.execute(f"SELECT EXISTS (SELECT 1 FROM pg_class WHERE relname = '{index_name}');")
            exists = cur.fetchone()[0]
        LOGGER.info(f"Index {'exists' if exists else 'does not exist'}")
        return exists

    def remove_attribute_index(self, entity_def: EntityDef, attribute: AttributeDef) -> None:
        LOGGER.info(f"Removing attribute index for {entity_def.name}.{attribute.name}")
        index_name = self.generate_index_name(entity_def, attribute)
        if not self.attribute_index_exists(entity_def, attribute):
            LOGGER.info(f"Index for {entity_def.name}.{attribute.name} does not exist")
            return

        drop_column_stmt = sql.SQL("""
            ALTER TABLE {table_name}
            DROP COLUMN {index_name};
        """).format(
            table_name=sql.Identifier("attributes_index"),
            index_name=sql.Identifier(index_name),
        )

        drop_index_stmt = sql.SQL("""
            DROP INDEX {index_name};
        """).format(
            index_name=sql.Identifier(index_name),
        )

        LOGGER.info(f"Removing index {index_name} from table {entity_def.name}")
        with self.conn.cursor() as cur:
            cur.execute(drop_column_stmt)
            cur.execute(drop_index_stmt)
            self.conn.commit()
        LOGGER.info(f"Index {index_name} removed successfully")

    def list_indices(self) -> list[Index]:
        LOGGER.info("Listing all indices")
        with self.conn.cursor() as cur:
            cur.execute("SELECT index_name, index_type FROM attributes_index;")
            indices = [Index(index_name=row[0], index_type=row[1]) for row in cur.fetchall()]
        LOGGER.info(f"Found {len(indices)} indices")
        return indices
