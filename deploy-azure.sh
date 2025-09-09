#!/bin/bash
# Azure Container Instances Deployment Script with Security

echo "🚀 Deploying Secure Dedalus Dashboard to Azure..."

# Set variables (update these for your environment)
RESOURCE_GROUP=${RESOURCE_GROUP:-dedalus-rg}
REGISTRY_NAME=${REGISTRY_NAME:-dedalusregistry}
CONTAINER_NAME=${CONTAINER_NAME:-dedalus-tooling-dashboard}
DNS_LABEL=${DNS_LABEL:-dedalus-tooling-dashboard}
LOCATION=${LOCATION:-eastus}

# Build and push to ACR
echo "📦 Building and pushing Docker image..."
az acr login --name $REGISTRY_NAME
docker build -t dedalus-tooling-dashboard .
docker tag dedalus-tooling-dashboard $REGISTRY_NAME.azurecr.io/dedalus-tooling-dashboard:latest
docker push $REGISTRY_NAME.azurecr.io/dedalus-tooling-dashboard:latest

# Deploy to Container Instances with security
echo "🚀 Deploying to Azure Container Instances..."
az container create \
  --resource-group $RESOURCE_GROUP \
  --name $CONTAINER_NAME \
  --image $REGISTRY_NAME.azurecr.io/dedalus-tooling-dashboard:latest \
  --ports 8050 \
  --dns-name-label $DNS_LABEL \
  --location $LOCATION \
  --restart-policy Always \
  --environment-variables \
    SECRET_KEY=azure-dedalus-secret-2024 \
    HOST=0.0.0.0 \
    PORT=8050 \
    DEBUG=false \
  --cpu 1 \
  --memory 1 \
  --registry-login-server $REGISTRY_NAME.azurecr.io \
  --registry-username $REGISTRY_NAME \
  --registry-password $(az acr credential show --name $REGISTRY_NAME --query "passwords[0].value" -o tsv)

# Get the FQDN
FQDN=$(az container show --resource-group $RESOURCE_GROUP --name $CONTAINER_NAME --query ipAddress.fqdn -o tsv)

echo "✅ Deployed to Azure Container Instances with security enabled"
echo "🌐 Access at: http://$FQDN:8050"
echo "🔐 Login required: admin/dedalus2024 or viewer/viewer2024"
echo "📊 Dashboard secured by default"
