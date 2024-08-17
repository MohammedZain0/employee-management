from pydantic import BaseModel,EmailStr
from typing import Optional
from datetime import date

class Employee(BaseModel):
    EmployeeID: int
    FirstName: str
    Surname: str
    Department: str
    Position: str


class EmployeeCreate(BaseModel):
    EmployeeID: int
    FirstName: str
    Surname: str
    Email: str
    DateOfBirth: str
    Department: str
    Position: str

class EmployeeUpdate(BaseModel):
    FirstName: Optional[str]
    Surname: Optional[str]
    Email: Optional[str]
    DateOfBirth: Optional[date]
    Department: Optional[str]
    Position: Optional[str]


# Schema for the response of months of service
class MonthsOfServiceResponse(BaseModel):
    months: int



# Schema for the response of yeaes of service

class EmployeeYearsOfServiceResponse(BaseModel):
    years: int