pipeline {
    agent any

    options {
        disableConcurrentBuilds()
    }

    stages {
        stage('Checkout'){
            steps {
                checkout scm
            }
        }
        stage('Linting') {
            steps {
                script {
                    sh "ruff check .";
                }
            }
        }
        stage('Sync github repo') {
            when { branch 'master' }
            steps {
                syncRemoteBranch('git@github.com:nbr23/wyoming-piper-http-bridge.git', 'master')
            }
        }
    }
}
