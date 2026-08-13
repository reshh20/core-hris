
from datetime import date
from sqlalchemy.orm import Session

from app.models.department import Department
from app.models.position import Position
from app.models.employee import Employee


def seed_departments(db: Session) -> dict[str, int]:
    departments = [
        {"name": "Executive", "description": "C-suite and executive leadership"},
        {"name": "Engineering", "description": "Software development and technology"},
        {"name": "Quality Assurance", "description": "Software testing and quality control"},
        {"name": "Finance", "description": "Financial planning, accounting, and analysis"},
        {"name": "Human Resources", "description": "Employee relations, recruitment, and HR operations"},
        {"name": "Marketing", "description": "Brand management, campaigns, and market research"},
    ]

    dept_map = {}
    for dept_data in departments:
        dept = Department(**dept_data)
        db.add(dept)
        db.flush()
        dept_map[dept.name] = dept.id

    return dept_map


def seed_positions(db: Session) -> dict[str, int]:
    positions = [
        {"title": "Chief Executive Officer", "level": "C-Level"},
        {"title": "Chief Technology Officer", "level": "C-Level"},
        {"title": "Chief Financial Officer", "level": "C-Level"},
        {"title": "Head of Human Resources", "level": "Director"},
        {"title": "Head of Marketing", "level": "Director"},
        {"title": "Engineering Manager", "level": "Manager"},
        {"title": "QA Manager", "level": "Manager"},
        {"title": "Finance Manager", "level": "Manager"},
        {"title": "HR Manager", "level": "Manager"},
        {"title": "Marketing Manager", "level": "Manager"},
        {"title": "Senior Software Engineer", "level": "Senior"},
        {"title": "Software Engineer", "level": "Mid"},
        {"title": "QA Engineer", "level": "Mid"},
        {"title": "Financial Analyst", "level": "Mid"},
        {"title": "HR Executive", "level": "Mid"},
        {"title": "Marketing Executive", "level": "Mid"},
        {"title": "Software Intern", "level": "Intern"},
    ]

    pos_map = {}
    for pos_data in positions:
        pos = Position(**pos_data)
        db.add(pos)
        db.flush()
        pos_map[pos.title] = pos.id

    return pos_map


def seed_employees(db: Session, dept_map: dict[str, int], pos_map: dict[str, int]):
    employees_data = [
        {
            "employee_id": "EMP001",
            "first_name": "Rajesh",
            "last_name": "Sharma",
            "email": "rajesh.sharma@corehris.com",
            "phone": "+91 9876543210",
            "department": "Executive",
            "position": "Chief Executive Officer",
            "manager_emp_id": None,
            "location": "Mumbai, India",
            "joining_date": date(2018, 1, 15),
            "employment_status": "ACTIVE",
        },
        {
            "employee_id": "EMP002",
            "first_name": "Aisha",
            "last_name": "Patel",
            "email": "aisha.patel@corehris.com",
            "phone": "+91 9876543211",
            "department": "Engineering",
            "position": "Chief Technology Officer",
            "manager_emp_id": "EMP001",
            "location": "Bangalore, India",
            "joining_date": date(2018, 3, 1),
            "employment_status": "ACTIVE",
        },
        {
            "employee_id": "EMP003",
            "first_name": "Vikram",
            "last_name": "Mehta",
            "email": "vikram.mehta@corehris.com",
            "phone": "+91 9876543212",
            "department": "Finance",
            "position": "Chief Financial Officer",
            "manager_emp_id": "EMP001",
            "location": "Mumbai, India",
            "joining_date": date(2018, 2, 10),
            "employment_status": "ACTIVE",
        },
        {
            "employee_id": "EMP004",
            "first_name": "Priya",
            "last_name": "Nair",
            "email": "priya.nair@corehris.com",
            "phone": "+91 9876543213",
            "department": "Human Resources",
            "position": "Head of Human Resources",
            "manager_emp_id": "EMP001",
            "location": "Mumbai, India",
            "joining_date": date(2018, 4, 20),
            "employment_status": "ACTIVE",
        },
        {
            "employee_id": "EMP005",
            "first_name": "Arjun",
            "last_name": "Reddy",
            "email": "arjun.reddy@corehris.com",
            "phone": "+91 9876543214",
            "department": "Marketing",
            "position": "Head of Marketing",
            "manager_emp_id": "EMP001",
            "location": "Hyderabad, India",
            "joining_date": date(2019, 1, 8),
            "employment_status": "ACTIVE",
        },
        {
            "employee_id": "EMP006",
            "first_name": "Sneha",
            "last_name": "Gupta",
            "email": "sneha.gupta@corehris.com",
            "phone": "+91 9876543215",
            "department": "Engineering",
            "position": "Engineering Manager",
            "manager_emp_id": "EMP002",
            "location": "Bangalore, India",
            "joining_date": date(2019, 6, 15),
            "employment_status": "ACTIVE",
        },
        {
            "employee_id": "EMP007",
            "first_name": "Ravi",
            "last_name": "Kumar",
            "email": "ravi.kumar@corehris.com",
            "phone": "+91 9876543216",
            "department": "Quality Assurance",
            "position": "QA Manager",
            "manager_emp_id": "EMP002",
            "location": "Bangalore, India",
            "joining_date": date(2019, 8, 1),
            "employment_status": "ACTIVE",
        },
        {
            "employee_id": "EMP008",
            "first_name": "Deepa",
            "last_name": "Iyer",
            "email": "deepa.iyer@corehris.com",
            "phone": "+91 9876543217",
            "department": "Finance",
            "position": "Finance Manager",
            "manager_emp_id": "EMP003",
            "location": "Mumbai, India",
            "joining_date": date(2019, 9, 12),
            "employment_status": "ACTIVE",
        },
        {
            "employee_id": "EMP009",
            "first_name": "Karthik",
            "last_name": "Menon",
            "email": "karthik.menon@corehris.com",
            "phone": "+91 9876543218",
            "department": "Human Resources",
            "position": "HR Manager",
            "manager_emp_id": "EMP004",
            "location": "Mumbai, India",
            "joining_date": date(2020, 1, 6),
            "employment_status": "ACTIVE",
        },
        {
            "employee_id": "EMP010",
            "first_name": "Meera",
            "last_name": "Joshi",
            "email": "meera.joshi@corehris.com",
            "phone": "+91 9876543219",
            "department": "Marketing",
            "position": "Marketing Manager",
            "manager_emp_id": "EMP005",
            "location": "Hyderabad, India",
            "joining_date": date(2020, 3, 18),
            "employment_status": "ACTIVE",
        },
        {
            "employee_id": "EMP011",
            "first_name": "Ananya",
            "last_name": "Desai",
            "email": "ananya.desai@corehris.com",
            "phone": "+91 9876543220",
            "department": "Engineering",
            "position": "Senior Software Engineer",
            "manager_emp_id": "EMP006",
            "location": "Bangalore, India",
            "joining_date": date(2020, 5, 25),
            "employment_status": "ACTIVE",
        },
        {
            "employee_id": "EMP012",
            "first_name": "Rohit",
            "last_name": "Verma",
            "email": "rohit.verma@corehris.com",
            "phone": "+91 9876543221",
            "department": "Engineering",
            "position": "Software Engineer",
            "manager_emp_id": "EMP006",
            "location": "Pune, India",
            "joining_date": date(2021, 2, 14),
            "employment_status": "ACTIVE",
        },
        {
            "employee_id": "EMP013",
            "first_name": "Neha",
            "last_name": "Singh",
            "email": "neha.singh@corehris.com",
            "phone": "+91 9876543222",
            "department": "Engineering",
            "position": "Software Intern",
            "manager_emp_id": "EMP006",
            "location": "Bangalore, India",
            "joining_date": date(2024, 6, 1),
            "employment_status": "ACTIVE",
        },
        {
            "employee_id": "EMP014",
            "first_name": "Siddharth",
            "last_name": "Rao",
            "email": "siddharth.rao@corehris.com",
            "phone": "+91 9876543223",
            "department": "Quality Assurance",
            "position": "QA Engineer",
            "manager_emp_id": "EMP007",
            "location": "Bangalore, India",
            "joining_date": date(2021, 7, 19),
            "employment_status": "ACTIVE",
        },
        {
            "employee_id": "EMP015",
            "first_name": "Kavita",
            "last_name": "Pillai",
            "email": "kavita.pillai@corehris.com",
            "phone": "+91 9876543224",
            "department": "Finance",
            "position": "Financial Analyst",
            "manager_emp_id": "EMP008",
            "location": "Mumbai, India",
            "joining_date": date(2021, 10, 4),
            "employment_status": "ACTIVE",
        },
        {
            "employee_id": "EMP016",
            "first_name": "Divya",
            "last_name": "Chatterjee",
            "email": "divya.chatterjee@corehris.com",
            "phone": "+91 9876543225",
            "department": "Human Resources",
            "position": "HR Executive",
            "manager_emp_id": "EMP009",
            "location": "Mumbai, India",
            "joining_date": date(2022, 1, 10),
            "employment_status": "ACTIVE",
        },
        {
            "employee_id": "EMP017",
            "first_name": "Amit",
            "last_name": "Banerjee",
            "email": "amit.banerjee@corehris.com",
            "phone": "+91 9876543226",
            "department": "Human Resources",
            "position": "HR Executive",
            "manager_emp_id": "EMP009",
            "location": "Delhi, India",
            "joining_date": date(2022, 4, 18),
            "employment_status": "ON_LEAVE",
        },
        {
            "employee_id": "EMP018",
            "first_name": "Pooja",
            "last_name": "Saxena",
            "email": "pooja.saxena@corehris.com",
            "phone": "+91 9876543227",
            "department": "Marketing",
            "position": "Marketing Executive",
            "manager_emp_id": "EMP010",
            "location": "Hyderabad, India",
            "joining_date": date(2022, 8, 22),
            "employment_status": "ACTIVE",
        },
        {
            "employee_id": "EMP019",
            "first_name": "Suresh",
            "last_name": "Menon",
            "email": "suresh.menon@corehris.com",
            "phone": "+91 9876543228",
            "department": "Engineering",
            "position": "Software Engineer",
            "manager_emp_id": "EMP006",
            "location": "Chennai, India",
            "joining_date": date(2020, 11, 9),
            "employment_status": "RESIGNED",
        },
        {
            "employee_id": "EMP020",
            "first_name": "Lakshmi",
            "last_name": "Narayan",
            "email": "lakshmi.narayan@corehris.com",
            "phone": "+91 9876543229",
            "department": "Quality Assurance",
            "position": "QA Engineer",
            "manager_emp_id": "EMP007",
            "location": "Bangalore, India",
            "joining_date": date(2021, 3, 15),
            "employment_status": "TERMINATED",
        },
    ]

    emp_id_to_db_id = {}
    employee_objects = []

    for emp_data in employees_data:
        employee = Employee(
            employee_id=emp_data["employee_id"],
            first_name=emp_data["first_name"],
            last_name=emp_data["last_name"],
            email=emp_data["email"],
            phone=emp_data["phone"],
            department_id=dept_map[emp_data["department"]],
            position_id=pos_map[emp_data["position"]],
            manager_id=None,  # Set later
            location=emp_data["location"],
            joining_date=emp_data["joining_date"],
            employment_status=emp_data["employment_status"],
        )
        db.add(employee)
        db.flush()
        emp_id_to_db_id[emp_data["employee_id"]] = employee.id
        employee_objects.append((employee, emp_data["manager_emp_id"]))

    for employee, manager_emp_id in employee_objects:
        if manager_emp_id is not None:
            employee.manager_id = emp_id_to_db_id[manager_emp_id]

    db.flush()


def seed_database(db: Session):
    employee_count = db.query(Employee).count()
    if employee_count > 0:
        return

    try:
        dept_map = seed_departments(db)
        pos_map = seed_positions(db)
        seed_employees(db, dept_map, pos_map)
        db.commit()
        print("[OK] Database seeded with demo data successfully.")
    except Exception as e:
        db.rollback()
        print(f"[ERROR] Error seeding database: {e}")
        raise
