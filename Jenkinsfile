pipeline {
    agent any
    
    environment {
        DOCKER_IMAGE = 'masteroz/zomato-flask-app'
        DOCKER_TAG = "${env.BUILD_NUMBER}"
        DOCKER_REGISTRY = 'docker.io'
        JENKINS_SERVER = '5.161.59.136:8080'
        ADMIN_EMAIL = 'hassanejaz400@gmail.com'  // Update with your admin email
    }
    
    stages {
        stage('Checkout') {
            steps {
                echo 'Checking out code from repository...'
                checkout scm
            }
        }
        
        stage('Code Quality Check') {
            steps {
                echo 'Running flake8 code quality check...'
                sh '''
                    python -m pip install flake8
                    flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
                    flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
                '''
            }
        }
        
        stage('Unit Tests') {
            steps {
                echo 'Running unit tests...'
                sh '''
                    python -m pip install -r requirements.txt
                    python -m pytest tests/ -v --cov=. --cov-report=html --cov-report=term-missing
                '''
            }
            post {
                always {
                    publishHTML([
                        allowMissing: false,
                        alwaysLinkToLastBuild: true,
                        keepAll: true,
                        reportDir: 'htmlcov',
                        reportFiles: 'index.html',
                        reportName: 'Coverage Report'
                    ])
                }
            }
        }
        
        stage('Build Docker Image') {
            steps {
                echo 'Building Docker image...'
                script {
                    def image = docker.build("${DOCKER_IMAGE}:${DOCKER_TAG}")
                    docker.withRegistry("https://${DOCKER_REGISTRY}", 'dockerhub-credentials') {
                        image.push()
                        image.push('latest')
                    }
                }
            }
        }
        
        stage('Security Scan') {
            steps {
                echo 'Running security scan on Docker image...'
                sh '''
                    docker run --rm -v /var/run/docker.sock:/var/run/docker.sock \
                    -v /tmp:/tmp aquasec/trivy image --exit-code 0 --severity HIGH,CRITICAL \
                    ${DOCKER_IMAGE}:${DOCKER_TAG}
                '''
            }
        }
    }
    
    post {
        always {
            echo 'Cleaning up workspace...'
            cleanWs()
        }
        success {
            echo 'Pipeline completed successfully!'
            emailext (
                subject: "✅ Jenkins Build Success: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                body: """
                <h2>🎉 Build Successful!</h2>
                <p><strong>Project:</strong> ${env.JOB_NAME}</p>
                <p><strong>Build Number:</strong> ${env.BUILD_NUMBER}</p>
                <p><strong>Branch:</strong> ${env.BRANCH_NAME}</p>
                <p><strong>Commit:</strong> ${env.GIT_COMMIT}</p>
                <p><strong>Docker Image:</strong> ${DOCKER_IMAGE}:${DOCKER_TAG}</p>
                <p><strong>DockerHub URL:</strong> <a href="https://hub.docker.com/r/${DOCKER_IMAGE}">https://hub.docker.com/r/${DOCKER_IMAGE}</a></p>
                <p><strong>Build URL:</strong> <a href="${env.BUILD_URL}">${env.BUILD_URL}</a></p>
                <p>✅ All tests passed and Docker image has been successfully pushed to DockerHub.</p>
                <p>🚀 The application is now ready for deployment!</p>
                """,
                to: "${ADMIN_EMAIL}",
                mimeType: 'text/html'
            )
        }
        failure {
            echo 'Pipeline failed!'
            emailext (
                subject: "❌ Jenkins Build Failed: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                body: """
                <h2>🚨 Build Failed!</h2>
                <p><strong>Project:</strong> ${env.JOB_NAME}</p>
                <p><strong>Build Number:</strong> ${env.BUILD_NUMBER}</p>
                <p><strong>Branch:</strong> ${env.BRANCH_NAME}</p>
                <p><strong>Commit:</strong> ${env.GIT_COMMIT}</p>
                <p><strong>Build URL:</strong> <a href="${env.BUILD_URL}">${env.BUILD_URL}</a></p>
                <p>❌ Please check the build logs for more details and fix the issues.</p>
                <p>🔧 Contact the development team for assistance.</p>
                """,
                to: "${ADMIN_EMAIL}",
                mimeType: 'text/html'
            )
        }
    }
}
