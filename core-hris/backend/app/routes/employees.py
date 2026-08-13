
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.employee import (
    EmployeeCreate,
    EmployeeUpdate,
    EmployeeResponse,
    EmployeeListResponse,
)
from app.services import employee_service

router = APIRouter(prefix="/api/employees", tags=["Employees"])


@router.get(
    "",
    response_model=list[EmployeeListResponse],
    summary="Get all employees",
    description="Retrieve all employees with optional search, department, status, and location filters.",
)
def get_employees(
    search: str | None = Query(None, description="Search by name, employee ID, or email"),
    department_id: int | None = Query(None, description="Filter by department ID"),
    status: str | None = Query(None, alias="status", description="Filter by employment status"),
    location: str | None = Query(None, description="Filter by location"),
    db: Session = Depends(get_db),
):
    return employee_service.get_employees(
        db,
        search=search,
        department_id=department_id,
        status_filter=status,
        location=location,
    )


@router.get(
    "/{employee_id}",
    response_model=EmployeeResponse,
    summary="Get employee by ID",
    description="Retrieve a single employee's full details including manager and direct reports.",
)
def get_employee(employee_id: int, db: Session = Depends(get_db)):
    return employee_service.get_employee_by_id(db, employee_id)


@router.post(
    "",
    response_model=EmployeeResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new employee",
    description="Create a new employee record with full validation.",
)
def create_employee(employee_data: EmployeeCreate, db: Session = Depends(get_db)):
    return employee_service.create_employee(db, employee_data)


@router.put(
    "/{employee_id}",
    response_model=EmployeeResponse,
    summary="Update an employee",
    description="Update an existing employee's details.",
)
def update_employee(
    employee_id: int, employee_data: EmployeeUpdate, db: Session = Depends(get_db)
):
    return employee_service.update_employee(db, employee_id, employee_data)


@router.delete(
    "/{employee_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete an employee",
    description="Delete an employee. Fails if the employee has direct reports.",
)
def delete_employee(employee_id: int, db: Session = Depends(get_db)):
    employee_service.delete_employee(db, employee_id)
