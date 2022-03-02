pipeline {
    agent any

    stages {   
        stage('Clean') {
            steps {
                updateGitlabCommitStatus(name: 'Frontend: Clean', state: 'running')
                
                catchError(buildResult: 'SUCCESS', stageResult: 'FAILURE') {
                    sh 'sudo rm -r /var/www/app/*'
                }

                updateGitlabCommitStatus(name: 'Frontend: Clean', state: 'success')
            }
        }

        stage('Build') {
            steps {
                updateGitlabCommitStatus(name: 'Frontend: Build', state: 'running')

                dir('frontend/') {
                    sh 'npm install && npm run build'
                }

                updateGitlabCommitStatus(name: 'Frontend: Build', state: 'success')
            }
        }

        stage('Deploy') {
            steps {
                updateGitlabCommitStatus(name: 'Frontend: Deploy', state: 'running')

                dir('frontend/') {
                    sh 'sudo mv build/* /var/www/app/'
                }

                updateGitlabCommitStatus(name: 'Frontend: Deploy', state: 'success')
            }
        }
    }
    
}
