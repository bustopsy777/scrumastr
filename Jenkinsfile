pipeline {

   
  environment {
    registry = "bustopsy777/chatscrum"
    registryCredential = 'dockerhub'

  }

  agent any

  stages {

    stage('Checkout Source') {
      steps {
        git 'https://gitlab.com/bustopsy777/scrumastr.git'
      }
    }

    stage('Build image') {
      steps{
        script {
          dockerImage = docker.build registry + ":$VBUILD_NUMBER"
        }
      }
    }

    stage('Push Image') {
      steps{
        script {
          docker.withRegistry( "https://registry.hub.docker.com", registryCredential ) {
            dockerImage.push("$VBUILD_NUMBER")
            dockerImage.push('latest')
          }
        }
      }
    }

    stage('Remove Unused docker image') {
    
       steps{
         sh "docker rmi $registry:V$BUILD_NUMBER"

      }

    }     

    stage('Kubernetes Deploy') {
      steps {
        script {
          kubernetesDeploy(configs: "cs-deployment.yaml", kubeconfigId: "mykubeconfig")
        }
      }
    }
  }
}
