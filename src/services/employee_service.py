import pandas as pd
from typing import List, Dict, Optional,Union
from datetime import datetime
from src.schemas.employee_schemas import EmployeeCreate



# ---------- Csv File Paths -------------
employee_data = "data/employee_data.csv"
employee_salaries_file = "data/employee_salaries.csv"

# ---------- Read employee data from CSV file------------
def read_employee_data() -> pd.DataFrame:
    df = pd.read_csv('data/employee_data.csv', usecols=lambda x: x not in ['Start_Date', 'End_Date'], on_bad_lines='skip')
    return df


#----------- Read employee salaries data from CSV file ----------
def read_employee_salaries() -> pd.DataFrame:
    """Read employee salaries data from CSV file."""
    return pd.read_csv(employee_salaries_file, on_bad_lines='skip')


def write_employee_data(df: pd.DataFrame) -> None:
    """Write employee data to CSV file."""
    df.to_csv('data/employee_data.csv', index=False)

# -------- Get all employees --------
def get_all_employees() -> List[Dict]:
    """Get all employees and return as a list of dictionaries."""
    df = read_employee_data()
    employees = df.to_dict(orient="records")
    return employees

#------------ Get employee by ID ------------

def get_employee_by_id(employee_id: int) -> Optional[Dict]:
    """Get an employee by ID and return as a dictionary."""
    employee_data = read_employee_data()
    employee_salaries = read_employee_salaries()
    
    employee_details = employee_data[employee_data['EmployeeID'] == employee_id]
    if employee_details.empty:
        return None
    
    employee = employee_details.iloc[0].to_dict()
    
    salary_details = employee_salaries[employee_salaries['EmployeeID'] == employee_id]
    if not salary_details.empty:
        first_record = salary_details.iloc[0]
        last_record = salary_details.iloc[-1]
        
        start_date = pd.to_datetime(f"01 {first_record['Month']} {first_record['Year']}", format='%d %B %Y').strftime('%d/%m/%Y')
        end_date = pd.to_datetime(f"30 {last_record['Month']} {last_record['Year']}", format='%d %B %Y').strftime('%d/%m/%Y')
        
        employee['Start_Date'] = start_date
        employee['End_Date'] = end_date
    else:
        employee['Start_Date'] = None
        employee['End_Date'] = None
    
    return employee




#---------- Add New Employee -----------
def add_employee(employee: EmployeeCreate) -> Dict:
    """Add a new employee to the CSV file."""
    df = read_employee_data()
    
    new_employee = pd.DataFrame([employee.dict()])
    df = pd.concat([df, new_employee], ignore_index=True)
    
    write_employee_data(df)
    
    return {"EmployeeID": employee.EmployeeID, "Message": "Employee added successfully"}

# ----------- Apdate Employee -------------

def update_employee(employee_id: int, updated_data: dict) -> Optional[Dict]:
    """Update an employee's data by ID."""
    employee_data = read_employee_data()
    
    index = employee_data.index[employee_data['EmployeeID'] == employee_id].tolist()
    if not index:
        return None  
    
    employee_index = index[0]
    for key, value in updated_data.items():
        if key in employee_data.columns:
            employee_data.at[employee_index, key] = value
    
    employee_data.to_csv("data/employee_data.csv", index=False)
    
    return employee_data.iloc[employee_index].to_dict()


# --------------- Delete Employee ---------------
def delete_employee(employee_id: int) -> Optional[Dict]:
    df = read_employee_data()
    employee_to_delete = df[df['EmployeeID'] == employee_id]
    if employee_to_delete.empty:
        return None
    
    df = df[df['EmployeeID'] != employee_id]
    
    df.to_csv(employee_data, index=False)
    
    return employee_to_delete.iloc[0].to_dict()


def get_department_employees(department_name: str) -> List[Dict]:
    """Get all employees in a specified department and return as a list of dictionaries."""
    df = read_employee_data()
    department_employees = df[df['Department'].str.lower() == department_name.lower()]
    
    employees = department_employees[['EmployeeID', 'FirstName', 'Surname', 'Department', 'Position']].to_dict(orient="records")
    return employees


def get_avg_salary(employee_id: int) -> float:
    """الحصول على متوسط ​​الراتب لموظف معين."""
    salaries = read_employee_salaries()
    
    employee_salaries = salaries[salaries['EmployeeID'] == employee_id]['Salary']
    
    if employee_salaries.empty:
        return None
    
    avg_salary = employee_salaries.mean()
    
    return round(avg_salary, 2)  


# Get the number of months of service for an employee
def get_months_of_service(employee_id: int) -> int:
    """Calculate the number of months an employee has worked in the organization."""
    employee_salaries = read_employee_salaries()
    salary_details = employee_salaries[employee_salaries['EmployeeID'] == employee_id]
    
    if salary_details.empty:
        return 0  
    
    months_of_service = len(salary_details)  
    return months_of_service


def get_years_of_service(employee_id: int) -> str:
    """Return the number of years (and months) an employee has worked in the organization."""
    employee_salaries = read_employee_salaries()
    
    salary_details = employee_salaries[employee_salaries['EmployeeID'] == employee_id]
    if salary_details.empty:
        return "Employee not found or no salary data available."
    
    first_record = salary_details.iloc[0]
    last_record = salary_details.iloc[-1]
    
    start_date = pd.to_datetime(f"01 {first_record['Month']} {first_record['Year']}", format='%d %B %Y')
    end_date = pd.to_datetime(f"30 {last_record['Month']} {last_record['Year']}", format='%d %B %Y')
    
    total_months = (end_date.year - start_date.year) * 12 + (end_date.month - start_date.month + 1)

    years = total_months // 12
    months = total_months % 12

    if years > 0 and months > 0:
        return f"{years} years and {months} months"
    elif years > 0:
        return f"{years} years"
    else:
        return f"{months} months"
