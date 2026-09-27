import os
import duckdb
from pyspark.sql import SparkSession
from pyspark.sql.functions import col

def run_etl():
    # 1. Inicializar sesión de PySpark
    spark = SparkSession.builder \
        .appName("ETL_PySpark_DuckDB") \
        .master("local[*]") \
        .getOrCreate()

    # 2. Leer archivo CSV
    raw_path = os.path.join("data", "raw_sales.csv")
    df = spark.read.csv(raw_path, header=True, inferSchema=True)

    # 3. Limpieza y transformación pesada con PySpark
    df_clean = df.dropna().dropDuplicates()
    df_transformed = df_clean.withColumn(
        "monto_total", col("cantidad") * col("precio_unitario")
    )

    # 4. Convertir a Pandas para escribir en DuckDB (Warehouse Local)
    pandas_df = df_transformed.toPandas()
    
    con = duckdb.connect("analytics.duckdb")
    con.execute("CREATE SCHEMA IF NOT EXISTS raw_data")
    con.register("df_spark", pandas_df)
    con.execute("CREATE OR REPLACE TABLE raw_data.ventas AS SELECT * FROM df_spark")
    con.close()

    spark.stop()

if __name__ == "__main__":
    run_etl()