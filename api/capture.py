from fastapi import APIRouter, HTTPException
from schemas.input_schema import InputData
from database.connection import connect_to_snowflake
from database.queries import INSERT_APP_DATA

router = APIRouter()

@router.post("/")
async def capture_data(data: InputData):
    """
    Recibe datos crudos desde la aplicación y los guarda en Snowflake.
    """
    conn = connect_to_snowflake()
    cursor = conn.cursor()
    
    try:
        cursor.execute(INSERT_APP_DATA, tuple(data.dict().values()))
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail="An error occurred while saving the data.")
    finally:
        conn.close()
    
    return {"message": "Data captured successfully."}
