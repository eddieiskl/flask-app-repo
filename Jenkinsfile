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
                    // Stop and remove any existing container before running a new one
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
                    // Stop and forcefully remove the container using the image
                    sh '''
                        container_id=$(docker ps -a -q -f ancestor=eddieiskl/flask-app:latest)
                        if [ -n "$container_id" ]; then
                            docker stop $container_id || true
                            docker rm -f $container_id || true
                        fi
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