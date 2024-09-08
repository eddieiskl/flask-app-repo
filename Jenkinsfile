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
                    docker.build('eddieiskl/flask-app:latest')
                }
            }
        }
        stage('Run') {
            steps {
                script {
                    // Remove any existing container
                    sh '''
                        if [ "$(docker ps -a -q -f name=flask-app)" ]; then
                            docker rm -f flask-app
                        fi
                    '''
                    // Run the new container
                    sh '''
                        docker run -d -p 8777:8777 -v /Users/MacBook/.jenkins/workspace/ThePipeLine/Scores.txt:/app/Scores.txt --name flask-app eddieiskl/flask-app:latest
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
                    // Stop and forcefully remove the container
                    sh '''
                        docker stop flask-app || true
                        docker rm -f flask-app || true
                    '''

                    // List all containers and remove any using the image before removing the image
                    sh '''
                        docker ps -a | grep eddieiskl/flask-app:latest | awk '{print $1}' | xargs -r docker rm -f
                    '''

                    // Forcefully remove the Docker image
                    sh 'docker rmi -f eddieiskl/flask-app:latest || true'
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