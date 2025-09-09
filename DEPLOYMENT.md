# 🚀 Dedalus Dashboard - Docker Deployment Guide

## 🐳 **Quick Docker Deployment**

### **Local Docker**
```bash
# Build and run
docker build -t dedalus-dashboard .
docker run -p 8050:8050 dedalus-dashboard

# Or use docker-compose
docker-compose up -d
```

### **Access Dashboard**
- **URL**: http://localhost:8050
- **Health Check**: http://localhost:8050/health

## ☁️ **Cloud Deployment**

### **AWS (ECS/Fargate)**
1. **Setup ECR Repository**
   ```bash
   aws ecr create-repository --repository-name dedalus-dashboard
   ```

2. **Deploy**
   ```bash
   # Update YOUR_ACCOUNT in deploy-aws.sh
   chmod +x deploy-aws.sh
   ./deploy-aws.sh
   ```

### **Azure (Container Instances)**
1. **Setup ACR**
   ```bash
   az acr create --resource-group myResourceGroup --name myRegistry --sku Basic
   ```

2. **Deploy**
   ```bash
   # Update YOUR_REGISTRY in deploy-azure.sh
   chmod +x deploy-azure.sh
   ./deploy-azure.sh
   ```

### **Any Cloud Provider**
```bash
# Generic deployment
docker build -t dedalus-dashboard .
docker run -d -p 8050:8050 --name dedalus-dashboard dedalus-dashboard
```

## 🔧 **Environment Variables**
- `PORT`: Server port (default: 8050)
- `HOST`: Server host (default: 0.0.0.0)
- `DEBUG`: Debug mode (default: False)

## 📊 **Features**
- **Zero dependencies** - Self-contained Docker image
- **Health checks** - Built-in monitoring
- **Production ready** - Optimized for cloud deployment
- **Multi-cloud** - Works on AWS, Azure, GCP, or any Docker host

---
**Ready for production deployment anywhere!**
