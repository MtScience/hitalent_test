from pydantic import BaseModel, Field, model_validator
from typing import Literal, Self


class DeletionQueryParams(BaseModel):
    mode: Literal["cascade", "reassign"]
    reassign_id: int | None = Field(default=None)

    @model_validator(mode="after")
    def validator(self) -> Self:
        if self.reassign_id is None and self.mode == "reassign":
            raise ValueError("reassign_id has to be integer when mode is reassign")
        return self
