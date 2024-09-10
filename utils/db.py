from typing import Dict, Any, Tuple


def row_to_dict(row: Tuple[Any, ...]) -> Dict[str, Any]:
    """
    Convert a psycopg2 row to a dictionary.

    Args:
        row: A psycopg2 row object (tuple of values).

    Returns:
        A dictionary where keys are column names and values are row values.
    """
    return {col.name: value for col, value in zip(row.cursor_description, row)}
