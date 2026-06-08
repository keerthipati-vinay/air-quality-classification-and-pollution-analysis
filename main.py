from fastapi import FastAPI
from pydantic import BaseModel

import pandas as pd 
import joblib

#FastAPI app

app=FastAPI(
    title="Air Quality Classification and pollution analysis API"
)

#load saved files 
model_info = joblib.load( "models/air_quality_model.pkl" ) 

model = model_info["model"] 

requires_scaling = ( model_info["requires_scaling"] )
 
scaler = joblib.load( "models/scaler.pkl" ) 

label_encoder = joblib.load( "models/label_encoder.pkl" )
 
feature_columns = joblib.load( "models/feature_columns.pkl" )

# INPUT SCHEMA 
class AirQualityInput(BaseModel): 
    PM2_5: float 
    PM10: float 
    NO: float 
    NO2: float 
    NOx: float 
    NH3: float 
    CO: float 
    SO2: float 
    O3: float 
    Benzene: float 
    Toluene: float 
    Xylene: float 
    AQI: float
    

# Home route
@app.get("/")
def home():
    return{
        "message":
            "Air Quality Classification and pollution analysis API Running "
            
    }
    
#prediction route
@app.post("/predict")
def predict(data: AirQualityInput ):
    input_data = { 
                  "PM2.5": data.PM2_5, 
                  "PM10": data.PM10, 
                  "NO": data.NO, 
                  "NO2": data.NO2, 
                  "NOx": data.NOx, 
                  "NH3": data.NH3, 
                  "CO": data.CO, 
                  "SO2": data.SO2, 
                  "O3": data.O3, 
                  "Benzene": data.Benzene, 
                  "Toluene": data.Toluene, 
                  "Xylene": data.Xylene, 
                  "AQI": data.AQI 
                }
    # CONVERT TO DATAFRAME

    input_df = pd.DataFrame(
        [input_data]
    )

    # ARRANGE COLUMN ORDER

    input_df = input_df[
        feature_columns
    ]

    # SCALE IF REQUIRED

    if requires_scaling:

        input_df = scaler.transform(
            input_df
        )

    # PREDICTION

    prediction = model.predict(
        input_df
    )

    # DECODE PREDICTION

    predicted_category = (
        label_encoder.inverse_transform(
            prediction
        )
    )
    
    probabilities = model.predict_proba(
        input_df
    )

    confidence = (
        probabilities.max() * 100
    )


    class_probabilities = {}

    for i, class_name in enumerate(
        label_encoder.classes_
    ):

       class_probabilities[class_name] = round(
        float(probabilities[0][i] * 100),2
    )
    
    return {

        "predicted_category":
            predicted_category[0],

        "confidence":
            round(
                float(confidence),2
            ),

        "all_classes_probabilities":
            class_probabilities
    }
    

    
