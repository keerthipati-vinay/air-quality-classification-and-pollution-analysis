from sklearn.tree import DecisionTreeClassifier

from sklearn.ensemble import (
    RandomForestClassifier
)

from sklearn.linear_model import (
    LogisticRegression
)

from sklearn.neighbors import (
    KNeighborsClassifier
)

from sklearn.svm import SVC

from xgboost import XGBClassifier

import joblib
import os

from src.preprocessing import (
    preprocess_data
)

from src.evaluation import (
    evaluate_model
)

# Train Models 

def train_models():

    (
        x_train,
        x_test,
        x_train_scaled,
        x_test_scaled,
        y_train,
        y_test,
        label_encoder
    ) = preprocess_data()
  
# MODELS

    models = {

        "Logistic Regression":
            LogisticRegression(
                max_iter=500
            ),

        "KNN":
            KNeighborsClassifier(
                n_neighbors=5
            ),

        "SVM":
            SVC(
                kernel='rbf'
            ),
        "Random Forest":
            RandomForestClassifier(
            n_estimators=200,
            random_state=42
            ),

        "XGBoost":
            XGBClassifier(
                n_estimators=300,
                learning_rate=0.05,
                max_depth=6,
                subsample=0.8,
                colsample_bytree=0.8,
                random_state=42,
                eval_metric='mlogloss'
            )
    }

    # BEST MODEL VARIABLES

    best_model = None

    best_accuracy = 0
    best_precision  = 0
    best_recall = 0

    best_model_name = ""
    
    requires_scaling=False 
    
    os.makedirs(
        "models",
        exist_ok=True
    )

    # TRAIN EACH MODEL

    for name, model in models.items():

        print("\n================================")

        print(f"Training {name}")

        print("================================")

        # MODELS NEEDING SCALING
        
        if name in [
            "Logistic Regression",
            "KNN",
            "SVM"
        ]:

            model.fit(
                x_train_scaled,
                y_train
            )

            predictions = model.predict(
                x_test_scaled
            )
            current_scaling = True

        # MODELS NOT NEEDING SCALING

        else:

            model.fit(
                x_train,
                y_train
            )

            predictions = model.predict(
                x_test
            )
            
            current_scaling = False

        
        # EVALUATION

        metrics = evaluate_model(
            y_test,
            predictions,
            name
        )
        accuracy=metrics["accuracy"]
        
        precision=metrics["precision"]
        
        recall=metrics["recall"]
        
        # SAVE CURRENT MODEL

        file_name = (
            name.lower()
            .replace(" ", "_")
            + ".pkl"
        )

        model_info = {

            "model": model,

            "requires_scaling":
                current_scaling,

            "model_name":
                name
        }

        joblib.dump(
            model_info,
            f"models/{file_name}"
        )

        print(
            f"{name} saved successfully"
        )

       
        # BEST MODEL SELECTION

    if accuracy > best_accuracy:

        best_accuracy = accuracy

        best_model = model

        best_model_name = name
        
        requires_scaling = current_scaling
            
    if precision > best_precision:

        best_precision = precision
            
        best_model = model
            
        best_model_name = name 
        
        requires_scaling = current_scaling

    if recall > best_recall:

        best_recall = recall
            
        best_model = model
            
        best_model_name = name
        
        requires_scaling = current_scaling


    # BEST MODEL DETAILS

    print("\n================================")

    print("Best Model:", best_model_name)

    print(
        f"Best Accuracy: "
        f"{best_accuracy:.4f}"
    )
    print(
        f"Best precision: "
        f"{best_precision:.4f}"
    )
    print(
        f"Best recall: "
        f"{best_recall:.4f}"
    )

    print("================================")

    # SAVE BEST MODEL

    os.makedirs(
        "models",
        exist_ok=True
    )
    model_info = { 
                   "model": best_model, 
                   "requires_scaling": requires_scaling, 
                   "model_name": best_model_name
                } 
    joblib.dump( 
                model_info, 
                "models/air_quality_model.pkl" 
    )
    

    print("\nModel Saved Successfully")


 
# MAIN

if __name__ == "__main__":

    train_models()

