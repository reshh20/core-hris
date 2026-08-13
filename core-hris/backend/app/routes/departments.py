
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.department import Department
from app.models.employee import Employee
from app.schemas.department import DepartmentCreate, DepartmentUpdate, DepartmentResponse

router = APIRouter(prefix="/api/departments", tags=["Departments"])


@router.get(
    "",
    response_model=list[DepartmentResponse],
    summary="Get all departments",
    description="Retrieve all departments in the organization.",
)
def get_departments(db: Session = Depends(get_db)):
    return db.query(Department).order_by(Department.name).all()


@router.post(
    "",
    response_model=DepartmentResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new department",
)
def create_department(dept_data: DepartmentCreate, db: Session = Depends(get_db)):
    existing = db.query(Department).filter(Department.name == dept_data.name).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={"success": False, "message": "Department name already exists", "field": "name"},
        )
    department = Department(name=dept_data.name, description=dept_data.description)
    db.add(department)
    db.commit()
    db.refresh(department)
    return department


@router.put(
    "/{department_id}",
    response_model=DepartmentResponse,
    summary="Update a department",
)
def update_department(
    department_id: int, dept_data: DepartmentUpdate, db: Session = Depends(get_db)
):
    department = db.query(Department).filter(Department.id == department_id).first()
    if not department:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"success": False, "message": "Department not found", "field": "id"},
        )

    update_dict = dept_data.model_dump(exclude_unset=True)

    if "name" in update_dict:
        existing = (
            db.query(Department)
            .filter(Department.name == update_dict["name"], Department.id != department_id)
            .first()
        )
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={"success": False, "message": "Department name already exists", "field": "name"},
            )

    for key, value in update_dict.items():
        setattr(department, key, value)

    db.commit()
    db.refresh(department)
    return department


@router.delete(
    "/{department_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a department",
    description="Delete a department. Fails if employees are assigned to it.",
)
def delete_department(department_id: int, db: Session = Depends(get_db)):
    department = db.query(Department).filter(Department.id == department_id).first()
    if not department:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"success": False, "message": "Department not found", "field": "id"},
        )

    employee_count = db.query(Employee).filter(Employee.department_id == department_id).count()
    if employee_count > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "success": False,
                "message": f"Cannot delete department with {employee_count} employee(s). Reassign them first.",
                "field": "id",
            },
        )

    db.delete(department)
    db.commit()
