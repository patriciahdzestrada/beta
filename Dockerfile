FROM apache/spark-py:v3.4.0

USER root

WORKDIR /app

# Copiar e instalar las dependencias restantes (dbt, duckdb, pytest, etc.)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["bash"]