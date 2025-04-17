pipeline {
    agent any

    stages {
        stage('Clone Repository') {
            steps {
                git 'https://github.com/lkassous/rooms-reservation-system.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    sh 'echo "🛠️ Building Docker image..."'
                    // Replace with actual Docker build later
                }
            }
        }

        stage('Done') {
            steps {
                echo "🚀 CI Pipeline Finished"
            }
        }
    }
}
