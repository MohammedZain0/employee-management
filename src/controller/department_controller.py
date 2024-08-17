from fastapi import APIRouter , HTTPException
from src.services.department_service import get_all_departments
from src.services.department_service import get_employees_by_department
from src.schemas.department_schemas import DepartmentEmployeesResponse, DepartmentEmployee


router = APIRouter()

@router.get("/departments", tags=["Departments"], description="Returns a list of all departments.")
def get_departments():
    """Endpoint to get all departments."""
    departments = get_all_departments()
    return {"Departments": departments}


@router.get("/departments/{department_name}/employees", response_model=DepartmentEmployeesResponse, tags=["Departments"])
def get_department_employees(department_name: str):
    employees = get_employees_by_department(department_name)
    if not employees:
        raise HTTPException(status_code=404, detail="Department not found")
    return employees