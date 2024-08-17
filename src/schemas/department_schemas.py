from pydantic import BaseModel
from typing import List

# Schema for individual employee in a department
class DepartmentEmployee(BaseModel):
    EmployeeID: int
    FirstName: str
    Surname: str
    Department: str
    Position: str

DepartmentEmployeesResponse = List[DepartmentEmployee]
