FROM python:3.10-slim

# Instalar Java 17 (Requerido para PySpark)
RUN apt-get update && \
    apt-get install -y openjdk-21-jre-headless git && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

ENV JAVA_HOME=/usr/lib/jvm/java-21-openjdk-amd64

WORKDIR /app

COPY requirements.txt .
RUN pip install --default-timeout=300 --no-cache-dir -r requirements.txt

COPY . .

CMD ["bash"]