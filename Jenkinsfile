pipeline {
    agent any

    stages {
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
                echo "🎉 L\'image Docker a été créée avec succès !"
            }
        }
    }
}

