from pydantic import BaseModel, Field, ConfigDict
from typing import Optional


class Data(BaseModel):
    model_config = ConfigDict(coerce_numbers_to_str=True)

    data_id: str= Field(alias="id")


class User(BaseModel):
    id: int
    output_data: Optional[Data] = Field(alias="output", default=None)


json = {
    "id": 1,
    "output": {
        "id": 2,
    },
    "tags": ["tag1", "tag2"],
}

user = User(**json)
print(user)
print(user.model_dump(by_alias=True))
