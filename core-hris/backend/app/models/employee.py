
from sqlalchemy import (
    Column, Integer, String, Date, DateTime, ForeignKey, Enum as SAEnum, Index
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.database import Base


class EmploymentStatus(enum.Enum):

    ACTIVE = "ACTIVE"
    ON_LEAVE = "ON_LEAVE"
    RESIGNED = "RESIGNED"
    TERMINATED = "TERMINATED"


class Employee(Base):

    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    employee_id = Column(String(20), nullable=False, unique=True, index=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(255), nullable=False, unique=True, index=True)
    phone = Column(String(20), nullable=False)
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=False)
    position_id = Column(Integer, ForeignKey("positions.id"), nullable=False)
    manager_id = Column(Integer, ForeignKey("employees.id"), nullable=True)
    location = Column(String(200), nullable=False)
    joining_date = Column(Date, nullable=False)
    employment_status = Column(
        SAEnum(EmploymentStatus, values_callable=lambda x: [e.value for e in x]),
        nullable=False,
        default=EmploymentStatus.ACTIVE,
    )
    profile_image = Column(String(500), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    department = relationship("Department", back_populates="employees")
    position = relationship("Position", back_populates="employees")
    manager = relationship(
        "Employee", remote_side=[id], back_populates="direct_reports"
    )
    direct_reports = relationship(
        "Employee", back_populates="manager", cascade="all"
    )

    __table_args__ = (
        Index("ix_employees_department_id", "department_id"),
        Index("ix_employees_manager_id", "manager_id"),
        Index("ix_employees_status", "employment_status"),
    )

    def __repr__(self):
        return (
            f"<Employee(id={self.id}, employee_id='{self.employee_id}', "
            f"name='{self.first_name} {self.last_name}')>"
        )
