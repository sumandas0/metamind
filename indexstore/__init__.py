import configparser
import os
import psycopg2

from indexstore.index_store import IndexStore
from indexstore.postgres import PostgresIndexStore


def get_index_store() -> IndexStore:
    index_config = configparser.ConfigParser()
    index_config.read("index.config")
    match index_config["Index"]["store"]:
        case "postgres":
            conn_string = os.getenv("PG_CONN_STR")
            conn = psycopg2.connect(conn_string)
            return PostgresIndexStore(conn)
        case _:
            raise ValueError(f"Invalid index store type: {index_config['Index']['store']}")
