import joblib
import io
import pandas as pd
from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.responses import StreamingResponse
from pydantic import BaseModel,Field

app = FastAPI()

# Load the trained model and column names
model = joblib.load('housing_random_forest_model.joblib')
columns = joblib.load('housing_random_forest_columns.joblib')

# input schema for the API
class HousingData(BaseModel):
    MedInc: float = Field(..., gt=0, description="Median income in block group")
    HouseAge: float = Field(..., gt=0, description="Median house age in block group")
    AveRooms: float = Field(..., gt=0, description="Average number of rooms per household")
    AveBedrms: float = Field(..., gt=0, description="Average number of bedrooms per household")
    Population: float = Field(..., gt=0, description="Block group population")
    AveOccup: float = Field(..., gt=0, description="Average number of household members")
    Latitude: float = Field(..., gt=32, lt=42, description="Block group latitude")
    Longitude: float = Field(..., gt=-125, lt=-114, description="Block group longitude")


# home route
@app.get("/")
def home():
    return {"message": "Welcome to the California Housing Price Prediction API!"}

# health
@app.get("/health")
def health():
    return {"status": "ok",
            "model": "random_forest_model",
            "columns": columns,
            "avg_error": 25000.0
            }

# prediction route
@app.post("/predict")
def predict(data: HousingData):
    try:
        input_data=pd.DataFrame([{
            "MedInc": data.MedInc,
            "HouseAge": data.HouseAge,
            "AveRooms": data.AveRooms,
            "AveBedrms": data.AveBedrms,
            "Population": data.Population,
            "AveOccup": data.AveOccup,
            "Latitude": data.Latitude,
            "Longitude": data.Longitude
        }])

        prediction = model.predict(input_data[columns])[0]
        
        return {"predicted_price": f"${prediction*100000:,.2f}" ,
                "avg_error": 25000.0,
                "varrying range": f"${(prediction-0.25)*100000:,.2f} - ${(prediction+0.25)*100000:,.2f}",
                "model": "random_forest_model",
                "columns": columns
                }  # Convert to actual price
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
# route to upload new data for prediction
@app.post("/predict-file")
async def predict_file(file: UploadFile = File(...)):
    try:
        if not file.filename.endswith('.csv'):
            raise HTTPException(status_code=400, detail="Invalid file format. Please upload a CSV file.")
        
        contents = await file.read()
        df=pd.read_csv(io.StringIO(contents.decode('utf-8')))

        required_columns = [
            "MedInc", "HouseAge", "AveRooms", "AveBedrms",
            "Population", "AveOccup", "Latitude", "Longitude"
        ]

        if not all(col in df.columns for col in required_columns):
            raise HTTPException(status_code=400, detail=f"Missing required columns. Required columns are: {required_columns}")
        
        if len(df) == 0:
            raise HTTPException(status_code=400, detail="The uploaded CSV file is empty.")
        
        predictions = model.predict(df[columns])
        df['PredictedPrice'] = predictions * 100000  # Convert to actual price

        output=df.to_csv(index=False)
        return StreamingResponse(io.StringIO(output), media_type="text/csv", headers={"Content-Disposition": f"attachment; filename=predictions.csv"})
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))