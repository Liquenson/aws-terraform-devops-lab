cat > Jenkinsfile << 'EOF'
pipeline {
  agent any

  environment {
    AWS_REGION  = 'eu-west-1'
    AWS_ACCOUNT = credentials('aws-account-id')
    ECR_REPO    = "${AWS_ACCOUNT}.dkr.ecr.${AWS_REGION}.amazonaws.com/webapp"
  }

  stages {
    stage('Checkout') {
      steps { checkout scm }
    }
    stage('Build') {
      steps { sh 'mvn clean package -DskipTests' }
    }
    stage('Test') {
      steps { sh 'mvn test' }
    }
    stage('SonarQube') {
      steps {
        withSonarQubeEnv('sonar') { sh 'mvn sonar:sonar' }
      }
    }
    stage('Build & Push to ECR') {
      steps {
        sh '''
          aws ecr get-login-password --region $AWS_REGION | \
            docker login --username AWS --password-stdin $ECR_REPO
          docker build -t $ECR_REPO:$BUILD_NUMBER -t $ECR_REPO:latest .
          docker push $ECR_REPO:$BUILD_NUMBER
          docker push $ECR_REPO:latest
        '''
      }
    }
    stage('Deploy EKS') {
      steps {
        sh '''
          aws eks update-kubeconfig --name devops-cluster --region $AWS_REGION
          helm upgrade --install webapp helm/webapp \
            --namespace webapp \
            --create-namespace \
            --set image.repository=$ECR_REPO \
            --set image.tag=$BUILD_NUMBER \
            --wait
        '''
      }
    }
  }

  post {
    success { echo "Deploy OK: $ECR_REPO:$BUILD_NUMBER" }
    failure { echo "Fallo en stage: ${env.STAGE_NAME}" }
  }
}
EOF