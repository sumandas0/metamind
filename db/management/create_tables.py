import os
import psycopg2
from utils.logger import setup_logger

LOGGER = setup_logger(__name__)


def execute_create_tables(conn: psycopg2.extensions.connection, sql_folder: str) -> None:
    cur = conn.cursor()
    for filename in sorted(os.listdir(sql_folder)):
        if filename.endswith(".sql"):
            file_path = os.path.join(sql_folder, filename)
            LOGGER.info(f"Executing SQL script: {filename}")
            with open(file_path, "r") as f:
                sql_script = f.read()
                # Split the script into individual statements
                cur.execute(sql_script)
    conn.commit()
