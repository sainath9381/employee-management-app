pipeline {

    agent any

    environment {
        DOCKERHUB_USER = 'sainath1999'

        FRONTEND_IMAGE = 'sainath1999/employee-frontend:latest'
        BACKEND_IMAGE  = 'sainath1999/employee-backend:latest'
        DATABASE_IMAGE = 'sainath1999/employee-database:latest'

        EC2_HOST = '23.22.154.120'
        EC2_USER = 'ubuntu'
    }

    stages {

        stage('Checkout Code') {
            steps {
                checkout scm
            }
        }

        stage('Verify Environment') {
            steps {
                sh 'git --version'
                sh 'docker --version'
                sh 'docker compose version'
                sh 'docker compose config'
            }
        }

        stage('Build Docker Images') {
            steps {
                sh '''
                    docker build -t $FRONTEND_IMAGE ./frontend
                    docker build -t $BACKEND_IMAGE ./backend
                    docker build -t $DATABASE_IMAGE ./database
                '''
            }
        }

        stage('Login to Docker Hub') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'dockerhub-credentials',
                        usernameVariable: 'DOCKER_USER',
                        passwordVariable: 'DOCKER_TOKEN'
                    )
                ]) {
                    sh '''
                        echo "$DOCKER_TOKEN" | docker login \
                        -u "$DOCKER_USER" \
                        --password-stdin
                    '''
                }
            }
        }

        stage('Push Images to Docker Hub') {
            steps {
                sh '''
                    docker push $FRONTEND_IMAGE
                    docker push $BACKEND_IMAGE
                    docker push $DATABASE_IMAGE
                '''
            }
        }

        stage('Deploy to AWS EC2') {
            steps {
                withCredentials([
                    sshUserPrivateKey(
                        credentialsId: 'ec2-ssh-key',
                        keyFileVariable: 'SSH_KEY',
                        usernameVariable: 'SSH_USER'
                    )
                ]) {

                    sh '''
                        ssh -o StrictHostKeyChecking=no \
                        -i "$SSH_KEY" \
                        "$SSH_USER@$EC2_HOST" \
                        "cd ~/employee-app && \
                        docker compose pull && \
                        docker compose up -d && \
                        docker compose ps"
                    '''
                }
            }
        }

        stage('Verify Deployment') {
            steps {
                sh '''
                    sleep 10

                    echo "Checking Backend..."
                    curl --fail http://$EC2_HOST:5000/api/health

                    echo "Checking Frontend..."
                    curl --fail -I http://$EC2_HOST:3000
                '''
            }
        }
    }

    post {

        success {
            echo 'CI/CD Pipeline completed successfully!'
            echo 'Application deployed successfully to AWS EC2.'
        }

        failure {
            echo 'CI/CD Pipeline failed. Check the console output.'
        }

        always {
            sh 'docker logout || true'
        }
    }
}
