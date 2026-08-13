
from pydantic import BaseModel, Field


class PositionBase(BaseModel):

    title: str = Field(..., min_length=1, max_length=100, description="Position title")
    level: str = Field(..., min_length=1, max_length=50, description="Position level (e.g., C-Level, Senior, Mid, Junior, Intern)")


class PositionCreate(PositionBase):

    pass


class PositionUpdate(BaseModel):

    title: str | None = Field(None, min_length=1, max_length=100)
    level: str | None = Field(None, min_length=1, max_length=50)


class PositionResponse(PositionBase):

    id: int

    model_config = {"from_attributes": True}
