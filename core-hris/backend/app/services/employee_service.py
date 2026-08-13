
from datetime import date
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_
from fastapi import HTTPException, status

from app.models.employee import Employee
from app.models.department import Department
from app.models.position import Position
from app.schemas.employee import (
    EmployeeCreate,
    EmployeeUpdate,
    EmployeeResponse,
    EmployeeListResponse,
    ManagerSummary,
    DirectReportSummary,
)


def _build_employee_response(employee: Employee) -> dict:
    manager_summary = None
    if employee.manager:
        manager_summary = ManagerSummary(
            id=employee.manager.id,
            employee_id=employee.manager.employee_id,
            first_name=employee.manager.first_name,
            last_name=employee.manager.last_name,
            profile_image=employee.manager.profile_image,
        )

    direct_reports = []
    for report in employee.direct_reports:
        direct_reports.append(
            DirectReportSummary(
                id=report.id,
                employee_id=report.employee_id,
                first_name=report.first_name,
                last_name=report.last_name,
                position_title=report.position.title if report.position else None,
                profile_image=report.profile_image,
            )
        )

    return EmployeeResponse(
        id=employee.id,
        employee_id=employee.employee_id,
        first_name=employee.first_name,
        last_name=employee.last_name,
        email=employee.email,
        phone=employee.phone,
        department_id=employee.department_id,
        position_id=employee.position_id,
        manager_id=employee.manager_id,
        location=employee.location,
        joining_date=employee.joining_date,
        employment_status=employee.employment_status.value if hasattr(employee.employment_status, 'value') else employee.employment_status,
        profile_image=employee.profile_image,
        created_at=str(employee.created_at) if employee.created_at else None,
        updated_at=str(employee.updated_at) if employee.updated_at else None,
        department=employee.department,
        position=employee.position,
        manager=manager_summary,
        direct_reports=direct_reports,
    )


def get_employees(
    db: Session,
    search: str | None = None,
    department_id: int | None = None,
    status_filter: str | None = None,
    location: str | None = None,
) -> list[EmployeeListResponse]:
    query = db.query(Employee).options(
        joinedload(Employee.department),
        joinedload(Employee.position),
    )

    if search:
        search_term = f"%{search.strip()}%"
        query = query.filter(
            or_(
                Employee.first_name.ilike(search_term),
                Employee.last_name.ilike(search_term),
                Employee.employee_id.ilike(search_term),
                Employee.email.ilike(search_term),
                (Employee.first_name + " " + Employee.last_name).ilike(search_term),
            )
        )

    if department_id is not None:
        query = query.filter(Employee.department_id == department_id)

    if status_filter:
        query = query.filter(Employee.employment_status == status_filter)

    if location:
        query = query.filter(Employee.location.ilike(f"%{location.strip()}%"))

    employees = query.order_by(Employee.employee_id).all()

    result = []
    for emp in employees:
        emp_status = emp.employment_status.value if hasattr(emp.employment_status, 'value') else emp.employment_status
        result.append(
            EmployeeListResponse(
                id=emp.id,
                employee_id=emp.employee_id,
                first_name=emp.first_name,
                last_name=emp.last_name,
                email=emp.email,
                phone=emp.phone,
                location=emp.location,
                joining_date=emp.joining_date,
                employment_status=emp_status,
                profile_image=emp.profile_image,
                department=emp.department,
                position=emp.position,
            )
        )
    return result


def get_employee_by_id(db: Session, employee_db_id: int) -> EmployeeResponse:
    employee = (
        db.query(Employee)
        .options(
            joinedload(Employee.department),
            joinedload(Employee.position),
            joinedload(Employee.manager),
            joinedload(Employee.direct_reports).joinedload(Employee.position),
        )
        .filter(Employee.id == employee_db_id)
        .first()
    )

    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"success": False, "message": "Employee not found", "field": "id"},
        )

    return _build_employee_response(employee)


def _validate_foreign_keys(
    db: Session,
    department_id: int,
    position_id: int,
    manager_id: int | None,
    current_employee_id: int | None = None,
):
    department = db.query(Department).filter(Department.id == department_id).first()
    if not department:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"success": False, "message": "Department not found", "field": "department_id"},
        )

    position = db.query(Position).filter(Position.id == position_id).first()
    if not position:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"success": False, "message": "Position not found", "field": "position_id"},
        )

    if manager_id is not None:
        if current_employee_id is not None and manager_id == current_employee_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "success": False,
                    "message": "Employee cannot be their own manager",
                    "field": "manager_id",
                },
            )

        manager = db.query(Employee).filter(Employee.id == manager_id).first()
        if not manager:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"success": False, "message": "Manager not found", "field": "manager_id"},
            )


def _detect_circular_hierarchy(db: Session, employee_id: int, new_manager_id: int) -> bool:
    visited = {employee_id}
    current_id = new_manager_id

    while current_id is not None:
        if current_id in visited:
            return True
        visited.add(current_id)
        manager = db.query(Employee).filter(Employee.id == current_id).first()
        if manager is None:
            break
        current_id = manager.manager_id

    return False


def _check_unique_employee_id(db: Session, employee_id_str: str, exclude_id: int | None = None):
    query = db.query(Employee).filter(Employee.employee_id == employee_id_str)
    if exclude_id is not None:
        query = query.filter(Employee.id != exclude_id)
    existing = query.first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={
                "success": False,
                "message": "Employee ID already exists",
                "field": "employee_id",
            },
        )


def _check_unique_email(db: Session, email: str, exclude_id: int | None = None):
    query = db.query(Employee).filter(Employee.email == email.lower())
    if exclude_id is not None:
        query = query.filter(Employee.id != exclude_id)
    existing = query.first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={
                "success": False,
                "message": "Employee email already exists",
                "field": "email",
            },
        )


def create_employee(db: Session, employee_data: EmployeeCreate) -> EmployeeResponse:
    _check_unique_employee_id(db, employee_data.employee_id)
    _check_unique_email(db, employee_data.email)

    _validate_foreign_keys(
        db,
        employee_data.department_id,
        employee_data.position_id,
        employee_data.manager_id,
    )

    employee = Employee(
        employee_id=employee_data.employee_id,
        first_name=employee_data.first_name,
        last_name=employee_data.last_name,
        email=employee_data.email.lower(),
        phone=employee_data.phone,
        department_id=employee_data.department_id,
        position_id=employee_data.position_id,
        manager_id=employee_data.manager_id,
        location=employee_data.location,
        joining_date=employee_data.joining_date,
        employment_status=employee_data.employment_status,
        profile_image=employee_data.profile_image,
    )

    db.add(employee)
    db.commit()
    db.refresh(employee)

    return get_employee_by_id(db, employee.id)


def update_employee(
    db: Session, employee_db_id: int, employee_data: EmployeeUpdate
) -> EmployeeResponse:
    employee = db.query(Employee).filter(Employee.id == employee_db_id).first()
    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"success": False, "message": "Employee not found", "field": "id"},
        )

    update_dict = employee_data.model_dump(exclude_unset=True)

    if "employee_id" in update_dict and update_dict["employee_id"] != employee.employee_id:
        _check_unique_employee_id(db, update_dict["employee_id"], exclude_id=employee.id)

    if "email" in update_dict and update_dict["email"].lower() != employee.email:
        _check_unique_email(db, update_dict["email"], exclude_id=employee.id)
        update_dict["email"] = update_dict["email"].lower()

    dept_id = update_dict.get("department_id", employee.department_id)
    pos_id = update_dict.get("position_id", employee.position_id)
    mgr_id = update_dict.get("manager_id", employee.manager_id)

    _validate_foreign_keys(db, dept_id, pos_id, mgr_id, current_employee_id=employee.id)

    if "manager_id" in update_dict and mgr_id is not None:
        if _detect_circular_hierarchy(db, employee.id, mgr_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "success": False,
                    "message": "This manager assignment would create a circular reporting relationship",
                    "field": "manager_id",
                },
            )

    for key, value in update_dict.items():
        setattr(employee, key, value)

    db.commit()
    db.refresh(employee)

    return get_employee_by_id(db, employee.id)


def delete_employee(db: Session, employee_db_id: int) -> None:
    employee = db.query(Employee).filter(Employee.id == employee_db_id).first()
    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"success": False, "message": "Employee not found", "field": "id"},
        )

    direct_reports = (
        db.query(Employee).filter(Employee.manager_id == employee.id).count()
    )
    if direct_reports > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "success": False,
                "message": f"Cannot delete employee with {direct_reports} direct report(s). Reassign them first.",
                "field": "id",
            },
        )

    db.delete(employee)
    db.commit()
