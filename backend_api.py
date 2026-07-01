
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class PatientData(BaseModel):
    glucose: float
    haemoglobin: float
    cholesterol: float

@app.post("/predict")
def predict(data: PatientData):

    prediction = []

    # Diabetes Risk
    if data.glucose > 6.5:
        prediction.append("Diabetes Risk")

    # Anemia Risk
    if data.haemoglobin < 11:
        prediction.append("Anemia Risk")

    # Heart Disease Risk
    if data.cholesterol > 240:
        prediction.append("Heart Disease Risk")

    # Healthy
    if len(prediction) == 0:
        result = "Healthy"

    else:
        result = ", ".join(prediction)

    return {
        "prediction": result
    }
