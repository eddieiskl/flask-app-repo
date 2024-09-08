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
                    docker.build("eddieiskl/flask-app:latest")
                }
            }
        }
        stage('Run') {
            steps {
                script {
                    // Ensure port 8777 is used here
                    sh 'docker run -d -p 8777:8777 --name flask-app eddieiskl/flask-app:latest'
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
                    sh 'docker stop flask-app'
                    sh 'docker rm flask-app'
                    docker.withRegistry('https://index.docker.io/v1/', 'docker-hub-credentials') {
                        docker.image("eddieiskl/flask-app:latest").push()
                    }
                }
            }
        }
    }
}