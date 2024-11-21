SELECT
    id,
    person_age,
    person_income,
    person_home_ownership,
    person_emp_length,
    loan_intent,
    loan_grade,
    loan_amnt,
    loan_int_rate,
    loan_percent_income,
    cb_person_default_on_file,
    cb_person_cred_hist_length,
    -- 1. Clasificación de edad
    CASE
        WHEN person_age <= 25 THEN 'Joven'
        WHEN person_age BETWEEN 26
        AND 35 THEN 'Adulto'
        ELSE 'Mayor'
    END AS age_group,
    -- 2. Relación préstamo/ingreso
    loan_amnt / person_income AS loan_to_income_ratio,
    -- 3. Duración del empleo categorizada
    CASE
        WHEN person_emp_length = 0 THEN 'Desempleado'
        WHEN person_emp_length BETWEEN 1
        AND 3 THEN 'Poca experiencia'
        WHEN person_emp_length BETWEEN 4
        AND 7 THEN 'Experiencia moderada'
        ELSE 'Alta experiencia'
    END AS emp_length_category,
    -- 4. Nivel de riesgo por tasa de interés
    CASE
        WHEN loan_int_rate < 10 THEN 'Bajo'
        WHEN loan_int_rate BETWEEN 10
        AND 15 THEN 'Moderado'
        ELSE 'Alto'
    END AS interest_rate_risk,
    -- 5. Historial crediticio categorizado
    CASE
        WHEN cb_person_cred_hist_length < 3 THEN 'Corto'
        WHEN cb_person_cred_hist_length BETWEEN 3
        AND 7 THEN 'Medio'
        ELSE 'Largo'
    END AS credit_history_category,
    -- 6. Categorías por tipo de vivienda
    CASE
        WHEN person_home_ownership IN ('OWN', 'MORTGAGE') THEN 'Propietario'
        ELSE 'Arrendatario'
    END AS home_ownership_group,
    -- 7. Indicador de alto endeudamiento
    CASE
        WHEN loan_percent_income > 0.5 THEN 1
        ELSE 0
    END AS high_debt_indicator,
    -- 8. Relación duración préstamo vs historial crediticio
    cb_person_cred_hist_length - person_emp_length AS credit_vs_loan_duration,
    -- 10. Categorías por intención de préstamo
    CASE
        WHEN loan_intent IN ('EDUCATION', 'MEDICAL') THEN 'Educación/Salud'
        WHEN loan_intent = 'VENTURE' THEN 'Negocios'
        WHEN loan_intent IN ('PERSONAL', 'HOMEIMPROVEMENT') THEN 'Personal'
        WHEN loan_intent = 'DEBTCONSOLIDATION' THEN 'Deuda'
        ELSE 'Otros'
    END AS loan_intent_category,
    -- 11. Nivel de confianza en historial crediticio
    CASE
        WHEN cb_person_default_on_file = 'Y' THEN 'Bajo'
        WHEN cb_person_cred_hist_length >= 7 THEN 'Alto'
        ELSE 'Moderado'
    END AS credit_confidence_level,
    -- 12. Tasa ajustada por riesgo
    loan_int_rate * (1 + loan_percent_income) AS adjusted_interest_rate,
    -- 13. Capacidad de ahorro estimada
    (person_income - loan_amnt) / 12 AS estimated_savings,
    -- 14. Duración laboral simplificada
    CASE
        WHEN person_emp_length < 2 THEN 'Principiante'
        WHEN person_emp_length BETWEEN 2
        AND 5 THEN 'Intermedio'
        ELSE 'Experto'
    END AS simplified_emp_length,
    -- 15. Nivel de préstamo basado en categoría
    CASE
        WHEN loan_amnt < 10000 THEN 'Bajo'
        WHEN loan_amnt BETWEEN 10000
        AND 30000 THEN 'Medio'
        ELSE 'Alto'
    END AS loan_amount_category,
    -- 16. Riesgo combinado de vivienda y empleo
    CASE
        WHEN person_home_ownership IN ('RENT', 'OTHER')
        AND person_emp_length < 3 THEN 'Alto'
        WHEN person_home_ownership IN ('OWN', 'MORTGAGE')
        AND person_emp_length >= 5 THEN 'Bajo'
        ELSE 'Moderado'
    END AS housing_employment_risk,
    -- 17. Categoría de edad para riesgos
    CASE
        WHEN person_age <= 25
        AND loan_int_rate > 15 THEN 'Joven-AltoRiesgo'
        WHEN person_age > 25
        AND loan_int_rate <= 10 THEN 'Mayor-BajoRiesgo'
        ELSE 'Moderado'
    END AS age_interest_risk,
    -- 18. Días pendientes de deuda estimados
    loan_amnt / (person_income / 12) * 30 AS estimated_days_to_clear_debt,
    -- 19. Indicador de capacidad de pago temprana
    CASE
        WHEN loan_amnt <= person_income * 2 THEN 1
        ELSE 0
    END AS early_payment_capability,
    -- 20. Intensidad del préstamo
    loan_amnt * loan_int_rate / (person_emp_length + 1) AS loan_intensity_score,
    CASE
        WHEN person_income < 20000 THEN 'Bajo'
        WHEN person_income BETWEEN 20000
        AND 50000 THEN 'Medio'
        WHEN person_income BETWEEN 50001
        AND 100000 THEN 'Alto'
        ELSE 'Muy alto'
    END AS income_range,
    (person_income / loan_amnt) AS financial_stability_ratio,
    CASE
        WHEN person_home_ownership = 'RENT'
        AND loan_percent_income > 0.5 THEN 'Alto riesgo en alquiler'
        WHEN person_home_ownership = 'OWN'
        AND loan_percent_income <= 0.5 THEN 'Bajo riesgo como propietario'
        ELSE 'Moderado'
    END AS housing_debt_risk,
    loan_int_rate / (person_emp_length + 1) AS interest_rate_adjusted_by_employment,
    (person_income / 12) - (loan_percent_income * (person_income / 12)) AS available_monthly_payment,
    CASE
        WHEN cb_person_default_on_file = 'Y'
        AND cb_person_cred_hist_length < 3 THEN 'Riesgo extremo'
        WHEN cb_person_default_on_file = 'N'
        AND cb_person_cred_hist_length >= 7 THEN 'Riesgo bajo'
        ELSE 'Riesgo moderado'
    END AS credit_risk_combined,
    loan_amnt * loan_int_rate / person_income AS overall_loan_risk,
    (loan_amnt / person_income) * 100 AS annual_income_dedicated_to_loan,
    CASE
        WHEN loan_percent_income < 0.4 THEN 'Sostenible'
        ELSE 'Insostenible'
    END AS loan_sustainability,
    loan_amnt * (1 + (loan_int_rate / 100)) AS total_loan_cost,
    CASE
        WHEN person_age < 25
        AND cb_person_cred_hist_length < 3 THEN 'Riesgo alto'
        WHEN person_age >= 25
        AND cb_person_cred_hist_length >= 7 THEN 'Riesgo bajo'
        ELSE 'Riesgo moderado'
    END AS age_credit_risk
FROM
    BANK_BNC_PROD.APP_BNC_CREDIT.APP_BNC_DATA_API
    WHERE IS_PROCESSED = FALSE;