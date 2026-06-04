from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report
)

import matplotlib.pyplot as plt
import seaborn as sns

# EVALUATE MODEL

def evaluate_model(
    y_test,
    predictions,
    model_name
):

    try:

        # Accuracy
        accuracy = accuracy_score(
            y_test,
            predictions
        )

        # Precision
        precision = precision_score(
            y_test,
            predictions,
            average='weighted',
            zero_division=0
        )

        # Recall
        recall = recall_score(
            y_test,
            predictions,
            average='weighted',
            zero_division=0
        )

        # F1 Score
        f1 = f1_score(
            y_test,
            predictions,
            average='weighted',
            zero_division=0
        )

        print("\n================================")

        print(f"{model_name} Evaluation")

        print("================================")

        print(f"\nAccuracy: {accuracy:}")

        print(f"Precision: {precision:}")

        print(f"Recall: {recall:}")

        print(f"F1 Score: {f1:}")

        # Classification Report
        print("\nClassification Report:\n")

        print(
            classification_report(
                y_test,
                predictions,
                zero_division=0
            )
        )

        # Confusion Matrix
        cm = confusion_matrix(
            y_test,
            predictions
        )

        print("\nConfusion Matrix:\n")

        print(cm)

        # Visualization
        plt.figure(figsize=(8, 6))

        sns.heatmap(
            cm,
            annot=True,
            fmt='d',
            cmap='Blues'
        )

        plt.title(
            f"{model_name} Confusion Matrix"
        )

        plt.xlabel("Predicted")

        plt.ylabel("Actual")

        plt.show()

        # Return accuracy for best model selection
        return {
            "accuracy": accuracy,
            "precision":precision,
            "recall":recall
        }

    except Exception as e:

        print(f"Evaluation Error: {e}")
