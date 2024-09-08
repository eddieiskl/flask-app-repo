pipeline {
    agent any

    environment {
        DOCKER_CREDENTIALS_ID = 'docker-hub-credentials'
        DOCKER_IMAGE = 'eddieiskl/flask-app:latest'
        DOCKER_CONTAINER_NAME = 'flask-app'
        GIT_URL = 'https://github.com/eddieiskl/flask-app-repo.git'
        GIT_BRANCH = 'main'
        HOST_PORT = '8777'
        CONTAINER_PORT = '8777'
        SCORES_FILE = "${WORKSPACE}/Scores.txt"  // This file will be mounted
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: "${GIT_BRANCH}", url: "${GIT_URL}"
            }
        }

        stage('Build') {
            steps {
                script {
                    withDockerServer([uri: "unix:///var/run/docker.sock"]) {
                        docker.build("${DOCKER_IMAGE}")
                    }
                }
            }
        }

        stage('Run') {
            steps {
                script {
                    withDockerServer([uri: "unix:///var/run/docker.sock"]) {
                        sh """
                        if [ -n "\$(docker ps -a -q -f name=${DOCKER_CONTAINER_NAME})" ]; then
                            docker rm -f ${DOCKER_CONTAINER_NAME}
                        fi
                        docker run -d -p ${HOST_PORT}:${CONTAINER_PORT} -v ${SCORES_FILE}:/app/Scores.txt --name ${DOCKER_CONTAINER_NAME} ${DOCKER_IMAGE}
                        """
                    }
                }
            }
        }

        stage('Test') {
            steps {
                script {
                    withDockerServer([uri: "unix:///var/run/docker.sock"]) {
                        sh """
                        python e2e.py
                        """
                    }
                }
            }
        }

        stage('Finalize') {
            steps {
                script {
                    withDockerServer([uri: "unix:///var/run/docker.sock"]) {
                        sh "docker stop ${DOCKER_CONTAINER_NAME}"
                        sh "docker rmi ${DOCKER_IMAGE} -f" // Force remove image even if it is in use by stopped container
                    }

                    withCredentials([usernamePassword(credentialsId: "${DOCKER_CREDENTIALS_ID}", passwordVariable: 'DOCKER_PASSWORD', usernameVariable: 'DOCKER_USERNAME')]) {
                        sh "echo ${DOCKER_PASSWORD} | docker login -u ${DOCKER_USERNAME} --password-stdin"
                        sh "docker push ${DOCKER_IMAGE}"
                    }
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