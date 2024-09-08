pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                // Check out the code from GitHub
                git 'https://github.com/eddieiskl/flask-app-repo.git'
            }
        }

        stage('Build') {
            steps {
                // Build the Docker image
                script {
                    sh 'docker build -t eddieiskl/flask-app:latest .'
                }
            }
        }

        stage('Run') {
            steps {
                // Stop and remove any existing container named 'flask-app'
                script {
                    sh 'docker rm -f flask-app || true'
                    // Run the Docker container with the updated port mapping
                    sh 'docker run -d -p 8777:8777 --name flask-app eddieiskl/flask-app:latest'
                }
            }
        }

        stage('Test') {
            steps {
                // Run the Selenium test
                script {
                    // Run the Selenium test inside the pipeline
                    sh 'python e2e.py'
                }
            }
        }

        stage('Finalize') {
            steps {
                // Cleanup the Docker container
                script {
                    sh 'docker rm -f flask-app'
                }
                // Push the new image to DockerHub (if needed)
                script {
                    withCredentials([string(credentialsId: 'docker-hub-credentials', variable: 'DOCKER_PASSWORD')]) {
                        sh 'echo $DOCKER_PASSWORD | docker login -u eddieiskl --password-stdin'
                        sh 'docker push eddieiskl/flask-app:latest'
                    }
                }
            }
        }
    }

    post {
        always {
            // Clean up workspace after the build is finished
            cleanWs()
        }
    }
}