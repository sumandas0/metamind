from pydantic import BaseModel


class Index(BaseModel):
    name: str
    type: str
