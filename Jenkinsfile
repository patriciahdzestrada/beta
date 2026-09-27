pipeline {
    agent any

    stages {
        stage('Build Docker Image') {
            steps {
                script {
                    sh 'docker build -t pyspark-dbt-runner .'
                }
            }
        }

        stage('PySpark ETL & Tests') {
            steps {
                script {
                    sh '''
                    docker run --rm \
                      -v ${WORKSPACE}:/app \
                      pyspark-dbt-runner \
                      pytest tests/
                    '''
                    
                    sh '''
                    docker run --rm \
                      -v ${WORKSPACE}:/app \
                      pyspark-dbt-runner \
                      python scripts/spark_etl.py
                    '''
                }
            }
        }

        stage('dbt Transformations & Tests') {
            steps {
                script {
                    sh '''
                    docker run --rm \
                      -v ${WORKSPACE}:/app \
                      -w /app/dbt_project \
                      pyspark-dbt-runner \
                      bash -c "dbt run --profiles-dir . && dbt test --profiles-dir ."
                    '''
                }
            }
        }
    }

    post {
        always {
            cleanWs()
        }
    }
}