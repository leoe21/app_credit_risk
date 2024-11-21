INSERT_APP_DATA = """
INSERT INTO BANK_BNC_PROD.APP_BNC_CREDIT.APP_BNC_DATA_API (
    person_age, person_income, person_home_ownership, person_emp_length, 
    loan_intent, loan_grade, loan_amnt, loan_int_rate, 
    loan_percent_income, cb_person_default_on_file, cb_person_cred_hist_length
) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
"""

SELECT_ENRICHED_DATA = """
SELECT * FROM BANK_BNC_PROD.bcn_credit_risk.calculate_feature_new_client;
"""

# Insertar predicciones en la tabla
INSERT_PREDICTION = """
INSERT INTO BANK_BNC_PROD.APP_BNC_CREDIT.APP_BNC_PREDICTIONS (id, prediction)
VALUES (%s, %s);
"""

# Actualizar el estado de los datos procesados
UPDATE_IS_PROCESSED = """
UPDATE BANK_BNC_PROD.APP_BNC_CREDIT.APP_BNC_DATA_API
SET IS_PROCESSED = TRUE
WHERE ID IN (%s);
"""

GET_FEATURES_BY_ID = """
SELECT *
FROM BANK_BNC_PROD.bcn_credit_risK.calculate_feature_new_client
WHERE id = {client_id};
"""