# Dockerfile para App Info Service
# Imagen optimizada para Cloud Run

FROM python:3.11-slim

WORKDIR /app

# Copiar requirements e instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código de la aplicación
COPY app.py .

# Cloud Run requiere que la aplicación escuche en el puerto definido por PORT
# El puerto se configura automáticamente por Cloud Run
#ENV PORT=8080

# Exponer puerto (documentación, Cloud Run lo maneja automáticamente)
EXPOSE 8080

# Comando para ejecutar la aplicación
# Usar flask run en lugar de python app.py para mejor compatibilidad
CMD ["python", "app.py"]

