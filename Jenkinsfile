pipeline {

    agent any

    environment {

        DOCKERHUB_USER = 'sainath1999'

        FRONTEND_IMAGE = 'sainath1999/employee-frontend:latest'
        BACKEND_IMAGE  = 'sainath1999/employee-backend:latest'

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
            }
        }


        stage('Build Docker Images') {
            steps {

                sh '''
                    echo "Building Frontend Image..."
                    docker build -t $FRONTEND_IMAGE ./frontend

                    echo "Building Backend Image..."
                    docker build -t $BACKEND_IMAGE ./backend
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
                    echo "Pushing Frontend Image..."
                    docker push $FRONTEND_IMAGE

                    echo "Pushing Backend Image..."
                    docker push $BACKEND_IMAGE
                '''
            }
        }


        stage('Deploy to AWS EC2') {
            steps {

                withCredentials([
                    sshUserPrivateKey(
                        credentialsId: 'ec2-ssh-key',
                        keyFileVariable: 'EC2_KEY',
                        usernameVariable: 'SSH_USER'
                    )
                ]) {

                    sh '''
                        chmod 600 "$EC2_KEY"

                        ssh -o StrictHostKeyChecking=no \
                        -i "$EC2_KEY" \
                        "$SSH_USER@$EC2_HOST" '

                        mkdir -p ~/employee-app

                        cat > ~/employee-app/docker-compose.yml << "EOF"

services:

  mysql:
    image: mysql:8.0
    container_name: mysql-db

    environment:
      MYSQL_ROOT_PASSWORD: root123
      MYSQL_DATABASE: employee_db

    volumes:
      - mysql-data:/var/lib/mysql

    restart: always


  backend:
    image: sainath1999/employee-backend:latest
    container_name: employee-backend

    environment:
      DB_HOST: mysql
      DB_PORT: 3306
      DB_USER: root
      DB_PASSWORD: root123
      DB_NAME: employee_db

    ports:
      - "5000:5000"

    depends_on:
      - mysql

    restart: always


  frontend:
    image: sainath1999/employee-frontend:latest
    container_name: employee-frontend

    ports:
      - "3000:80"

    depends_on:
      - backend

    restart: always


volumes:

  mysql-data:

EOF

                        cd ~/employee-app

                        echo "Stopping old containers..."
                        docker compose down || true

                        echo "Pulling latest images..."
                        docker compose pull

                        echo "Starting containers..."
                        docker compose up -d

                        echo "Checking containers..."
                        docker compose ps
                        '
                '''
                }
            }
        }


        stage('Verify Deployment') {
            steps {

                sh '''
                    echo "Waiting for application to start..."

                    sleep 20

                    echo "Checking Backend..."

                    curl --fail \
                    http://$EC2_HOST:5000/api/health

                    echo "Checking Frontend..."

                    curl --fail -I \
                    http://$EC2_HOST:3000
                '''
            }
        }
    }


    post {

        success {

            echo '========================================='
            echo 'CI/CD Pipeline Completed Successfully!'
            echo 'Application deployed successfully to AWS EC2.'
            echo 'Frontend: http://23.22.154.120:3000'
            echo 'Backend: http://23.22.154.120:5000/api/health'
            echo '========================================='
        }


        failure {

            echo 'CI/CD Pipeline Failed.'
            echo 'Check Jenkins Console Output for the error.'
        }


        always {

            sh 'docker logout || true'
        }
    }
}
