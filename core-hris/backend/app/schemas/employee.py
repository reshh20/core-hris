
import re
from datetime import date
from pydantic import BaseModel, Field, field_validator, EmailStr
from app.schemas.department import DepartmentResponse
from app.schemas.position import PositionResponse


EMPLOYEE_ID_PATTERN = re.compile(r"^EMP\d{3,}$")
PHONE_PATTERN = re.compile(r"^\+?[\d\s\-()]{7,20}$")
NAME_PATTERN = re.compile(r"^[a-zA-Z\s\-'.]+$")
URL_PATTERN = re.compile(
    r"^https?://"
    r"(?:[a-zA-Z0-9\-._~:/?#\[\]@!$&'()*+,;=%])+"
    r"$"
)

VALID_STATUSES = {"ACTIVE", "ON_LEAVE", "RESIGNED", "TERMINATED"}


class EmployeeBase(BaseModel):

    employee_id: str = Field(
        ..., description="Unique employee identifier (format: EMP followed by digits, e.g., EMP001)"
    )
    first_name: str = Field(..., min_length=1, max_length=100, description="Employee first name")
    last_name: str = Field(..., min_length=1, max_length=100, description="Employee last name")
    email: EmailStr = Field(..., description="Employee email address")
    phone: str = Field(..., min_length=7, max_length=20, description="Employee phone number")
    department_id: int = Field(..., gt=0, description="Department ID")
    position_id: int = Field(..., gt=0, description="Position ID")
    manager_id: int | None = Field(None, description="Manager's employee record ID (null for top-level)")
    location: str = Field(..., min_length=1, max_length=200, description="Employee work location")
    joining_date: date = Field(..., description="Date the employee joined")
    employment_status: str = Field(
        ..., description="Employment status: ACTIVE, ON_LEAVE, RESIGNED, or TERMINATED"
    )
    profile_image: str | None = Field(None, max_length=500, description="Profile image URL")

    @field_validator("employee_id")
    @classmethod
    def validate_employee_id(cls, v: str) -> str:
        if not EMPLOYEE_ID_PATTERN.match(v):
            raise ValueError(
                "Employee ID must follow the format EMP followed by digits (e.g., EMP001)"
            )
        return v

    @field_validator("first_name", "last_name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("Name cannot be empty or only whitespace")
        if not NAME_PATTERN.match(v):
            raise ValueError("Name must contain only letters, spaces, hyphens, apostrophes, or periods")
        return v

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, v: str) -> str:
        v = v.strip()
        if not PHONE_PATTERN.match(v):
            raise ValueError("Invalid phone number format")
        return v

    @field_validator("location")
    @classmethod
    def validate_location(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("Location cannot be empty or only whitespace")
        return v

    @field_validator("joining_date")
    @classmethod
    def validate_joining_date(cls, v: date) -> date:
        if v > date.today():
            raise ValueError("Joining date cannot be in the future")
        return v

    @field_validator("employment_status")
    @classmethod
    def validate_employment_status(cls, v: str) -> str:
        v = v.upper().strip()
        if v not in VALID_STATUSES:
            raise ValueError(
                f"Employment status must be one of: {', '.join(sorted(VALID_STATUSES))}"
            )
        return v

    @field_validator("profile_image")
    @classmethod
    def validate_profile_image(cls, v: str | None) -> str | None:
        if v is not None:
            v = v.strip()
            if v and not URL_PATTERN.match(v):
                raise ValueError("Profile image must be a valid URL starting with http:// or https://")
            if not v:
                return None
        return v


class EmployeeCreate(EmployeeBase):

    pass


class EmployeeUpdate(BaseModel):

    employee_id: str | None = Field(None)
    first_name: str | None = Field(None, min_length=1, max_length=100)
    last_name: str | None = Field(None, min_length=1, max_length=100)
    email: EmailStr | None = Field(None)
    phone: str | None = Field(None, min_length=7, max_length=20)
    department_id: int | None = Field(None, gt=0)
    position_id: int | None = Field(None, gt=0)
    manager_id: int | None = Field(None)
    location: str | None = Field(None, min_length=1, max_length=200)
    joining_date: date | None = Field(None)
    employment_status: str | None = Field(None)
    profile_image: str | None = Field(None, max_length=500)

    @field_validator("employee_id")
    @classmethod
    def validate_employee_id(cls, v: str | None) -> str | None:
        if v is not None and not EMPLOYEE_ID_PATTERN.match(v):
            raise ValueError(
                "Employee ID must follow the format EMP followed by digits (e.g., EMP001)"
            )
        return v

    @field_validator("first_name", "last_name")
    @classmethod
    def validate_name(cls, v: str | None) -> str | None:
        if v is not None:
            v = v.strip()
            if not v:
                raise ValueError("Name cannot be empty or only whitespace")
            if not NAME_PATTERN.match(v):
                raise ValueError("Name must contain only letters, spaces, hyphens, apostrophes, or periods")
        return v

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, v: str | None) -> str | None:
        if v is not None:
            v = v.strip()
            if not PHONE_PATTERN.match(v):
                raise ValueError("Invalid phone number format")
        return v

    @field_validator("location")
    @classmethod
    def validate_location(cls, v: str | None) -> str | None:
        if v is not None:
            v = v.strip()
            if not v:
                raise ValueError("Location cannot be empty or only whitespace")
        return v

    @field_validator("joining_date")
    @classmethod
    def validate_joining_date(cls, v: date | None) -> date | None:
        if v is not None and v > date.today():
            raise ValueError("Joining date cannot be in the future")
        return v

    @field_validator("employment_status")
    @classmethod
    def validate_employment_status(cls, v: str | None) -> str | None:
        if v is not None:
            v = v.upper().strip()
            if v not in VALID_STATUSES:
                raise ValueError(
                    f"Employment status must be one of: {', '.join(sorted(VALID_STATUSES))}"
                )
        return v

    @field_validator("profile_image")
    @classmethod
    def validate_profile_image(cls, v: str | None) -> str | None:
        if v is not None:
            v = v.strip()
            if v and not URL_PATTERN.match(v):
                raise ValueError("Profile image must be a valid URL starting with http:// or https://")
            if not v:
                return None
        return v


class ManagerSummary(BaseModel):

    id: int
    employee_id: str
    first_name: str
    last_name: str
    profile_image: str | None = None

    model_config = {"from_attributes": True}


class DirectReportSummary(BaseModel):

    id: int
    employee_id: str
    first_name: str
    last_name: str
    position_title: str | None = None
    profile_image: str | None = None


class EmployeeResponse(BaseModel):

    id: int
    employee_id: str
    first_name: str
    last_name: str
    email: str
    phone: str
    department_id: int
    position_id: int
    manager_id: int | None = None
    location: str
    joining_date: date
    employment_status: str
    profile_image: str | None = None
    created_at: str | None = None
    updated_at: str | None = None
    department: DepartmentResponse | None = None
    position: PositionResponse | None = None
    manager: ManagerSummary | None = None
    direct_reports: list[DirectReportSummary] = []

    model_config = {"from_attributes": True}


class EmployeeListResponse(BaseModel):

    id: int
    employee_id: str
    first_name: str
    last_name: str
    email: str
    phone: str
    location: str
    joining_date: date
    employment_status: str
    profile_image: str | None = None
    department: DepartmentResponse | None = None
    position: PositionResponse | None = None

    model_config = {"from_attributes": True}


class EmployeePaginatedResponse(BaseModel):
    items: list[EmployeeListResponse]
    total: int
    page: int
    per_page: int
    total_pages: int



class OrgChartNode(BaseModel):

    id: int
    employee_id: str
    first_name: str
    last_name: str
    position_title: str | None = None
    department_name: str | None = None
    profile_image: str | None = None
    manager_id: int | None = None
    children: list["OrgChartNode"] = []
