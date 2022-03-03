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

                updateGitlabCommitStatus(name: 'Backend documentation: Clean', state: 'success')
                catchError(buildResult: 'SUCCESS', stageResult: 'FAILURE') {
                    sh 'sudo rm -r /var/www/documentation/*'
                }
                updateGitlabCommitStatus(name: 'Backend documentation: Clean', state: 'success')
            }
        }

        stage('Build') {
            steps {
                updateGitlabCommitStatus(name: 'Frontend: Build', state: 'running')
                dir('frontend/') {
                    sh 'npm install && npm run build'
                }
                updateGitlabCommitStatus(name: 'Frontend: Build', state: 'success')

                updateGitlabCommitStatus(name: 'Backend documentation: Build', state: 'running')
                dir('backend/') {
                    sh 'mkdocs build'
                }
                updateGitlabCommitStatus(name: 'Backend documentation: Build', state: 'success')
            }
        }

        stage('Deploy') {
            steps {
                updateGitlabCommitStatus(name: 'Frontend: Deploy', state: 'running')
                dir('frontend/') {
                    sh 'sudo mv build/* /var/www/app/'
                }
                updateGitlabCommitStatus(name: 'Frontend: Deploy', state: 'success')

                updateGitlabCommitStatus(name: 'Backend documentation: Deploy', state: 'running')
                dir('backend/') {
                    sh 'sudo mv site/* /var/www/documentation/'
                }
                updateGitlabCommitStatus(name: 'Backend documentation: Deploy', state: 'success')
            }
        }
    }
    
}
