// Jenkinsfile
pipeline {
  agent any
  environment {
    AWS_REGION = 'eu-west-1'
    ECR_REPO   = '123456789.dkr.ecr.eu-west-1.amazonaws.com/webapp'
  }
  stages {
    stage('Checkout')    { steps { checkout scm } }
    stage('Build')       { steps { sh 'mvn clean package -DskipTests' } }
    stage('Test')        { steps { sh 'mvn test' } }
    stage('SonarQube')   { steps { withSonarQubeEnv('sonar') { sh 'mvn sonar:sonar' } } }
    stage('Push to ECR') { steps { sh 'docker build -t $ECR_REPO:$BUILD_NUMBER .' } }
    stage('Deploy EKS')  { steps { sh 'helm upgrade --install webapp helm/webapp --set image.tag=$BUILD_NUMBER' } }
  }
}
