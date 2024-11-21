# 1. Elegimos la imagen base
FROM python:3.10-slim
# Aquí estamos usando una versión ligera de Python 3.10 para que nuestro contenedor sea más pequeño y rápido.

# 2. Configuramos el directorio de trabajo
WORKDIR /app
# Este comando establece que todo el trabajo que hagamos dentro del contenedor se hará en el directorio `/app`.

# 3. Copiamos los archivos de nuestro proyecto al contenedor
COPY . /app
# Esto copia todos los archivos de nuestro proyecto al directorio `/app` dentro del contenedor. 
# Nota: El punto (`.`) se refiere al directorio actual donde está el Dockerfile.

# 4. Instalamos las dependencias de Python
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r /app/requirements.txt
# Aquí estamos actualizando `pip` y luego instalando las librerías listadas en `requirements.txt`. 
# `--no-cache-dir` evita que Docker almacene archivos temporales, para ahorrar espacio.

# 5. Exponemos el puerto 8000
EXPOSE 8000
# Esto es como decirle a Docker que nuestra aplicación usará el puerto 8000. 
# Este es el puerto que usaremos para acceder a nuestra API desde el navegador o herramientas como Postman.

# 6. Indicamos cómo ejecutar la API
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
# Este es el comando que se ejecutará cuando el contenedor se inicie.
# `uvicorn` es el servidor que ejecutará nuestra API de FastAPI.
# `main:app` significa que buscará en el archivo `main.py` la instancia llamada `app`.
# `--reload` es útil en desarrollo porque recarga los cambios automáticamente.

###########

### **Cómo funciona cada paso**
#1. **Seleccionar una imagen base:** Esto es como elegir una base de trabajo. Usamos `python:3.10-slim` porque es una versión ligera y eficiente de Python.
#2. **Configurar el directorio de trabajo:** Todo lo que hagamos dentro del contenedor sucederá en el directorio `/app`. Es como establecer el escritorio donde vamos a trabajar.
#3. **Copiar los archivos:** Copiamos nuestro proyecto al contenedor. Es como meter todo en una carpeta que luego Docker usará para ejecutar la aplicación.
#4. **Instalar dependencias:** Python necesita librerías para que nuestra API funcione. Esto las instala según lo que escribimos en `requirements.txt`.
#5. **Exponer un puerto:** Esto permite que la API esté disponible en el puerto 8000, como si abriéramos una ventana para que otros programas puedan comunicarse con nuestra aplicación.
#6. **Definir el comando final:** Aquí le decimos a Docker cómo arrancar nuestra API.



### **Pasos para construir y ejecutar el contenedor**

#1. **Construir la imagen:**
#docker build -t app_credit_risk .
