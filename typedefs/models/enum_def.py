from pydantic import BaseModel
from typing import List


class EnumDef(BaseModel):
    name: str
    description: str
    values: List[str]