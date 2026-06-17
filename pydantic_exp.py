from fastapi import FastAPI
from pydantic import BaseModel



app = FastAPI()

class Loan(BaseModel):
    name: str
    customer_id: int
    income: float
    age: int
    amount: float
    interest_rate: float
    


@app.post("/predict_loan_risk")
def predict_loan_risk(loan: Loan):

    approved=(
        loan.income >= 50000 and
        loan.age > 25 and
        loan.amount < 50000 and
        loan.interest_rate < 10 
    
    )
    return {
        "name": loan.name,
        "customer_id": loan.customer_id,
        "loan_amount": loan.amount,
        "approved": approved
    }