pipeline {
    agent none
    options {
        skipStagesAfterUnstable()
    }
    stages {
        stage('Build') {
            agent {
                docker {
                    image 'docker.ask4ua.com/whir-app'
                }
            }
            steps {
		sh 'python -m py_compile sources/add2vals.py sources/calc.py'
		
            }
        }
        stage('Test') {
            agent {
                docker {
                    image 'docker.ask4ua.com/whir-app'
                }
            }
            steps {
		sh 'python -m py_compile sources/add2vals.py sources/calc.py'
            }
        }
        stage('Deliver') { 
            agent {
                docker {
                    image 'cdrx/pyinstaller-linux:python2' 
                }
            }
            steps {
                sh 'pyinstaller --onefile sources/add2vals.py' 
            }
            post {
                success {
                    archiveArtifacts 'dist/add2vals' 
                }
            }
        }
    }
}
