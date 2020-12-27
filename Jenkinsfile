pipeline {
    agent any
    
    stages {
        stage('Install') {
            steps {
                echo 'Installing lastipy...'
                sh '''
                    python3 -m venv venv
                    source venv/bin/activate
                    pip install wheel
                    pip install .
                    deactivate
                    '''
            }
        }

        stage('Run tests') {
            steps {
                // TODO show test results in Jenkins?
                echo 'Running tests...'
                sh '''
                    source venv/bin/activate
                    pytest test/
                    deactivate
                    '''
            }
        }

        stage('Increment version number') {
            steps {
                // TODO only on master
                echo 'Incrementing version number...'
                sh '''
                    source venv/bin/activate
                    pip install bump2version==1.0.0
                    bump2version patch
                    deactivate
                    '''
                echo 'Pushing version number change to SCM...'
                sh '''
                    git remote add origin git@github.com:jenkins/lastipy.git 
                    git push origin --tags
                    '''
            }
        }

        stage('Deploy artifacts') {
            // TODO only on master
            // sh 'python -m twine upload dist/* -u $pypi_username -p $pypi_password'
            steps {
                echo 'Deploying artifacts...'
                sh '''
                    source venv/bin/activate
                    pip install setuptools
                    pip install twine
                    python setup.py sdist bdist_wheel
                    deactivate
                    '''
            }
        }

        // TODO post-build: post to GitHub, send an email
    }

    post {
        always {
            deleteDir()
        }
    }
}
