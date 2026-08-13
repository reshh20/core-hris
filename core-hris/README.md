# Core HRIS — Simplified Core Employee Management

A full-stack Human Resource Information System (HRIS) built as a modern web application for managing employee directories and organizational hierarchies.

## Overview

Core HRIS is a centralized source of truth for employee information and organizational relationships. It provides HR administrators with a comprehensive view of the workforce through two primary screens:

1. **Employee Directory** — Search, filter, and view detailed employee information
2. **Organization Chart** — Visual representation of the reporting hierarchy

## Features

- **Employee Directory**: View all employees in a searchable, filterable table
- **Employee Search**: Search by name, employee ID, or email
- **Employee Filters**: Filter by department and employment status
- **Employee Profile**: Detailed view with personal, employment, and reporting information
- **Reporting Hierarchy**: See who each employee reports to and their direct reports
- **Organization Chart**: Interactive visual tree built with React Flow (zoom, pan, fit view)
- **Click Navigation**: Navigate between employees through the org chart and profile views
- **Data Validation**: Comprehensive validation at frontend, Pydantic, service, and database layers
- **Business Rules**: Cycle detection, duplicate prevention, dependency protection

## Technology Stack

| Layer | Technology |
|-------|-----------|
| **Frontend** | React, Vite, Tailwind CSS, React Router, Axios, React Flow (@xyflow/react) |
| **Backend** | Python, FastAPI, SQLAlchemy, Pydantic |
| **Local DB** | SQLite |
| **Production DB** | PostgreSQL |
| **Deployment** | Frontend: Vercel, Backend: Render, DB: Neon PostgreSQL |

## Architecture

```
React Frontend (Vite + Tailwind)
      │
      │  Axios REST API
      ▼
FastAPI Backend
      │
      ▼
Pydantic Validation
      │
      ▼
Business Service Layer
      │
      ▼
SQLAlchemy ORM
      │
      ▼
SQLite (local) / PostgreSQL (production)
```

## Database Schema

### Employee
| Field | Type | Constraints |
|-------|------|------------|
| id | Integer | PK, Auto |
| employee_id | String(20) | Unique, Index, Pattern: EMP\d{3,} |
| first_name | String(100) | Required |
| last_name | String(100) | Required |
| email | String(255) | Unique, Index, Valid email |
| phone | String(20) | Required |
| department_id | Integer | FK → departments.id |
| position_id | Integer | FK → positions.id |
| manager_id | Integer | FK → employees.id (nullable) |
| location | String(200) | Required |
| joining_date | Date | Not in future |
| employment_status | Enum | ACTIVE, ON_LEAVE, RESIGNED, TERMINATED |
| profile_image | String(500) | Optional, valid URL |
| created_at | DateTime | Auto |
| updated_at | DateTime | Auto |

### Department
| Field | Type | Constraints |
|-------|------|------------|
| id | Integer | PK, Auto |
| name | String(100) | Unique |
| description | Text | Optional |

### Position
| Field | Type | Constraints |
|-------|------|------------|
| id | Integer | PK, Auto |
| title | String(100) | Unique |
| level | String(50) | Required |

## API Endpoints

### Employees
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/employees` | List all employees (supports ?search, ?department_id, ?status, ?location) |
| GET | `/api/employees/{id}` | Get employee details with manager and direct reports |
| POST | `/api/employees` | Create a new employee |
| PUT | `/api/employees/{id}` | Update an employee |
| DELETE | `/api/employees/{id}` | Delete an employee |

### Departments
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/departments` | List all departments |
| POST | `/api/departments` | Create a department |
| PUT | `/api/departments/{id}` | Update a department |
| DELETE | `/api/departments/{id}` | Delete a department |

### Positions
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/positions` | List all positions |
| POST | `/api/positions` | Create a position |
| PUT | `/api/positions/{id}` | Update a position |
| DELETE | `/api/positions/{id}` | Delete a position |

### Organization
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/org-chart` | Get nested org chart hierarchy |

### Health
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check |
| GET | `/docs` | OpenAPI documentation |

## Validation

- **Employee ID**: Format `EMP` + digits (e.g., EMP001). Must be unique.
- **Email**: Valid email format. Must be unique. Normalized to lowercase.
- **Name**: Letters, spaces, hyphens, apostrophes only. Trimmed.
- **Phone**: Valid phone format (7–20 chars with digits, spaces, hyphens, parens).
- **Joining Date**: Must not be in the future.
- **Employment Status**: Must be ACTIVE, ON_LEAVE, RESIGNED, or TERMINATED.
- **Profile Image**: If provided, must be a valid URL.
- **Foreign Keys**: Department, position, and manager must exist.

## Business Rules

1. Employee ID must be unique
2. Email must be unique
3. Department must exist
4. Position must exist
5. Manager must exist (if specified)
6. Employee cannot be their own manager
7. Circular reporting hierarchies are prevented (cycle detection)
8. Cannot delete a department with assigned employees
9. Cannot delete a position with assigned employees
10. Cannot delete an employee who has direct reports

## Local Setup

### Prerequisites
- Python 3.10+
- Node.js 18+
- npm

### Backend Setup

```bash
cd core-hris/backend

# Create virtual environment (optional but recommended)
python -m venv venv
venv\Scripts\activate    # Windows
# source venv/bin/activate  # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Create .env file
copy .env.example .env

# Start the server
python -m uvicorn app.main:app --reload --port 8000
```

The database is created automatically and seeded with demo data on first run.

### Frontend Setup

```bash
cd core-hris/frontend

# Install dependencies
npm install

# Create .env file
copy .env.example .env

# Start the development server
npm run dev
```

### Access the Application

| Service | URL |
|---------|-----|
| Frontend | http://localhost:5173 |
| Backend API | http://localhost:8000 |
| API Docs | http://localhost:8000/docs |
| Health Check | http://localhost:8000/health |

## Testing

### Backend Tests

```bash
cd core-hris/backend
python -m pytest tests/ -v
```

### Frontend Build

```bash
cd core-hris/frontend
npm run build
```


8. **Chart Navigation** — Click any node → navigate to that employee's profile
9. **API Documentation** — Visit /docs for interactive Swagger UI
