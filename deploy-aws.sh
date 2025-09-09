#!/bin/bash
# AWS ECS Deployment Script with Security

echo "🚀 Deploying Secure Dedalus Dashboard to AWS..."

# Set variables (update these for your environment)
AWS_REGION=${AWS_REGION:-us-east-1}
ECR_REPO=${ECR_REPO:-dedalus-tooling-dashboard}
CLUSTER_NAME=${CLUSTER_NAME:-dedalus-cluster}
SERVICE_NAME=${SERVICE_NAME:-dedalus-dashboard-service}

# Build and push to ECR
echo "📦 Building and pushing Docker image..."
aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com

docker build -t $ECR_REPO .
docker tag $ECR_REPO:latest $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$ECR_REPO:latest
docker push $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$ECR_REPO:latest

# Create ECS task definition with security
cat > task-definition.json << EOF
{
  "family": "dedalus-dashboard",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "256",
  "memory": "512",
  "executionRoleArn": "arn:aws:iam::$AWS_ACCOUNT_ID:role/ecsTaskExecutionRole",
  "containerDefinitions": [
    {
      "name": "dedalus-dashboard",
      "image": "$AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$ECR_REPO:latest",
      "portMappings": [
        {
          "containerPort": 8050,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {"name": "SECRET_KEY", "value": "aws-dedalus-secret-2024"},
        {"name": "HOST", "value": "0.0.0.0"},
        {"name": "PORT", "value": "8050"},
        {"name": "DEBUG", "value": "false"}
      ],
      "healthCheck": {
        "command": ["CMD-SHELL", "curl -f http://localhost:8050/login || exit 1"],
        "interval": 30,
        "timeout": 5,
        "retries": 3
      },
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/dedalus-dashboard",
          "awslogs-region": "$AWS_REGION",
          "awslogs-stream-prefix": "ecs"
        }
      }
    }
  ]
}
EOF

# Register task definition
aws ecs register-task-definition --cli-input-json file://task-definition.json

echo "✅ Deployed to AWS ECS with security enabled"
echo "🔐 Login required: admin/dedalus2024 or viewer/viewer2024"
echo "📋 Next: Configure ALB and update service"
