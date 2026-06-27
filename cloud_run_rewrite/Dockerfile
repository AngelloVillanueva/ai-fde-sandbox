# PASO 1 — Imagen base (SO + Python preinstalado)
FROM python:3.12-slim

# PASO 2 — Dónde trabajar dentro del contenedor
WORKDIR /cloud_run_rewrite

# PASO 3 — Dependencias (capa cacheable: cambia poco)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# PASO 4 — Tu código
COPY src/ ./src/
COPY config/ ./config/

# PASO 5 — Puerto que escucha el proceso
EXPOSE 8080

# PASO 6 — Comando al arrancar el contenedor
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8080"]