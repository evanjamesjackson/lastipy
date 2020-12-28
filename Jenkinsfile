pipeline {
    agent any

    environment {
        PYPI_API_KEY = credentials('PyPi')
    }

    stages {
        stage('Initialize') {
            steps {
                script {
                    def gitCommitAuthor = sh(script: 'git log -1 --pretty=format:\'%an\'', returnStdout: true)
                    echo "Last commit was made by ${gitCommitAuthor}"
                    if (gitCommitAuthor.toLowerCase().contains('jenkins')) {
                        currentBuild.result = 'ABORTED'
                        error('Last commit was made by Jenkins itself, therefore aborting the build to prevent an endless loop')
                    }
                }
            }
        }

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
                    pytest --junitxml results.xml test/
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
                sh """
                    git push git@github.com:evanjamesjackson/lastipy.git HEAD:$env.BRANCH_NAME --follow-tags
                    """
            }
        }

        stage('Deploy artifacts') {
            when {
                branch 'master'
            }
            steps {
                echo 'Deploying artifacts...'
                // Double-quotes necessary in order for the Jenkins variables to be interpreted properly
                sh """
                    source venv/bin/activate
                    pip install setuptools
                    pip install twine
                    python setup.py sdist bdist_wheel
                    twine upload dist/* -u __token__ -p $env.PYPI_API_KEY
                    deactivate
                    """
            }
        }
    }

    post {
        always {
            junit 'results.xml'
            deleteDir()
        }
        success {
            setGitHubCommitStatus("Build succeeded", "SUCCESS")
            sendStatusEmail()
        }
        failure {
            setGitHubCommitStatus("Build failed", "FAILURE")
            sendStatusEmail()
        }
    }
}

// TODO this doesn't appear to be working
void sendStatusEmail() {
    emailext body: "${currentBuild.currentResult}: Job ${env.JOB_NAME} build ${env.BUILD_NUMBER}\n More info at: ${env.BUILD_URL}",
             recipientProviders: [[$class: 'DevelopersRecipientProvider'], [$class: 'RequesterRecipientProvider']],
             subject: "Jenkins Build ${currentBuild.currentResult}: Job ${env.JOB_NAME}"
}

void setGitHubCommitStatus(String message, String state) {
  step([
      $class: "GitHubCommitStatusSetter",
      reposSource: [$class: "ManuallyEnteredRepositorySource", url: env.GIT_URL],
      contextSource: [$class: "ManuallyEnteredCommitContextSource", context: "ci/jenkins/build-status"],
      errorHandlers: [[$class: "ChangingBuildStatusErrorHandler", result: "UNSTABLE"]],
      statusResultSource: [ $class: "ConditionalStatusResultSource", results: [[$class: "AnyBuildResult", message: message, state: state]] ]
  ]);
}
