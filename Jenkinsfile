pipeline {
    agent any
    environment {
        DOCKER_IMAGE = 'eddieiskl/flask-app:latest'
        CONTAINER_NAME = 'flask-app'
    }
    stages {
        stage('Checkout') {
            steps {
                git 'https://github.com/eddieiskl/flask-app-repo.git'
            }
        }
        stage('Build') {
            steps {
                script {
                    docker.build(DOCKER_IMAGE)
                }
            }
        }
        stage('Run') {
            steps {
                script {
                    // Clean up any existing container
                    sh '''
                    CONTAINER_ID=$(docker ps -a -q -f name=${CONTAINER_NAME})
                    if [ -n "$CONTAINER_ID" ]; then
                        docker rm -f ${CONTAINER_NAME}
                    fi
                    docker run -d -p 8777:8777 -v ${WORKSPACE}/Scores.txt:/app/Scores.txt --name ${CONTAINER_NAME} ${DOCKER_IMAGE}
                    '''
                }
            }
        }
        stage('Test') {
            steps {
                script {
                    sh 'python e2e.py'
                }
            }
        }
        stage('Finalize') {
            steps {
                script {
                    // Stop the container and wait for it to stop before removing the image
                    sh '''
                    docker stop ${CONTAINER_NAME}
                    while docker ps -a --filter "name=${CONTAINER_NAME}" --filter "status=running" | grep -q ${CONTAINER_NAME}; do
                        echo "Waiting for container to stop..."
                        sleep 2
                    done
                    docker rmi -f ${DOCKER_IMAGE}
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