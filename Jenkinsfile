pipeline {
    agent { label 'docker' }
    
    environment {
        SONAR_HOST = "http://192.168.1.206:9000"
        SCANNER_HOME = tool 'SonarScanner'
        PYTHONPATH = "${WORKSPACE}"
    }
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('Setup Python') {
            steps {
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                    pip install pytest pytest-cov pylint bandit httpx
                '''
            }
        }
        
        stage('Unit Tests with Coverage') {
            steps {
                sh '''
                    . venv/bin/activate
                    export PYTHONPATH="${PYTHONPATH}:${WORKSPACE}"
                    pytest tests/ \
                        --cov=app \
                        --cov-report=xml:coverage.xml \
                        --cov-report=html \
                        --junitxml=pytest-report.xml
                '''
            }
        }
        
        stage('Code Quality Analysis') {
            parallel {
                stage('Pylint') {
                    steps {
                        sh '''
                            . venv/bin/activate
                            export PYTHONPATH="${PYTHONPATH}:${WORKSPACE}"
                            pylint app/ --output-format=parseable --reports=no > pylint-report.txt || true
                        '''
                    }
                }
                stage('Security Scan') {
                    steps {
                        sh '''
                            . venv/bin/activate
                            export PYTHONPATH="${PYTHONPATH}:${WORKSPACE}"
                            bandit -r app/ -f json -o bandit-report.json || true
                        '''
                    }
                }
            }
        }
        
        stage('SonarQube Analysis') {
            steps {
                script {
                    withSonarQubeEnv('SonarQube-Homelab') {
                        sh """
                            ${SCANNER_HOME}/bin/sonar-scanner \
                                -Dsonar.projectKey=fastapi-app \
                                -Dsonar.sources=app \
                                -Dsonar.tests=tests \
                                -Dsonar.python.coverage.reportPaths=coverage.xml \
                                -Dsonar.python.xunit.reportPath=pytest-report.xml \
                                -Dsonar.python.version=3.11 \
                                -Dsonar.exclusions=**/tests/**,**/__pycache__/**
                        """
                    }
                }
            }
        }
        
        stage('Quality Gate') {
            steps {
                timeout(time: 5, unit: 'MINUTES') {
                    waitForQualityGate abortPipeline: true
                }
            }
        }
        
        stage('Build Docker Image') {
            when {
                expression { 
                    currentBuild.result == null || currentBuild.result == 'SUCCESS' 
                }
            }
            steps {
                sh '''
                    docker build -t fastapi-app:${BUILD_NUMBER} .
                '''
            }
        }
    }
    
    post {
        always {
            junit testResults: 'pytest-report.xml', allowEmptyResults: true
            publishHTML([
                allowMissing: false,
                alwaysLinkToLastBuild: true,
                keepAll: true,
                reportDir: 'htmlcov',
                reportFiles: 'index.html',
                reportName: 'Coverage Report',
                reportTitles: 'Code Coverage'
            ])
        }
        success {
            echo '✅ Pipeline completado exitosamente'
        }
        failure {
            echo '❌ Pipeline falló - Revisar logs'
        }
        cleanup {
            cleanWs()
        }
    }
}