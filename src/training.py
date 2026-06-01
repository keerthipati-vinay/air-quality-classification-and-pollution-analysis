from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score
import joblib
import os

from src.preprocessing import preprocess_data

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

    models = {

        "Decision Tree":
            DecisionTreeClassifier(
                random_state=42
            ),

        "Random Forest":
            RandomForestClassifier(
                n_estimators=300,
                max_depth=20,
                min_samples_split=5,
                min_samples_leaf=2,
                random_state=42
            ),

        "Logistic Regression":
            LogisticRegression(
                max_iter=500
            ),

        "KNN":
            KNeighborsClassifier(
                n_neighbors=5
            ),

        "SVM":
            SVC(kernel='rbf'),

        "XGBoost":
            XGBClassifier(
                n_estimators=300,
                learning_rate=0.05,
                max_depth=10,
                subsample=0.8,
                colsample_bytree=0.8,
                random_state=42,
                eval_metric='mlogloss'
            )
    }

    best_model = None

    best_accuracy = 0

    best_model_name = ""

    for name, model in models.items():

        print(f"\n============================")
        print(f"Training {name}")
        print(f"============================")

        # Models needing scaling
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

        else:

            model.fit(
                x_train,
                y_train
            )

            predictions = model.predict(
                x_test
            )

        # Accuracy
        accuracy = accuracy_score(
            y_test,
            predictions
        )

        print(f"\nAccuracy: {accuracy:}")

        # Best model selection
        if accuracy > best_accuracy:

            best_accuracy = accuracy

            best_model = model

            best_model_name = name

    print("\n================================")

    print("Best Model:", best_model_name)

    print(
        f"Best Accuracy:"
        f" {best_accuracy:}"
    )

    print("================================")

    # Save best model
    os.makedirs("models", exist_ok=True)

    joblib.dump(
        best_model,
        "models/air_quality_model.pkl"
    )

    print("\nModel Saved Successfully")


if __name__ == "__main__":

    train_models()