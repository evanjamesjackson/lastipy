pipeline {
    agent any

    stages {
        stage('Install') {
            steps {
                echo 'Creating virtual environment...'
                sh 'python3 -m venv venv'
                sh 'source venv/bin/activate'

                echo 'Installing lastipy...'
                sh 'pip install wheel'
                sh 'pip install .'

                sh 'deactivate'
            }
        }

        stage('Run tests') {
            steps {
                echo 'Running tests...'
                sh 'source venv/bin/activate'
                sh 'pytest test/'
                // TODO show test results in a nice way?
                sh 'deactivate'
            }
        }

        stage('Increment version number') {
            steps {
                // TODO only on master
                echo 'Incrementing version number...'
                sh 'source venv/bin/activate'
                sh 'pip install bump2version==1.0.0'
                sh 'bump2version patch'
                // TODO push to git
                // TODO tagging?
                sh 'deactivate'
            }
        }

        stage('Deploy artifacts') {
            steps {
                // TODO only on master
                echo 'Deploying artifacts...'
                sh 'source venv/bin/activate'
                sh 'python3 -m pip install setuptools'
                sh 'python3 -m pip install twine'
                sh 'python3 setup.py sdist bdist_wheel'
                // sh 'python -m twine upload dist/* -u $pypi_username -p $pypi_password'
                sh 'deactivate'
            }
        }

        // TODO post-build: post to GitHub, send an email
    }
}
