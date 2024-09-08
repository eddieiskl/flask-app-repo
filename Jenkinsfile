pipeline {
    agent any
    stages {
        stage('Checkout') {
            steps {
                git 'https://github.com/eddieiskl/flask-app-repo.git'
            }
        }
        stage('Build') {
            steps {
                script {
                    // Build the Docker image
                    docker.build('eddieiskl/flask-app:latest')
                }
            }
        }
        stage('Run') {
            steps {
                script {
                    // Stop and remove any existing container with the name 'flask-app'
                    sh '''
                        if [ "$(docker ps -a -q -f name=flask-app)" ]; then
                            docker rm -f flask-app
                        fi
                    '''
                    // Run the container
                    sh '''
                        docker run -d -p 8777:8777 -v /Users/MacBook/.jenkins/workspace/ThePipeLine/Scores.txt:/app/Scores.txt --name flask-app eddieiskl/flask-app:latest
                    '''
                }
            }
        }
        stage('Test') {
            steps {
                script {
                    // Run the test script
                    sh 'python e2e.py'
                }
            }
        }
        stage('Finalize') {
            steps {
                script {
                    // Stop the container if it exists
                    sh '''
                        if [ "$(docker ps -q -f name=flask-app)" ]; then
                            docker stop flask-app
                        fi
                    '''
                    // Remove the container after stopping
                    sh '''
                        if [ "$(docker ps -a -q -f name=flask-app)" ]; then
                            docker rm flask-app
                        fi
                    '''
                    // Forcefully remove the image after the container is removed
                    sh '''
                        if [ "$(docker images -q eddieiskl/flask-app:latest)" ]; then
                            docker rmi -f eddieiskl/flask-app:latest
                        fi
                    '''
                }
            }
        }
    }
    post {
        always {
            cleanWs() // Clean up workspace after every build
        }
    }
}