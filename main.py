from fastapi import FastAPI, HTTPException
import pandas as pd
from src.controller.employee_controller import router as employee_router
from src.controller import department_controller

app = FastAPI()


# --------- Csv File ----------------
employee_data = "data/employee_data.csv"
employee_salaries = "data/employee_salaries.csv"

#--------- Read Csv File -------------
def read_employee_data():
    return pd.read_csv(employee_data, on_bad_lines='skip')

def read_employee_salaries():
    return pd.read_csv(employee_salaries, on_bad_lines='skip')

#----------- Endpoint for message -----------
@app.get("/")
def read_root():
    return {"message": "Welcome to Employee Management System"}

# ------ Include the employee router ------
app.include_router(employee_router)
app.include_router(department_controller.router)


#----------- Run Server -------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000) 
