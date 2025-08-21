"""
Database manager for Employee Salary Management System
Handles all database operations using SQLite
"""

import sqlite3
import os
from datetime import datetime
from typing import List, Optional, Tuple
from .models import Employee, Area, EmployeeAreaRate, SalaryRecord, SalaryRecordView

class DatabaseManager:
    """Manages all database operations"""
    
    def __init__(self, db_path: str = None):
        """Initialize database manager"""
        if db_path is None:
            # Create data directory if it doesn't exist
            data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
            os.makedirs(data_dir, exist_ok=True)
            db_path = os.path.join(data_dir, 'salary_management.db')
        
        self.db_path = db_path
        self.connection = None
    
    def get_connection(self) -> sqlite3.Connection:
        """Get database connection"""
        if self.connection is None:
            self.connection = sqlite3.connect(self.db_path)
            self.connection.row_factory = sqlite3.Row
        return self.connection
    
    def close_connection(self):
        """Close database connection"""
        if self.connection:
            self.connection.close()
            self.connection = None
    
    def initialize_database(self):
        """Create database tables if they don't exist"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Create employees table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS employees (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create areas table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS areas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create employee_area_rates table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS employee_area_rates (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                employee_id INTEGER NOT NULL,
                area_id INTEGER NOT NULL,
                base_salary REAL NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (employee_id) REFERENCES employees (id) ON DELETE CASCADE,
                FOREIGN KEY (area_id) REFERENCES areas (id) ON DELETE CASCADE,
                UNIQUE(employee_id, area_id)
            )
        ''')
        
        # Create salary_records table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS salary_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                employee_id INTEGER NOT NULL,
                area_id INTEGER NOT NULL,
                base_salary REAL NOT NULL,
                allowance REAL DEFAULT 0,
                total REAL NOT NULL,
                date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (employee_id) REFERENCES employees (id) ON DELETE CASCADE,
                FOREIGN KEY (area_id) REFERENCES areas (id) ON DELETE CASCADE
            )
        ''')
        
        conn.commit()
        
        # Add sample data if tables are empty
        self._add_sample_data()
    
    def _add_sample_data(self):
        """Add sample data if database is empty"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Check if we have any employees
        cursor.execute("SELECT COUNT(*) FROM employees")
        if cursor.fetchone()[0] == 0:
            # Add sample employees
            sample_employees = ["أحمد محمد", "فاطمة علي", "محمود حسن", "نور الدين"]
            for name in sample_employees:
                self.add_employee(Employee(name=name))
            
            # Add sample areas
            sample_areas = ["القاهرة", "الجيزة", "الإسكندرية", "المنصورة"]
            for name in sample_areas:
                self.add_area(Area(name=name))
            
            # Add sample rates
            employees = self.get_all_employees()
            areas = self.get_all_areas()
            
            base_rates = [3000, 3500, 4000, 4500]  # Different base rates
            
            for i, employee in enumerate(employees):
                for j, area in enumerate(areas):
                    # Each employee has different rate per area
                    rate = base_rates[i] + (j * 200)  # Variation per area
                    self.add_employee_area_rate(EmployeeAreaRate(
                        employee_id=employee.id,
                        area_id=area.id,
                        base_salary=rate
                    ))
    
    # Employee operations
    def add_employee(self, employee: Employee) -> int:
        """Add new employee"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            "INSERT INTO employees (name) VALUES (?)",
            (employee.name,)
        )
        conn.commit()
        return cursor.lastrowid
    
    def get_all_employees(self) -> List[Employee]:
        """Get all employees"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM employees ORDER BY name")
        rows = cursor.fetchall()
        
        return [Employee(
            id=row['id'],
            name=row['name'],
            created_at=datetime.fromisoformat(row['created_at'])
        ) for row in rows]
    
    def update_employee(self, employee: Employee) -> bool:
        """Update employee"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            "UPDATE employees SET name = ? WHERE id = ?",
            (employee.name, employee.id)
        )
        conn.commit()
        return cursor.rowcount > 0
    
    def delete_employee(self, employee_id: int) -> bool:
        """Delete employee"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM employees WHERE id = ?", (employee_id,))
        conn.commit()
        return cursor.rowcount > 0
    
    # Area operations
    def add_area(self, area: Area) -> int:
        """Add new area"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            "INSERT INTO areas (name) VALUES (?)",
            (area.name,)
        )
        conn.commit()
        return cursor.lastrowid
    
    def get_all_areas(self) -> List[Area]:
        """Get all areas"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM areas ORDER BY name")
        rows = cursor.fetchall()
        
        return [Area(
            id=row['id'],
            name=row['name'],
            created_at=datetime.fromisoformat(row['created_at'])
        ) for row in rows]
    
    def update_area(self, area: Area) -> bool:
        """Update area"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            "UPDATE areas SET name = ? WHERE id = ?",
            (area.name, area.id)
        )
        conn.commit()
        return cursor.rowcount > 0
    
    def delete_area(self, area_id: int) -> bool:
        """Delete area"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM areas WHERE id = ?", (area_id,))
        conn.commit()
        return cursor.rowcount > 0
    
    # Employee Area Rate operations
    def add_employee_area_rate(self, rate: EmployeeAreaRate) -> int:
        """Add or update employee area rate"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            """INSERT OR REPLACE INTO employee_area_rates 
               (employee_id, area_id, base_salary) VALUES (?, ?, ?)""",
            (rate.employee_id, rate.area_id, rate.base_salary)
        )
        conn.commit()
        return cursor.lastrowid
    
    def get_employee_area_rate(self, employee_id: int, area_id: int) -> Optional[float]:
        """Get base salary for employee in specific area"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT base_salary FROM employee_area_rates WHERE employee_id = ? AND area_id = ?",
            (employee_id, area_id)
        )
        row = cursor.fetchone()
        return row['base_salary'] if row else None
    
    def get_all_employee_area_rates(self) -> List[Tuple[str, str, float]]:
        """Get all employee area rates with names"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT e.name as employee_name, a.name as area_name, r.base_salary
            FROM employee_area_rates r
            JOIN employees e ON r.employee_id = e.id
            JOIN areas a ON r.area_id = a.id
            ORDER BY e.name, a.name
        """)
        
        return [(row['employee_name'], row['area_name'], row['base_salary']) 
                for row in cursor.fetchall()]
    
    # Salary Record operations
    def add_salary_record(self, record: SalaryRecord) -> int:
        """Add new salary record"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            """INSERT INTO salary_records 
               (employee_id, area_id, base_salary, allowance, total) 
               VALUES (?, ?, ?, ?, ?)""",
            (record.employee_id, record.area_id, record.base_salary, 
             record.allowance, record.total)
        )
        conn.commit()
        return cursor.lastrowid
    
    def get_all_salary_records(self) -> List[SalaryRecordView]:
        """Get all salary records with employee and area names"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT s.id, e.name as employee_name, a.name as area_name,
                   s.base_salary, s.allowance, s.total, s.date_created,
                   s.employee_id, s.area_id
            FROM salary_records s
            JOIN employees e ON s.employee_id = e.id
            JOIN areas a ON s.area_id = a.id
            ORDER BY s.date_created DESC
        """)
        
        return [SalaryRecordView(
            id=row['id'],
            employee_name=row['employee_name'],
            area_name=row['area_name'],
            base_salary=row['base_salary'],
            allowance=row['allowance'],
            total=row['total'],
            date_created=datetime.fromisoformat(row['date_created']),
            employee_id=row['employee_id'],
            area_id=row['area_id']
        ) for row in cursor.fetchall()]
    
    def update_salary_record(self, record: SalaryRecord) -> bool:
        """Update salary record"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            """UPDATE salary_records 
               SET employee_id = ?, area_id = ?, base_salary = ?, 
                   allowance = ?, total = ? 
               WHERE id = ?""",
            (record.employee_id, record.area_id, record.base_salary,
             record.allowance, record.total, record.id)
        )
        conn.commit()
        return cursor.rowcount > 0
    
    def delete_salary_record(self, record_id: int) -> bool:
        """Delete salary record"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM salary_records WHERE id = ?", (record_id,))
        conn.commit()
        return cursor.rowcount > 0
    
    def get_total_salaries(self) -> float:
        """Get grand total of all salary records"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT SUM(total) as grand_total FROM salary_records")
        row = cursor.fetchone()
        return row['grand_total'] if row['grand_total'] else 0.0
