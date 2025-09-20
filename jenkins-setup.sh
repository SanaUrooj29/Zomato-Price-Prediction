#!/bin/bash

# Jenkins CI/CD Setup Script for Flask Zomato App
# Updated for your specific server and branch structure

set -e

echo "🐳 Setting up Jenkins CI/CD Pipeline for 5.161.59.136:8080..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    print_error "Docker is not running. Please start Docker first."
    exit 1
fi

# Stop existing containers if they exist
print_status "Stopping existing Jenkins containers..."
docker stop jenkins-server jenkins-docker 2>/dev/null || true
docker rm jenkins-server jenkins-docker 2>/dev/null || true

# Create Jenkins network
print_status "Creating Jenkins network..."
docker network create jenkins 2>/dev/null || true

# Create Docker-in-Docker container
print_status "Starting Docker-in-Docker container..."
docker run \
  --name jenkins-docker \
  --rm \
  --detach \
  --privileged \
  --network jenkins \
  --network-alias docker \
  --env DOCKER_TLS_CERTDIR=/certs \
  --volume jenkins-docker-certs:/certs/client \
  --volume jenkins-data:/var/jenkins_home \
  --publish 2376:2376 \
  docker:dind \
  --storage-driver overlay2

# Start Jenkins server
print_status "Starting Jenkins server..."
docker run \
  --name jenkins-server \
  --rm \
  --detach \
  --network jenkins \
  --env DOCKER_HOST=tcp://docker:2376 \
  --env DOCKER_CERT_PATH=/certs/client \
  --env DOCKER_TLS_VERIFY=1 \
  --publish 8080:8080 \
  --publish 50000:50000 \
  --volume jenkins-data:/var/jenkins_home \
  --volume jenkins-docker-certs:/certs/client:ro \
  --volume /var/run/docker.sock:/var/run/docker.sock \
  jenkins/jenkins:lts

# Wait for Jenkins to start
print_status "Waiting for Jenkins to start..."
sleep 30

# Get initial admin password
print_status "Getting Jenkins initial admin password..."
ADMIN_PASSWORD=$(docker exec jenkins-server cat /var/jenkins_home/secrets/initialAdminPassword 2>/dev/null || echo "Password not available yet")

print_success "Jenkins setup completed!"
echo ""
echo "🌐 Access Jenkins at: http://5.161.59.136:8080"
echo "🔑 Initial Admin Password: $ADMIN_PASSWORD"
echo ""
echo "📋 Your Branch Structure:"
echo "  • master: No direct pushes, requires PR from test"
echo "  • test: No direct pushes, requires PR, triggers GitHub Actions"
echo "  • Jenkins: Monitors test branch for CI/CD"
echo ""
echo "📋 Next Steps:"
echo "1. Access Jenkins web interface at http://5.161.59.136:8080"
echo "2. Install suggested plugins"
echo "3. Create admin user"
echo "4. Install additional plugins: Git, Docker, Email Extension"
echo "5. Configure DockerHub credentials (username: masteroz)"
echo "6. Create pipeline job using the Jenkinsfile"
echo "7. Configure GitHub webhook for test branch"
echo ""
echo "🔧 Useful Commands:"
echo "  View logs: docker logs jenkins-server"
echo "  Stop Jenkins: docker stop jenkins-server jenkins-docker"
echo "  Restart: ./jenkins-setup.sh"
echo ""
echo "📧 GitHub Webhook URL:"
echo "  http://5.161.59.136:8080/github-webhook/"