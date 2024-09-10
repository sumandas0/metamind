from psycopg2.extensions import connection
from psycopg2 import sql


def definition_exists(conn: connection, name: str) -> bool:
    with conn.cursor() as cur:
        sql_stmt = sql.SQL(
            """
            SELECT EXISTS (SELECT 1 FROM type_defs WHERE name = {name})
            """
        ).format(name=sql.Literal(name))
        cur.execute(sql_stmt)
        row = cur.fetchone()
        if row:
            return row[0] is True
        else:
            return False
