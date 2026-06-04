
import pandas as pd
import joblib


# LOAD MODEL INFO

model_info = joblib.load(
    "models/air_quality_model.pkl"
)

model = model_info["model"]

requires_scaling = (
    model_info["requires_scaling"]
)

# LOAD SCALER

scaler = joblib.load(
    "models/scaler.pkl"
)

# LOAD LABEL ENCODER

label_encoder = joblib.load(
    "models/label_encoder.pkl"
)

# LOAD FEATURE COLUMNS

feature_columns = joblib.load(
    "models/feature_columns.pkl"
)


# USER INPUT

input_data = {

  "PM2.5": 380.0, 
  "PM10": 490.0, 
  "NO": 90.0, 
  "NO2": 140.0, 
  "NOx": 210.0,
  "NH3": 85.0, 
  "CO": 4.8, 
  "SO2": 55.0, 
  "O3": 190.0,
  "Benzene": 12.5, 
  "Toluene": 18.0, 
  "Xylene": 5.5, 
  "AQI":460

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

# FINAL OUTPUT

print("\n================================")

print(
    "Predicted AQI Category:"
)

print(
    predicted_category[0]
)

print("================================")

