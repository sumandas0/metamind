from pydantic import BaseModel
from typing import Optional, Union
from typedefs.models.builtins import BuiltinType
from typedefs.models.enum_def import EnumDef


class AttributeDef(BaseModel):
    name: str
    description: str
    type: Union[BuiltinType, EnumDef]
    default: str
    required: bool

    index: bool
    unique: bool
    default: Optional[str] = None
    min_length: Optional[int] = None  # only for string types
    max_length: Optional[int] = None  # only for string types
    min_value: Optional[float] = None  # only for numeric types
    max_value: Optional[float] = None  # only for numeric types
    vector_dimensions: Optional[int] = None  # only for vector types
