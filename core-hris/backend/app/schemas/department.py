
from pydantic import BaseModel, Field


class DepartmentBase(BaseModel):

    name: str = Field(..., min_length=1, max_length=100, description="Department name")
    description: str | None = Field(None, max_length=500, description="Department description")


class DepartmentCreate(DepartmentBase):

    pass


class DepartmentUpdate(BaseModel):

    name: str | None = Field(None, min_length=1, max_length=100)
    description: str | None = Field(None, max_length=500)


class DepartmentResponse(DepartmentBase):

    id: int

    model_config = {"from_attributes": True}
