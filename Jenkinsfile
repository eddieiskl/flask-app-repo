pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                git 'https://github.com/eddieiskl/flask-app.git'
            }
        }
        stage('Build') {
            steps {
                script {
                    // Change directory to the location of your Dockerfile
                    sh 'cd flask-app-repo && docker build -t flask-app .'
                }
            }
        }
        stage('Run') {
            steps {
                script {
                    // Run the container and mount the Scores.txt file
                    sh 'docker run -d -p 8777:5000 -v $(pwd)/Scores.txt:/app/Scores.txt --name flask-app-test flask-app'
                }
            }
        }
        stage('Test') {
            steps {
                script {
                    // Run the selenium tests
                    sh 'python3 flask-app-repo/e2e.py'
                }
            }
        }
        stage('Finalize') {
            steps {
                script {
                    // Stop and remove the container, then push the image to DockerHub
                    sh 'docker stop flask-app-test'
                    sh 'docker rm flask-app-test'
                    withCredentials([usernamePassword(credentialsId: 'docker-hub-credentials', usernameVariable: 'DOCKER_USERNAME', passwordVariable: 'DOCKER_PASSWORD')]) {
                        sh 'docker login -u $DOCKER_USERNAME -p $DOCKER_PASSWORD'
                        sh 'docker push flask-app'
                    }
                }
            }
        }
    }
}