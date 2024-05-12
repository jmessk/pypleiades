from pydantic import BaseModel, Field
from typing import Optional


class Data(BaseModel):
    data_id: int = Field(alias="id")


class User(BaseModel):
    id: int
    output_data: Optional[Data] = Field(alias="output", default=None)


json = {
    "id": 1,
    "output": {
        "id": 2,
    }
}

user = User(**json)
print(user)
