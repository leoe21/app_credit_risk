import snowflake.connector
import os
from dotenv import load_dotenv

load_dotenv()

def connect_to_snowflake():
    """
    Crea una conexión segura a Snowflake usando credenciales validadas del archivo .env.
    """
    try:
        connection = snowflake.connector.connect(
            user=os.getenv("SNOWFLAKE_USER"),
            password=os.getenv("SNOWFLAKE_PASSWORD"),
            account=os.getenv("SNOWFLAKE_ACCOUNT"),
            warehouse=os.getenv("SNOWFLAKE_WAREHOUSE")
        )
        print("Conexión a Snowflake establecida correctamente.")
        return connection
    except Exception as e:
        print(f"Error al conectar con Snowflake: {e}")
        raise
