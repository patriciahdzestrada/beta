import os
import duckdb
import pytest
from scripts.spark_etl import run_etl


def test_spark_etl_pipeline(tmp_path):
    """
    Prueba unitaria para verificar que el pipeline de PySpark ejecuta correctamente
    y genera la tabla 'ventas' en DuckDB con el cálculo de 'monto_total'.
    """
    # 1. Ejecutar la función ETL
    run_etl()

    # 2. Verificar que la base de datos DuckDB fue creada
    db_file = "analytics.duckdb"
    assert os.path.exists(db_file), "El archivo de base de datos analytics.duckdb no fue creado."

    # 3. Conectarse a DuckDB para validar el contenido
    con = duckdb.connect(db_file)
    
    # Validar número de registros cargados
    count_result = con.execute("SELECT COUNT(*) FROM raw_data.ventas").fetchone()[0]
    assert count_result == 5, f"Se esperaban 5 registros, pero se encontraron {count_result}."

    # Validar que la columna calculada por PySpark (monto_total) tiene el resultado correcto para un registro
    # Para el producto Laptop (id=1): 1 * 1200.00 = 1200.00
    laptop_monto = con.execute(
        "SELECT monto_total FROM raw_data.ventas WHERE id = 1"
    ).fetchone()[0]
    
    assert laptop_monto == 1200.00, f"El monto esperado era 1200.00, pero se obtuvo {laptop_monto}."

    con.close()