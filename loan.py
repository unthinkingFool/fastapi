from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class loan(BaseModel):
    age: int
    loan_id: int
    amount: float
    interest_rate: float
   

@app.post("/loan")
def create_loan(loan: loan):
    if loan.age < 18:
        return {"message": "Loan application rejected. Applicant must be at least 18 years old."}
    elif loan.amount <= 0:
        return {"message": "Loan application rejected. Amount must be greater than zero."}
    elif loan.interest_rate < 0:
        return {"message": "Loan application rejected. Interest rate cannot be negative."}
    else:
        return {"message": f"Loan application accepted for loan ID: {loan.loan_id} with amount: {loan.amount} and interest rate: {loan.interest_rate}%."}
    
@app.get("/customer/{customer_id}")
def get_customer(customer_id: int):
    return {"message": f"Customer details for ID: {customer_id}"}