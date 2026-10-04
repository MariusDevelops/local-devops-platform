pipeline {
  agent any
  environment { REGISTRY = 'localhost:5000' }

  stages {
    stage('Test backend') {
      steps {
        sh '''
          docker rm -f ci-pg || true
          docker network create ci-net || true
          docker run -d --name ci-pg --network ci-net \
            -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=todos postgres:16
          docker build --target test -t backend-test ./backend
          until docker exec ci-pg pg_isready -U postgres; do sleep 1; done
          sleep 3
          docker run --rm --network ci-net \
            -e DATABASE_URL=postgresql://postgres:postgres@ci-pg:5432/todos backend-test
        '''
      }
      post { always { sh 'docker rm -f ci-pg || true' } }
    }

    stage('Test frontend') {
      steps {
        sh '''
          docker build --target build -t frontend-test ./frontend
          docker run --rm frontend-test npm test
        '''
      }
    }

    stage('Build images') {
      steps {
        sh '''
          docker build -t $REGISTRY/todo-backend:$BUILD_NUMBER -t $REGISTRY/todo-backend:latest ./backend
          docker build -t $REGISTRY/todo-frontend:$BUILD_NUMBER -t $REGISTRY/todo-frontend:latest ./frontend
        '''
      }
    }

    stage('Push images') {
      steps {
        sh '''
          docker push --all-tags $REGISTRY/todo-backend
          docker push --all-tags $REGISTRY/todo-frontend
        '''
      }
    }
  }
}