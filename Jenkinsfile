pipeline {
    agent any

    environment {
        PYPI_CREDENTIALS = credentials('PyPi')
    }

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
            when {
                branch 'master'
            }
            steps {
                echo 'Incrementing version number...'
                sh '''
                    source venv/bin/activate
                    pip install bump2version==1.0.0
                    bump2version patch
                    deactivate
                    '''
                echo 'Pushing version number change to SCM...'
                sh '''
                    git remote set-url origin git@github.com:evanjamesjackson/lastipy.git 
                    git push origin --tags
                    '''
            }
        }

        stage('Deploy artifacts') {
            // TODO only on master
            steps {
                echo 'Deploying artifacts...'
                // Double-quotes necessary in order for the Jenkins variables to be interpreted properly
                sh """
                    source venv/bin/activate
                    pip install setuptools
                    pip install twine
                    python setup.py sdist bdist_wheel
                    twine upload dist/* -u $env.PYPI_CREDENTIALS_USR -p $env.PYPI_CREDENTIALS_PSW
                    deactivate
                    """
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
