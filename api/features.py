from fastapi import APIRouter, HTTPException
import numpy as np
import pandas as pd
from fastapi.encoders import jsonable_encoder
from database.connection import connect_to_snowflake
from database.queries import GET_FEATURES_BY_ID, INSERT_PREDICTION, UPDATE_IS_PROCESSED
from models.model import load_model
import shap  # Para explicabilidad

router = APIRouter()

# Cargar el pipeline y el modelo
pipeline = load_model()

@router.post("/predict_and_explain/{client_id}")
async def predict_and_explain(client_id: int):
    """
    Endpoint para obtener predicciones de un usuario específico, explicar los resultados,
    y guardar la predicción en la base de datos con un indicador (1 si > 80%, 0 si < 80%).
    """
    conn = connect_to_snowflake()
    cursor = conn.cursor()
    
    try:
        # Buscar los datos del cliente por ID
        query = GET_FEATURES_BY_ID.format(client_id=client_id)
        client_data = pd.read_sql(query, conn)
        
        if client_data.empty:
            raise HTTPException(status_code=404, detail="Cliente no encontrado.")
        
        # Preparar los datos para el modelo
        features = client_data.drop(columns=["ID"])
        processed_features = pipeline.named_steps["preprocessor"].transform(features)

        # Obtener nombres de las características transformadas
        transformed_feature_names = pipeline.named_steps["preprocessor"].get_feature_names_out(input_features=features.columns)

        # Predicción
        prediction = pipeline.named_steps["classifier"].predict(processed_features)[0]
        prediction_proba = pipeline.named_steps["classifier"].predict_proba(processed_features)[0]

        # Umbral de probabilidad para el indicador
        probability_threshold = 0.8
        probability_score = prediction_proba[int(prediction)]
        prediction_result = "Aprobado" if probability_score >= probability_threshold else "Rechazado"
        
        # Crear indicador para guardar en la base de datos
        approval_indicator = 1 if probability_score >= probability_threshold else 0

        # Generar explicación usando SHAP
        explainer = shap.Explainer(pipeline.named_steps["classifier"], processed_features)
        shap_values = explainer(processed_features)

        # Obtener el índice de clase predicha y valores explicativos
        predicted_class_index = int(prediction)
        base_value = float(shap_values.base_values[0, predicted_class_index])
        shap_values_for_predicted_class = shap_values.values[0][:, predicted_class_index]

        # Crear diccionario de impacto de características
        feature_impact = {
            feature: float(impact) for feature, impact in zip(transformed_feature_names, shap_values_for_predicted_class)
        }

        # Crear DataFrame con datos transformados
        client_data_transformed = pd.DataFrame(processed_features, columns=transformed_feature_names)

        # Convertir datos a formato serializable
        client_data_transformed_dict = client_data_transformed.to_dict(orient="records")[0]

        # Crear explicación serializable
        explanation = {
            "prediction": int(prediction),
            "probability": probability_score,
            "base_value": base_value,
            "feature_impact": feature_impact,
            "feature_names": transformed_feature_names.tolist()
        }

        # Guardar la predicción en la base de datos con el indicador
        cursor.execute(INSERT_PREDICTION, (client_id, int(approval_indicator)))
        cursor.execute(UPDATE_IS_PROCESSED % client_id)
        conn.commit()

        # Crear la respuesta
        response = {
            "client_data": client_data.to_dict(orient="records")[0],
            "client_data_transformed": client_data_transformed_dict,
            "prediction_result": prediction_result,
            "probability": f"{probability_score * 100:.2f}%",
            "explanation": explanation
        }

        return response

    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Error al procesar la predicción: {e}")
    finally:
        conn.close()
