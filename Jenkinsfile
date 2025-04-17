pipeline {
    agent any

    stages {
        stage('Cloner le dépôt') {
            steps {
                git 'https://github.com/lkassous/rooms-reservation-system.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    dir('user-service') {
                        sh 'docker build -t user-service:latest .'
                    }
                }
            }
        }

        stage('Terminé') {
            steps {
                echo "🎉 L'image Docker a été créée avec succès !"
            }
        }
    }
}

