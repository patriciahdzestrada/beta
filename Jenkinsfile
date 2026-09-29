pipeline {
    agent any

    environment {
        DOCKER = 'C:\\Users\\mauri\\AppData\\Local\\Programs\\DockerDesktop\\resources\\bin\\docker.exe'
    }

    stages {

        stage('Build Docker Image') {
            steps {
                bat "\"${DOCKER}\" build -t pyspark-dbt-runner ."
            }
        }

        stage('PySpark ETL & Tests') {
            steps {

                bat """
                    "${DOCKER}" run --rm ^
                        -v "%WORKSPACE%:/app" ^
                        -e PYTHONPATH=/app:/opt/spark/python:/opt/spark/python/lib/py4j-0.10.9.5-src.zip ^
                        pyspark-dbt-runner ^
                        pytest tests/
                """

                bat """
                    "${DOCKER}" run --rm ^
                        -v "%WORKSPACE%:/app" ^
                        -e PYTHONPATH=/app:/opt/spark/python:/opt/spark/python/lib/py4j-0.10.9.5-src.zip ^
                        pyspark-dbt-runner ^
                        python scripts/spark_etl.py
                """
            }
        }

        stage('dbt Transformations & Tests') {
            steps {

                bat """
                    "${DOCKER}" run --rm ^
                        -v "%WORKSPACE%:/app" ^
                        -w /app/dbt_project ^
                        pyspark-dbt-runner ^
                        bash -c "dbt run --profiles-dir . && dbt test --profiles-dir ."
                """
            }
        }
    }

    post {
        always {
            cleanWs()
        }
    }
}