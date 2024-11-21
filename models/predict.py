import pandas as pd
from models.model import load_model

# Cargar el modelo entrenado
model = load_model()

def make_predictions(data: pd.DataFrame) -> list:
    """
    Realiza predicciones sobre los datos ingresados.
    :param data: DataFrame con datos enriquecidos.
    :return: Lista de predicciones.
    """
    features = data.drop(columns=["ID"])  # Excluir la columna ID antes de predecir
    predictions = model.predict(features)
    return predictions
