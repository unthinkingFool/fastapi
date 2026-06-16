from fastapi import FastAPI

app = FastAPI()
@app.get("/")
def home():
    return {"message": "Hello, World!"}

@app.get("/about")
def about():
    return {"message": "This is a simple FastAPI application about api."}
@app.get("/customer")
def customer(customer_id : int):
    return {"message": f"This is a simple FastAPI application about customer with ID: {customer_id}"}