from fastapi import APIRouter, HTTPException
import numpy as np
import pandas as pd
from fastapi.encoders import jsonable_encoder
from database.connection import connect_to_snowflake
from database.queries import GET_FEATURES_BY_ID, INSERT_PREDICTION, UPDATE_IS_PROCESSED
from models.model import load_model
import shap  # Para generar explicaciones sobre las predicciones

# Crear un router para organizar las rutas de FastAPI
router = APIRouter()

# Cargar el modelo y el pipeline preentrenado
pipeline = load_model()

@router.post("/predict_and_explain/{client_id}")
async def predict_and_explain(client_id: int):
    """
    Endpoint para:
    1. Obtener datos de un cliente a partir de su ID.
    2. Generar una predicción usando un modelo de Machine Learning.
    3. Explicar la predicción con SHAP.
    4. Guardar los resultados en una base de datos.
    """
    # Conectar a la base de datos
    conn = connect_to_snowflake()
    cursor = conn.cursor()
    
    try:
        # 1. Consultar los datos del cliente en la base de datos
        query = GET_FEATURES_BY_ID.format(client_id=client_id)
        client_data = pd.read_sql(query, conn)
        
        # Verificar si los datos del cliente existen
        if client_data.empty:
            raise HTTPException(status_code=404, detail="Cliente no encontrado.")
        
        # 2. Preparar los datos para el modelo
        # Eliminar columnas innecesarias, en este caso "ID"
        features = client_data.drop(columns=["ID"])
        
        # Transformar los datos usando el preprocesador del pipeline
        processed_features = pipeline.named_steps["preprocessor"].transform(features)

        # Obtener los nombres de las características transformadas
        transformed_feature_names = pipeline.named_steps["preprocessor"].get_feature_names_out(input_features=features.columns)

        # 3. Generar la predicción
        prediction = pipeline.named_steps["classifier"].predict(processed_features)[0]  # Clase predicha
        prediction_proba = pipeline.named_steps["classifier"].predict_proba(processed_features)[0]  # Probabilidades por clase

        # Definir el umbral para decidir si se aprueba o rechaza (80%)
        probability_threshold = 0.8
        probability_score = prediction_proba[int(prediction)]  # Probabilidad de la clase predicha
        prediction_result = "Aprobado" if probability_score >= probability_threshold else "Rechazado"
        
        # Crear un indicador (1 si aprobado, 0 si rechazado)
        approval_indicator = 1 if probability_score >= probability_threshold else 0

        # 4. Generar explicación con SHAP
        # Crear un explicador con el modelo ya entrenado
        explainer = shap.Explainer(pipeline.named_steps["classifier"], processed_features)
        shap_values = explainer(processed_features)

        # Obtener valores relevantes para la clase predicha
        predicted_class_index = int(prediction)
        base_value = float(shap_values.base_values[0, predicted_class_index])  # Valor base del modelo
        shap_values_for_predicted_class = shap_values.values[0][:, predicted_class_index]  # Impacto de cada característica

        # Crear un diccionario que asocia características con su impacto
        feature_impact = {
            feature: float(impact) for feature, impact in zip(transformed_feature_names, shap_values_for_predicted_class)
        }

        # Crear un DataFrame con las características transformadas para enviarlas como resultado
        client_data_transformed = pd.DataFrame(processed_features, columns=transformed_feature_names)

        # Convertir los datos a un formato serializable (diccionario)
        client_data_transformed_dict = client_data_transformed.to_dict(orient="records")[0]

        # Crear una explicación completa
        explanation = {
            "prediction": int(prediction),
            "probability": probability_score,
            "base_value": base_value,
            "feature_impact": feature_impact,
            "feature_names": transformed_feature_names.tolist()
        }

        # 5. Guardar los resultados en la base de datos
        cursor.execute(INSERT_PREDICTION, (client_id, int(approval_indicator)))  # Insertar la predicción
        cursor.execute(UPDATE_IS_PROCESSED % client_id)  # Marcar al cliente como procesado
        conn.commit()  # Confirmar los cambios en la base de datos

        # 6. Preparar la respuesta para el usuario
        response = {
            "client_data": client_data.to_dict(orient="records")[0],  # Datos originales del cliente
            "client_data_transformed": client_data_transformed_dict,  # Datos transformados
            "prediction_result": prediction_result,  # Resultado (Aprobado/Rechazado)
            "probability": f"{probability_score * 100:.2f}%",  # Probabilidad en porcentaje
            "explanation": explanation  # Explicación detallada
        }

        return response

    except Exception as e:
        # En caso de error, revertir cualquier cambio en la base de datos
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Error al procesar la predicción: {e}")
    finally:
        # Asegurarse de cerrar la conexión a la base de datos
        conn.close()

