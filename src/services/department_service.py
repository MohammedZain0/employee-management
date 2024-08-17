import pandas as pd
from typing import List, Dict


# Path to the CSV file
employee_data = "data/employee_data.csv"

# Function to read the employee data CSV file
def read_employee_data() -> pd.DataFrame:
    """Reads the employee data from the CSV file."""
    return pd.read_csv(employee_data, on_bad_lines='skip')


# Function to get all departments
def get_all_departments() -> list:
    """Returns a list of all unique departments."""
    df = read_employee_data()
    departments = df['Department'].unique().tolist()
    return departments


def get_employees_by_department(department_name: str) -> List[Dict]:
    """Returns a list of employees in the specified department."""
    df = read_employee_data()
    department_employees = df[df['Department'] == department_name]

    # Extract required fields
    employees = department_employees[['EmployeeID', 'FirstName', 'Surname', 'Department', 'Position']].to_dict(orient="records")
    return employees