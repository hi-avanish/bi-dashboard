#!/bin/bash
# Build and Push to Docker Hub

echo "🐳 Building and pushing Dedalus Tooling Dashboard to Docker Hub..."

# Docker Hub configuration
DOCKER_USERNAME="hello2avanish"
IMAGE_NAME="dedalus-tooling-dashboard"
TAG="latest"

# Build the image
echo "📦 Building Docker image..."
docker build -t $DOCKER_USERNAME/$IMAGE_NAME:$TAG .

# Tag with version if provided
if [ ! -z "$1" ]; then
    echo "🏷️ Tagging with version: $1"
    docker tag $DOCKER_USERNAME/$IMAGE_NAME:$TAG $DOCKER_USERNAME/$IMAGE_NAME:$1
fi

# Login to Docker Hub (you'll be prompted for credentials)
echo "🔐 Logging into Docker Hub..."
docker login

# Push the image
echo "🚀 Pushing to Docker Hub..."
docker push $DOCKER_USERNAME/$IMAGE_NAME:$TAG

# Push version tag if created
if [ ! -z "$1" ]; then
    docker push $DOCKER_USERNAME/$IMAGE_NAME:$1
fi

echo "✅ Successfully pushed to Docker Hub!"
echo "📋 Image available at: https://hub.docker.com/r/$DOCKER_USERNAME/$IMAGE_NAME"
echo "🐳 Pull command: docker pull $DOCKER_USERNAME/$IMAGE_NAME:$TAG"
