pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                echo 'Building...'
                bash '''#!/bin/bash
                    python3 -m venv venv
                    source venv/bin/activate
                    pip install -r requirements.txt
                '''
            }
        }
        stage('Test') {
            steps {
                echo 'Testing...'
                bash '''#!/bin/bash
                    python -m pytest test/
                '''
            }
        }
        stage('Deploy') {
            steps {
                echo 'Deploying...'
                // TODO copy the files, I guess...?
            }
        }
    }
}