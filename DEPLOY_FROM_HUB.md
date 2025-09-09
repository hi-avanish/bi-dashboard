# 🚀 Deploy from Docker Hub

## 📦 **Image Available**
- **Registry**: https://hub.docker.com/r/hello2avanish/dedalus-dashboard
- **Image**: `hello2avanish/dedalus-dashboard:latest`

## 🎯 **Quick Deploy Commands**

### **1. Simple Run**
```bash
docker pull hello2avanish/dedalus-dashboard:latest
docker run -p 8050:8050 hello2avanish/dedalus-dashboard:latest
```

### **2. Docker Compose (Recommended)**
```bash
# Download compose file
curl -O https://raw.githubusercontent.com/your-repo/docker-compose.hub.yml

# Run with Docker Compose
docker-compose -f docker-compose.hub.yml up -d
```

### **3. Production Deployment**
```bash
docker run -d -p 8050:8050 \
  --name dedalus-dashboard \
  -e SECRET_KEY=your-production-secret \
  -e ADMIN_PASSWORD=your-secure-password \
  -e VIEWER_PASSWORD=your-viewer-password \
  --restart unless-stopped \
  hello2avanish/dedalus-dashboard:latest
```

## 🔐 **Access Dashboard**
- **URL**: http://localhost:8050
- **Login**: admin/dedalus2024 or viewer/viewer2024
- **Features**: Full dashboard with authentication

## ✅ **Verified Working**
- Authentication required
- Role-based access
- Professional dashboard
- Data import functionality
- Logout working properly

---
**Ready to deploy anywhere with Docker!**
