import os
import psycopg2
from psycopg2 import sql
from psycopg2.extensions import connection
from utils.logger import setup_logger

LOGGER = setup_logger(__name__)

def execute_create_tables(conn: connection, sql_folder: str) -> None:
    """
    Load SQL files from the specified folder and execute them one at a time.
    
    Args:
        conn (connection): Database connection object.
        sql_folder (str): Path to the folder containing SQL files.
    
    Raises:
        Exception: If there's an error during execution of SQL statements.
    """
    sql_files = []

    # Get all SQL files in the specified folder
    for filename in os.listdir(sql_folder):
        if filename.endswith('.sql'):
            sql_files.append(os.path.join(sql_folder, filename))

    try:
        with conn.cursor() as cur:
            for sql_file in sql_files:
                with open(sql_file, 'r') as f:
                    sql_statement = f.read()
                    # Execute each SQL file separately
                    cur.execute(sql_statement)
                    LOGGER.info(f"Executed SQL file: {sql_file}")
        # Commit all changes at the end
        conn.commit()
        LOGGER.info("All SQL statements executed and committed successfully.")
    except Exception as e:
        conn.rollback()
        error_msg = f"Error executing SQL statements: {str(e)}"
        LOGGER.error(error_msg)
        raise Exception(error_msg)
