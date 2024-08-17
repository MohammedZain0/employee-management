from fastapi import APIRouter, HTTPException
from typing import List, Dict, Optional
from src.services.employee_service import get_all_employees, get_employee_by_id, add_employee, update_employee, delete_employee, get_avg_salary , get_months_of_service,get_years_of_service
from src.schemas.employee_schemas import EmployeeCreate , EmployeeUpdate , MonthsOfServiceResponse , EmployeeYearsOfServiceResponse


router = APIRouter()

# -------------- get_all_employees -----------------
@router.get("/employees",response_model=List[Dict],tags=["Employees"],description="Retrieve a list of all employees. Each employee object includes their ID, first name, surname, department, and position.")
def read_employees():
    return get_all_employees()

# -------------- get_employee_by_id --------------
@router.get("/employees/{employee_id}",response_model=Dict,tags=["Employees"],description="Retrieve detailed information about a specific employee by their ID. Includes their ID, first name, surname, email, date of birth, department, position, start date, and end date.")
def read_employee(employee_id: int):
    employee = get_employee_by_id(employee_id)
    if employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee

# -------------- create_employee ----------------
@router.post("/employees", tags=["Employees"])
async def create_employee(employee: EmployeeCreate):
    try:
        response = add_employee(employee)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ------------- update -----------------
@router.put("/employees/{employee_id}",tags=["Employees"])
async def update_employee_endpoint(employee_id: int, updated_data: EmployeeUpdate):
    updated_employee = update_employee(employee_id, updated_data.dict(exclude_unset=True))
    if not updated_employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return {"message": "Employee updated successfully", "employee": updated_employee}

# --------------- Delete --------------
@router.delete("/employees/{employee_id}", tags=["Employees"], description="Delete an employee from the database based on their ID.")
def delete_employee_endpoint(employee_id: int) -> Dict:
    """Delete an employee from the database."""
    deleted_employee = delete_employee(employee_id)
    if deleted_employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    return {"message": f"Employee with ID {employee_id} has been successfully deleted.", "deleted_employee": deleted_employee}


@router.get("/employees/{employee_id}/avg-salary", tags=["Employees"], description="Returns the average salary of a specific employee.")
def get_employee_avg_salary(employee_id: int):
    avg_salary = get_avg_salary(employee_id)
    
    if avg_salary is None:
        raise HTTPException(status_code=404, detail="Employee not found or no salary records available.")
    
    return {"avg_salary": f"{avg_salary} £"}


# Get the number of months of service for an employee
@router.get("/employees/{employee_id}/months-of-service", response_model=MonthsOfServiceResponse, tags=["Employees"])
def get_employee_months_of_service(employee_id: int):
    months = get_months_of_service(employee_id)
    
    if months == 0:
        raise HTTPException(status_code=404, detail="Employee not found or has no recorded service months.")
    
    return MonthsOfServiceResponse(months=months)

@router.get("/employees/{employee_id}/years-of-service", tags=["Employees"])
def get_employee_years_of_service(employee_id: int):
    years_of_service = get_years_of_service(employee_id)
    return {"years_of_service": years_of_service}