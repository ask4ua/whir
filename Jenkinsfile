pipeline {
    agent none
    options {
        skipStagesAfterUnstable()
    }
    environment {
    	registry = "docker.ask4ua.com/whir-app"
    }
    stages {
        stage('Build') {
            steps {
		docker.build registry + ":latest"	
            }
        }
        stage('Test') {
            agent {
                docker {
                    image 'docker.ask4ua.com/whir-app'
                }
            }
            steps {
		sh 'python3 /app/whir/counter.py'
            }
        }
    }
}
