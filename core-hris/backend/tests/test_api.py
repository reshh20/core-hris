
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base, get_db
from app.main import app

TEST_DATABASE_URL = "sqlite:///./test_hris.db"
engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


client = TestClient(app)



def create_seed_data():
    dept_res = client.post("/api/departments", json={"name": "Engineering", "description": "Tech"})
    assert dept_res.status_code == 201
    dept_id = dept_res.json()["id"]

    dept_res2 = client.post("/api/departments", json={"name": "Finance", "description": "Money"})
    assert dept_res2.status_code == 201

    pos_res = client.post("/api/positions", json={"title": "Software Engineer", "level": "Mid"})
    assert pos_res.status_code == 201
    pos_id = pos_res.json()["id"]

    pos_res2 = client.post("/api/positions", json={"title": "Engineering Manager", "level": "Manager"})
    assert pos_res2.status_code == 201

    return dept_id, pos_id


def create_employee(employee_id="EMP001", email="test@example.com", dept_id=None, pos_id=None, manager_id=None):
    if dept_id is None or pos_id is None:
        dept_id, pos_id = create_seed_data()
    return client.post("/api/employees", json={
        "employee_id": employee_id,
        "first_name": "John",
        "last_name": "Doe",
        "email": email,
        "phone": "+91 9876543210",
        "department_id": dept_id,
        "position_id": pos_id,
        "manager_id": manager_id,
        "location": "Mumbai, India",
        "joining_date": "2023-01-15",
        "employment_status": "ACTIVE",
    }), dept_id, pos_id



def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"



def test_get_employees_empty():
    response = client.get("/api/employees")
    assert response.status_code == 200
    assert response.json() == []


def test_create_valid_employee():
    res, _, _ = create_employee()
    assert res.status_code == 201
    data = res.json()
    assert data["employee_id"] == "EMP001"
    assert data["first_name"] == "John"
    assert data["email"] == "test@example.com"


def test_get_employees():
    create_employee()
    response = client.get("/api/employees")
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_get_employee_by_id():
    res, _, _ = create_employee()
    emp_id = res.json()["id"]
    response = client.get(f"/api/employees/{emp_id}")
    assert response.status_code == 200
    assert response.json()["employee_id"] == "EMP001"


def test_employee_not_found():
    response = client.get("/api/employees/9999")
    assert response.status_code == 404


def test_invalid_employee_id_format():
    dept_id, pos_id = create_seed_data()
    response = client.post("/api/employees", json={
        "employee_id": "emp001",
        "first_name": "Jane",
        "last_name": "Doe",
        "email": "jane@example.com",
        "phone": "+91 9876543210",
        "department_id": dept_id,
        "position_id": pos_id,
        "location": "Mumbai",
        "joining_date": "2023-01-15",
        "employment_status": "ACTIVE",
    })
    assert response.status_code == 422


def test_invalid_email():
    dept_id, pos_id = create_seed_data()
    response = client.post("/api/employees", json={
        "employee_id": "EMP001",
        "first_name": "Jane",
        "last_name": "Doe",
        "email": "invalid-email",
        "phone": "+91 9876543210",
        "department_id": dept_id,
        "position_id": pos_id,
        "location": "Mumbai",
        "joining_date": "2023-01-15",
        "employment_status": "ACTIVE",
    })
    assert response.status_code == 422


def test_duplicate_employee_id():
    res, dept_id, pos_id = create_employee()
    assert res.status_code == 201

    response = client.post("/api/employees", json={
        "employee_id": "EMP001",
        "first_name": "Jane",
        "last_name": "Smith",
        "email": "jane@example.com",
        "phone": "+91 9876543211",
        "department_id": dept_id,
        "position_id": pos_id,
        "location": "Delhi",
        "joining_date": "2023-02-01",
        "employment_status": "ACTIVE",
    })
    assert response.status_code == 409


def test_duplicate_email():
    res, dept_id, pos_id = create_employee()
    assert res.status_code == 201

    response = client.post("/api/employees", json={
        "employee_id": "EMP002",
        "first_name": "Jane",
        "last_name": "Smith",
        "email": "test@example.com",
        "phone": "+91 9876543211",
        "department_id": dept_id,
        "position_id": pos_id,
        "location": "Delhi",
        "joining_date": "2023-02-01",
        "employment_status": "ACTIVE",
    })
    assert response.status_code == 409


def test_invalid_department():
    _, pos_id = create_seed_data()
    response = client.post("/api/employees", json={
        "employee_id": "EMP001",
        "first_name": "John",
        "last_name": "Doe",
        "email": "john@example.com",
        "phone": "+91 9876543210",
        "department_id": 9999,
        "position_id": pos_id,
        "location": "Mumbai",
        "joining_date": "2023-01-15",
        "employment_status": "ACTIVE",
    })
    assert response.status_code == 400


def test_invalid_position():
    dept_id, _ = create_seed_data()
    response = client.post("/api/employees", json={
        "employee_id": "EMP001",
        "first_name": "John",
        "last_name": "Doe",
        "email": "john@example.com",
        "phone": "+91 9876543210",
        "department_id": dept_id,
        "position_id": 9999,
        "location": "Mumbai",
        "joining_date": "2023-01-15",
        "employment_status": "ACTIVE",
    })
    assert response.status_code == 400


def test_invalid_manager():
    dept_id, pos_id = create_seed_data()
    response = client.post("/api/employees", json={
        "employee_id": "EMP001",
        "first_name": "John",
        "last_name": "Doe",
        "email": "john@example.com",
        "phone": "+91 9876543210",
        "department_id": dept_id,
        "position_id": pos_id,
        "manager_id": 9999,
        "location": "Mumbai",
        "joining_date": "2023-01-15",
        "employment_status": "ACTIVE",
    })
    assert response.status_code == 400


def test_self_manager():
    res, dept_id, pos_id = create_employee()
    emp_id = res.json()["id"]

    response = client.put(f"/api/employees/{emp_id}", json={
        "manager_id": emp_id,
    })
    assert response.status_code == 400


def test_circular_hierarchy():
    dept_id, pos_id = create_seed_data()

    res_a = client.post("/api/employees", json={
        "employee_id": "EMP001",
        "first_name": "Alice",
        "last_name": "A",
        "email": "alice@example.com",
        "phone": "+91 9876543210",
        "department_id": dept_id,
        "position_id": pos_id,
        "location": "Mumbai",
        "joining_date": "2023-01-01",
        "employment_status": "ACTIVE",
    })
    a_id = res_a.json()["id"]

    res_b = client.post("/api/employees", json={
        "employee_id": "EMP002",
        "first_name": "Bob",
        "last_name": "B",
        "email": "bob@example.com",
        "phone": "+91 9876543211",
        "department_id": dept_id,
        "position_id": pos_id,
        "manager_id": a_id,
        "location": "Mumbai",
        "joining_date": "2023-01-01",
        "employment_status": "ACTIVE",
    })
    b_id = res_b.json()["id"]

    res_c = client.post("/api/employees", json={
        "employee_id": "EMP003",
        "first_name": "Charlie",
        "last_name": "C",
        "email": "charlie@example.com",
        "phone": "+91 9876543212",
        "department_id": dept_id,
        "position_id": pos_id,
        "manager_id": b_id,
        "location": "Mumbai",
        "joining_date": "2023-01-01",
        "employment_status": "ACTIVE",
    })
    c_id = res_c.json()["id"]

    response = client.put(f"/api/employees/{a_id}", json={
        "manager_id": c_id,
    })
    assert response.status_code == 400
    assert "circular" in response.json()["detail"]["message"].lower()


def test_invalid_employment_status():
    dept_id, pos_id = create_seed_data()
    response = client.post("/api/employees", json={
        "employee_id": "EMP001",
        "first_name": "John",
        "last_name": "Doe",
        "email": "john@example.com",
        "phone": "+91 9876543210",
        "department_id": dept_id,
        "position_id": pos_id,
        "location": "Mumbai",
        "joining_date": "2023-01-15",
        "employment_status": "INVALID_STATUS",
    })
    assert response.status_code == 422


def test_future_joining_date():
    dept_id, pos_id = create_seed_data()
    response = client.post("/api/employees", json={
        "employee_id": "EMP001",
        "first_name": "John",
        "last_name": "Doe",
        "email": "john@example.com",
        "phone": "+91 9876543210",
        "department_id": dept_id,
        "position_id": pos_id,
        "location": "Mumbai",
        "joining_date": "2099-12-31",
        "employment_status": "ACTIVE",
    })
    assert response.status_code == 422


def test_org_chart_empty():
    response = client.get("/api/org-chart")
    assert response.status_code == 200
    assert response.json() == []


def test_org_chart_with_data():
    dept_id, pos_id = create_seed_data()

    res_ceo = client.post("/api/employees", json={
        "employee_id": "EMP001",
        "first_name": "Boss",
        "last_name": "CEO",
        "email": "ceo@example.com",
        "phone": "+91 9876543210",
        "department_id": dept_id,
        "position_id": pos_id,
        "location": "Mumbai",
        "joining_date": "2020-01-01",
        "employment_status": "ACTIVE",
    })
    ceo_id = res_ceo.json()["id"]

    client.post("/api/employees", json={
        "employee_id": "EMP002",
        "first_name": "Dev",
        "last_name": "Engineer",
        "email": "dev@example.com",
        "phone": "+91 9876543211",
        "department_id": dept_id,
        "position_id": pos_id,
        "manager_id": ceo_id,
        "location": "Mumbai",
        "joining_date": "2020-06-01",
        "employment_status": "ACTIVE",
    })

    response = client.get("/api/org-chart")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["first_name"] == "Boss"
    assert len(data[0]["children"]) == 1
    assert data[0]["children"][0]["first_name"] == "Dev"


def test_delete_employee_with_reports():
    dept_id, pos_id = create_seed_data()

    res_mgr = client.post("/api/employees", json={
        "employee_id": "EMP001",
        "first_name": "Manager",
        "last_name": "Boss",
        "email": "manager@example.com",
        "phone": "+91 9876543210",
        "department_id": dept_id,
        "position_id": pos_id,
        "location": "Mumbai",
        "joining_date": "2020-01-01",
        "employment_status": "ACTIVE",
    })
    mgr_id = res_mgr.json()["id"]

    client.post("/api/employees", json={
        "employee_id": "EMP002",
        "first_name": "Report",
        "last_name": "Employee",
        "email": "report@example.com",
        "phone": "+91 9876543211",
        "department_id": dept_id,
        "position_id": pos_id,
        "manager_id": mgr_id,
        "location": "Mumbai",
        "joining_date": "2020-06-01",
        "employment_status": "ACTIVE",
    })

    response = client.delete(f"/api/employees/{mgr_id}")
    assert response.status_code == 400


def test_search_employees():
    create_employee(employee_id="EMP001", email="john@example.com")
    response = client.get("/api/employees?search=John")
    assert response.status_code == 200
    assert len(response.json()) == 1
