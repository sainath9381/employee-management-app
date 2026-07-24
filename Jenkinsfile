pipeline {
    agent any

    stages {

        stage('Checkout Code') {
            steps {
                checkout scm
            }
        }

        stage('Verify Environment') {
            steps {
                sh 'python3 --version'
                sh 'git --version'
                sh 'docker --version'
                sh 'docker compose version'
            }
        }

        stage('Build Docker Images') {
            steps {
                sh 'docker compose build'
            }
        }

        stage('Deploy Application') {
            steps {
                sh 'docker compose down || true'
                sh 'docker compose up -d'
            }
        }

        stage('Verify Running Containers') {
            steps {
                sh 'docker ps'
            }
        }

    }

    post {
        success {
            echo '========================================'
            echo ' Application deployed successfully!'
            echo '========================================'
        }

        failure {
            echo '========================================'
            echo ' Application deployment failed!'
            echo '========================================'
        }

        always {
            cleanWs()
        }
    }
}
