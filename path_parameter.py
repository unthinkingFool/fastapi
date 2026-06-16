from fastapi import FastAPI
app = FastAPI()

customer_risk_profile = {
    101: {"name": "John Doe", "age": 30, "risk_level": 1},
    102: {"name": "Jane Smith", "age": 45, "risk_level": 2},
    103: {"name": "Bob Johnson", "age": 55, "risk_level": 3}
}

@app.get("/customer/{customer_id}")
def get_customer_risk_profile(customer_id: int):
    if customer_id in customer_risk_profile:
        return customer_risk_profile[customer_id]
    else:
        return {"message": f"Customer with ID {customer_id} not found."}
    
