from enum import Enum, auto


class BuiltinType(Enum):
    INT: str = "int"
    FLOAT: str = "float"
    STRING: str = "string"
    TEXT: str = "text"
    VECTOR: str = "vector"
    BOOLEAN: str = "boolean"
    DATE: str = "date"
    JSON: str = "json"
