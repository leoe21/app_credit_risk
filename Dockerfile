# Usa una imagen base de Python
FROM python:3.9-slim

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia el archivo de requerimientos al contenedor
COPY requirements.txt ./requirements.txt

# Instala las dependencias necesarias
RUN pip install --no-cache-dir -r requirements.txt

# Copia los archivos de la aplicación al contenedor
COPY . .

# Expone el puerto por defecto de Streamlit
EXPOSE 8501

# Comando para ejecutar la aplicación Streamlit
CMD ["streamlit", "run", "app.py"]
