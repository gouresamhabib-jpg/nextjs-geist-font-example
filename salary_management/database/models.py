"""
Data models for Employee Salary Management System
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Employee:
    """Employee data model"""
    id: Optional[int] = None
    name: str = ""
    created_at: Optional[datetime] = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()

@dataclass
class Area:
    """Work area data model"""
    id: Optional[int] = None
    name: str = ""
    created_at: Optional[datetime] = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()

@dataclass
class EmployeeAreaRate:
    """Employee rate per area data model"""
    id: Optional[int] = None
    employee_id: int = 0
    area_id: int = 0
    base_salary: float = 0.0
    created_at: Optional[datetime] = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()

@dataclass
class SalaryRecord:
    """Salary calculation record data model"""
    id: Optional[int] = None
    employee_id: int = 0
    area_id: int = 0
    base_salary: float = 0.0
    allowance: float = 0.0
    total: float = 0.0
    date_created: Optional[datetime] = None
    
    def __post_init__(self):
        if self.date_created is None:
            self.date_created = datetime.now()
        # Calculate total automatically
        self.total = self.base_salary + self.allowance

@dataclass
class SalaryRecordView:
    """Extended salary record with employee and area names for display"""
    id: Optional[int] = None
    employee_name: str = ""
    area_name: str = ""
    base_salary: float = 0.0
    allowance: float = 0.0
    total: float = 0.0
    date_created: Optional[datetime] = None
    employee_id: int = 0
    area_id: int = 0
