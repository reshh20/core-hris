
from sqlalchemy.orm import Session, joinedload
from app.models.employee import Employee
from app.schemas.employee import OrgChartNode


def get_org_chart(db: Session) -> list[OrgChartNode]:
    employees = (
        db.query(Employee)
        .options(
            joinedload(Employee.department),
            joinedload(Employee.position),
        )
        .all()
    )

    if not employees:
        return []

    emp_map = {}
    for emp in employees:
        emp_status = emp.employment_status.value if hasattr(emp.employment_status, 'value') else emp.employment_status
        emp_map[emp.id] = {
            "employee": emp,
            "children": [],
        }

    root_ids = []
    for emp in employees:
        if emp.manager_id is None or emp.manager_id not in emp_map:
            root_ids.append(emp.id)
        else:
            emp_map[emp.manager_id]["children"].append(emp.id)

    def build_node(emp_id: int) -> OrgChartNode:
        entry = emp_map[emp_id]
        emp = entry["employee"]
        children = [build_node(child_id) for child_id in entry["children"]]

        return OrgChartNode(
            id=emp.id,
            employee_id=emp.employee_id,
            first_name=emp.first_name,
            last_name=emp.last_name,
            position_title=emp.position.title if emp.position else None,
            department_name=emp.department.name if emp.department else None,
            profile_image=emp.profile_image,
            manager_id=emp.manager_id,
            children=children,
        )

    return [build_node(root_id) for root_id in root_ids]
