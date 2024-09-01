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
                    docker.build('flask-app')
                }
            }
        }
        stage('Run') {
            steps {
                script {
                    docker.image('flask-app').run('-p 8777:5000 -v $(pwd)/Scores.txt:/app/Scores.txt --name flask-app-test')
                }
            }
        }
        stage('Test') {
            steps {
                script {
                    // Run the Selenium tests using the e2e.py script
                    try {
                        docker.image('flask-app').inside {
                            sh 'python3 e2e.py'
                        }
                    } catch (Exception err) {
                        // Fail the build if the tests fail
                        error('Selenium tests failed.')
                    }
                }
            }
        }
        stage('Finalize') {
            steps {
                script {
                    // Stop and remove the container
                    sh 'docker stop flask-app-test'
                    sh 'docker rm flask-app-test'

                    // Push the image to DockerHub
                    docker.withRegistry('https://index.docker.io/v1/', 'docker-hub-credentials') {
                        docker.image('flask-app').push('latest')
                    }
                }
            }
        }
    }
}