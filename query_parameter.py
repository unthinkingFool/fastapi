from fastapi import FastAPI
app = FastAPI()

all_customers = [
    {"id": 1, "name": "John Doe", "city": "NewYork", "age": 30,"risk": "low"},
    {"id": 2, "name": "Jane Smith", "city": "LosAngeles", "age": 25,"risk": "medium"},
    {"id": 3, "name": "Mike Johnson", "city": "Chicago", "age": 30,"risk": "high"},
    {"id": 4, "name": "Emily Davis", "city": "NewYork", "age": 28,"risk": "low"},
    {"id": 5, "name": "David Wilson", "city": "Phoenix", "age": 40,"risk": "medium"},
]

@app.get("/customers")
def get_customers(city: str, risk: str ):
    filtered_customers = [
        customer for customer in all_customers
        if customer["city"] == city and customer["risk"] == risk
    ]

    return {
        "city": city,
        "risk": risk,
        "customer_count": len(filtered_customers),
        "customers": filtered_customers
    }
