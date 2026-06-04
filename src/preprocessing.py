
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.preprocessing import (
    LabelEncoder,
    StandardScaler
)

from sklearn.model_selection import train_test_split

import os
import joblib


# LOAD DATASET

def load_dataset():

    try:

        df = pd.read_csv(
            "Datasets/city_day.csv"
        )

        # REMOVE EXTRA SPACES
        df.columns = df.columns.str.strip()

        print("\nDataset Loaded Successfully")

        print("\nOriginal Shape:", df.shape)

        print("\nColumn Names:")
        print(df.columns.tolist())

        return df

    except FileNotFoundError:

        print("Error: Dataset file not found")

    except pd.errors.EmptyDataError:

        print("Error: CSV file is empty")

    except pd.errors.ParserError:

        print("Error: Problem parsing CSV file")

    except Exception as e:

        print(f"Unexpected Error: {e}")


# EDA

def perform_eda(df):

    try:

        print("\nFirst 5 Rows:")
        print(df.head())

        print("\nDataset Information:")
        df.info()

        print("\nNull Values Count:")
        print(df.isna().sum())

        print("\nDuplicate Rows Count:")
        print(df.duplicated().sum())

        # CORRELATION HEATMAP

        plt.figure(figsize=(12, 8))

        sns.heatmap(
            df.corr(numeric_only=True),
            annot=True,
            cmap="coolwarm"
        )

        plt.title(
            "Correlation Heatmap"
        )

        plt.show()

    except Exception as e:

        print(f"EDA Error: {e}")


# DATA CLEANING

def clean_data(df):

    try:

        # REMOVE DUPLICATES

        df.drop_duplicates(
            inplace=True
        )

        # SELECT FEATURES

        selected_features = [

            "PM2.5",
            "PM10",
            "NO",
            "NO2",
            "NOx",
            "NH3",
            "CO",
            "SO2",
            "O3",
            "Benzene",
            "Toluene",
            "Xylene",
            "AQI"
        ]

        # KEEP REQUIRED COLUMNS

        df = df[selected_features]

        # REMOVE MISSING AQI ROWS

        df.dropna(
            subset=["AQI"],
            inplace=True
        )

        # FILL MISSING VALUES

        numeric_columns = (
            df.select_dtypes(
                include=np.number
            ).columns
        )

        for col in numeric_columns:

            df[col] = df[col].fillna(
                df[col].median()
            )

        print(
            "\nCleaned Dataset Shape:",
            df.shape
        )

        print(
            "\nRemaining Null Values:"
        )

        print(df.isna().sum())

        return df

    except KeyError as e:

        print(f"Column Error: {e}")

    except Exception as e:

        print(f"Cleaning Error: {e}")


# SAVE PROCESSED DATA

def save_processed_data(df):

    try:

        os.makedirs(
            "Datasets/processed",
            exist_ok=True
        )

        processed_path = (
            "Datasets/processed/"
            "processed_city_day.csv"
        )

        df.to_csv(
            processed_path,
            index=False
        )

        print(
            f"\nProcessed dataset saved to:"
            f" {processed_path}"
        )

    except Exception as e:

        print(f"Saving Error: {e}")


# CREATE AQI BUCKET

def create_aqi_bucket(df):

    try:

        def categorize_aqi(aqi):

            if aqi <= 50:
                return "Good"

            elif aqi <= 100:
                return "Satisfactory"

            elif aqi <= 200:
                return "Moderate"

            elif aqi <= 300:
                return "Poor"

            elif aqi <= 400:
                return "Very Poor"

            else:
                return "Severe"

        # CREATE AQI CATEGORY

        df["AQI_Bucket"] = (
            df["AQI"].apply(
                categorize_aqi
            )
        )

        # LABEL ENCODING

        label_encoder = LabelEncoder()

        df["AQI_Bucket"] = (
            label_encoder.fit_transform(
                df["AQI_Bucket"]
            )
        )

        print(
            "\nAQI Bucket Created Successfully"
        )

        print("\nAQI Bucket Counts:")

        print(
            df["AQI_Bucket"]
            .value_counts()
        )

        # SAVE LABEL ENCODER

        os.makedirs(
            "models",
            exist_ok=True
        )

        joblib.dump(
            label_encoder,
            "models/label_encoder.pkl"
        )

        return df, label_encoder

    except Exception as e:

        print(f"Encoding Error: {e}")


# SPLIT FEATURES AND TARGET

def split_features_target(df):

    try:

        x = df.drop(
            "AQI_Bucket",
            axis=1
        )

        y = df["AQI_Bucket"]

        print(
            "\nFeatures Shape:",
            x.shape
        )

        print(
            "\nTarget Shape:",
            y.shape
        )

        x_train, x_test, y_train, y_test = (
            train_test_split(
                x,
                y,
                test_size=0.2,
                random_state=42,
                stratify=y
            )
        )

        print(
            "\nTrain Test Split Completed"
        )

        return (
            x_train,
            x_test,
            y_train,
            y_test
        )

    except Exception as e:

        print(f"Split Error: {e}")


# FEATURE SCALING

def scale_features(
    x_train,
    x_test
):

    try:

        scaler = StandardScaler()

        x_train_scaled = (
            scaler.fit_transform(
                x_train
            )
        )

        x_test_scaled = (
            scaler.transform(
                x_test
            )
        )

        # SAVE SCALER

        os.makedirs(
            "models",
            exist_ok=True
        )

        joblib.dump(
            scaler,
            "models/scaler.pkl"
        )

        print(
            "\nFeature Scaling Completed"
        )

        return (
            x_train_scaled,
            x_test_scaled,
            scaler
        )

    except Exception as e:

        print(f"Scaling Error: {e}")


# MAIN PREPROCESS FUNCTION

def preprocess_data():

    df = load_dataset()

    perform_eda(df)

    df = clean_data(df)

    save_processed_data(df)

    df, label_encoder = (
        create_aqi_bucket(df)
    )

    (
        x_train,
        x_test,
        y_train,
        y_test
    ) = split_features_target(df)

    # SAVE FEATURE COLUMNS

    joblib.dump(
        x_train.columns.tolist(),
        "models/feature_columns.pkl"
    )

    (
        x_train_scaled,
        x_test_scaled,
        scaler
    ) = scale_features(
        x_train,
        x_test
    )

    return (

        x_train,
        x_test,

        x_train_scaled,
        x_test_scaled,

        y_train,
        y_test,

        label_encoder
    )


# MAIN

if __name__ == "__main__":

    preprocess_data()

