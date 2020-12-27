pipeline {
    agent any

    stages {
        stage('Install') {
            steps {
                echo 'Creating virtual environment...'
                bash 'python3 -m venv venv'
                bash 'source venv/bin/activate'

                echo 'Installing lastipy...'
                bash 'pip install wheel'
                bash 'pip install .'
            }
        }

        stage('Run tests') {
            steps {
                echo 'Running tests...'
            }
        }

        stage('Increment version number') {
            steps {
                echo 'Incrementing version number...'
            }
        }

        stage('Deploy artifacts') {
            steps {
                echo 'Deploying artifacts...'
            }
        }
    }
}

// #!/bin/bash

// # Exit on error
// set -e

// echo Creating virtual environment...
// python3 -m venv venv
// source venv/bin/activate

// echo

// echo Installing lastipy...
// pip install wheel
// pip install .

// echo

// echo Running tests...
// python -m pytest test/

// echo

// echo Incrementing version number...
// python -m pip install bump2version==1.0.0
// bump2version patch

// echo

// echo Deploying to pypi...
// python -m pip install setuptools
// python -m pip install twine
// python setup.py sdist bdist_wheel
// python -m twine upload dist/* -u $pypi_username -p $pypi_password

// deactivate

// Post-build: post status to GitHub, email status