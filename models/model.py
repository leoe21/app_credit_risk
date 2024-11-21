import os
from dotenv import load_dotenv
import mlflow.sklearn

load_dotenv()

# Leer las variables de entorno
mlflow_tracking_username = os.getenv("MLFLOW_TRACKING_USERNAME")
mlflow_tracking_password = os.getenv("MLFLOW_TRACKING_PASSWORD")
mlflow_tracking_uri = os.getenv("MLFLOW_TRACKING_URI")

def load_model():
    """
    Carga el modelo entrenado desde MLflow.
    """
    mlflow.set_tracking_uri(mlflow_tracking_uri)

    model_name = "LoanRiskModel"
    model_version = 2

    model = mlflow.sklearn.load_model(model_uri=f"models:/{model_name}/{model_version}")
    return model