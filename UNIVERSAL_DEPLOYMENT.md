# 🌐 Universal Deployment Guide - Secure Dedalus Dashboard

## 🔐 **Security Enabled by Default**

### **Default Credentials**
- **Executive**: `admin` / `dedalus2024`
- **Operational**: `viewer` / `viewer2024`
- **Authentication**: Required for all environments
- **No anonymous access**: Login mandatory

## 🚀 **Deployment Options**

### **1. Docker Compose (Recommended)**
```bash
# Quick start with security
docker-compose up -d

# Access with authentication
http://localhost:8050
```

### **2. AWS ECS/Fargate**
```bash
# Set environment variables
export AWS_ACCOUNT_ID=123456789012
export AWS_REGION=us-east-1

# Deploy with security
chmod +x deploy-aws.sh
./deploy-aws.sh
```

### **3. Azure Container Instances**
```bash
# Set environment variables
export RESOURCE_GROUP=dedalus-rg
export REGISTRY_NAME=dedalusregistry

# Deploy with security
chmod +x deploy-azure.sh
./deploy-azure.sh
```

### **4. Any Docker Environment**
```bash
# Build and run anywhere
docker build -t dedalus-dashboard .
docker run -p 8050:8050 \
  -e SECRET_KEY=your-secret-key \
  -e DEBUG=false \
  dedalus-dashboard
```

## 🔧 **Environment Configuration**

### **Required Environment Variables**
```bash
SECRET_KEY=dedalus-dashboard-secret-key-2024
HOST=0.0.0.0
PORT=8050
DEBUG=false
```

### **Optional User Customization**
```bash
ADMIN_USERNAME=admin
ADMIN_PASSWORD=dedalus2024
VIEWER_USERNAME=viewer
VIEWER_PASSWORD=viewer2024
```

## 🎯 **Universal Compatibility**

### **Works Everywhere**
- ✅ **Local Docker** - `docker run` or `docker-compose`
- ✅ **AWS ECS/Fargate** - Container orchestration
- ✅ **Azure Container Instances** - Serverless containers
- ✅ **Google Cloud Run** - Serverless containers
- ✅ **Kubernetes** - Any K8s cluster
- ✅ **On-premises** - Any Docker host

### **Security Features**
- ✅ **Authentication required** - No anonymous access
- ✅ **Role-based access** - Executive vs Operational
- ✅ **Session management** - Secure Flask-Login
- ✅ **Environment secrets** - Configurable credentials
- ✅ **Health checks** - Built-in monitoring

## 📊 **Verification Steps**

### **1. Deploy**
```bash
# Choose your deployment method
docker-compose up -d
# OR
./deploy-aws.sh
# OR  
./deploy-azure.sh
```

### **2. Access**
```bash
# Navigate to dashboard
http://your-host:8050
```

### **3. Login**
```bash
# Executive access
Username: admin
Password: dedalus2024

# Operational access  
Username: viewer
Password: viewer2024
```

### **4. Verify Features**
- ✅ **Authentication works** - Login required
- ✅ **Default data loads** - Dashboard shows sample data
- ✅ **Role-based access** - Different views per user
- ✅ **Data import works** - Excel upload (Executive only)
- ✅ **Auto-refresh works** - Dashboard updates on import

## 🔒 **Production Security**

### **Change Default Credentials**
```bash
# Set secure passwords
export ADMIN_PASSWORD=your-secure-admin-password
export VIEWER_PASSWORD=your-secure-viewer-password
export SECRET_KEY=your-unique-secret-key
```

### **HTTPS Configuration**
```bash
# Use reverse proxy (nginx/ALB/Azure Gateway)
# Terminate SSL at load balancer level
# Dashboard runs HTTP internally
```

### **Network Security**
```bash
# AWS: Use VPC and security groups
# Azure: Use virtual networks and NSGs
# Docker: Use custom networks
```

## 🎯 **Quick Start Commands**

### **Local Development**
```bash
git clone <repository>
cd Dedalus-Tooling-Dashboard
docker-compose up -d
# Access: http://localhost:8050
```

### **AWS Production**
```bash
export AWS_ACCOUNT_ID=123456789012
./deploy-aws.sh
# Access via ALB endpoint
```

### **Azure Production**
```bash
export RESOURCE_GROUP=your-rg
export REGISTRY_NAME=your-registry
./deploy-azure.sh
# Access via provided FQDN
```

---
## ✅ **UNIVERSAL SECURE DEPLOYMENT**

**Features guaranteed in all environments:**
- 🔐 **Authentication required** - No anonymous access
- 👥 **Two user roles** - Executive and Operational
- 📊 **Full dashboard functionality** - Charts, tables, data import
- 🔄 **Auto-refresh** - Dashboard updates on data import
- 🐳 **Container ready** - Works in any Docker environment
- ☁️ **Cloud native** - AWS, Azure, GCP compatible
- 🔧 **Environment configurable** - Customizable via env vars

**Perfect secure dashboard ready for deployment anywhere!**
