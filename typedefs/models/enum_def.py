from pydantic import BaseModel
from typing import List


class EnumDef(BaseModel):
    name: str
    values: List[str]
