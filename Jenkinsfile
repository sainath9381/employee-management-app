pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                echo 'Source code downloaded from GitHub successfully.'
            }
        }

        stage('Verify Environment') {
            steps {
                sh 'java -version'
                sh 'git --version'
                sh 'docker --version'
            }
        }

        stage('List Project Files') {
            steps {
                sh 'pwd'
                sh 'ls -la'
                sh 'find . -maxdepth 2 -type f'
            }
        }
    }

    post {
        success {
            echo 'Pipeline executed successfully!'
        }

        failure {
            echo 'Pipeline failed!'
        }
    }
}
