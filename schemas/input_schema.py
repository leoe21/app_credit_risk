from pydantic import BaseModel, Field
from typing import Literal

class InputData(BaseModel):
    person_age: int = Field(..., ge=18, le=100, description="Age of the person")
    person_income: float = Field(..., gt=0, description="Annual income")
    person_home_ownership: Literal["RENT", "OWN", "MORTGAGE"] = Field(..., description="Home ownership status")
    person_emp_length: float = Field(..., ge=0, description="Years of employment")
    loan_intent: str = Field(..., description="Intent of the loan")
    loan_grade: str = Field(..., description="Grade of the loan")
    loan_amnt: float = Field(..., gt=0, description="Loan amount")
    loan_int_rate: float = Field(..., ge=0, description="Interest rate")
    loan_percent_income: float = Field(..., ge=0, description="Percentage of income dedicated to loan")
    cb_person_default_on_file: Literal["Y", "N"] = Field(..., description="Credit bureau default flag")
    cb_person_cred_hist_length: int = Field(..., ge=0, description="Credit history length in years")
