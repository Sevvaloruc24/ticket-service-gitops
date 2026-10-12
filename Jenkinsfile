pipeline {
    agent any

    environment {
        // Docker Hub üzerinde oluşturulacak repository adı
        DOCKER_HUB_REPO = 'sevvaloruc24/ticket-service'
        // Her derleme için benzersiz tag (Build numarası: 1, 2, 3...)
        IMAGE_TAG = "${env.BUILD_NUMBER}"
    }

    stages {
        // 1. Aşama: Kodları GitHub reposundan çeker
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        // 2. Aşama: Dockerfile dosyasını kullanarak container imajını derler
        stage('Build Docker Image') {
            steps {
                script {
                    echo "Docker imajı derleniyor: ${DOCKER_HUB_REPO}:${IMAGE_TAG}"
                    sh "docker build -t ${DOCKER_HUB_REPO}:${IMAGE_TAG} ."
                    sh "docker build -t ${DOCKER_HUB_REPO}:latest ."
                }
            }
        }

        // 3. Aşama: Jenkins Credentials kullanarak Docker Hub'a giriş yapar ve imajları yükler
        stage('Push to Docker Hub') {
            steps {
                script {
                    // Jenkins içerisindeki 'docker-hub-credentials' ID'li kimlik bilgisini kullanır
                    withCredentials([usernamePassword(credentialsId: 'docker-hub-credentials', passwordVariable: 'DOCKER_PASSWORD', usernameVariable: 'DOCKER_USERNAME')]) {
                        sh "echo \$DOCKER_PASSWORD | docker login -u \$DOCKER_USERNAME --password-stdin"
                        sh "docker push ${DOCKER_HUB_REPO}:${IMAGE_TAG}"
                        sh "docker push ${DOCKER_HUB_REPO}:latest"
                    }
                }
            }
        }
    }

    // Pipeline bittiğinde çalışacak adımlar
    post {
        always {
            // Güvenlik için Docker oturumunu kapatır
            sh "docker logout || true"
        }
        success {
            echo "CI Pipeline basariyla tamamlandi! Imaj Docker Hub'a yüklendi."
        }
        failure {
            echo "CI Pipeline basarisiz oldu. Lutfen loglari inceleyin."
        }
    }
}