# 🐳 Dedalus Dashboard - Docker Hub

## 📊 **Professional Tooling Dashboard**
Secure, role-based dashboard for tracking tool migration progress, ROI analysis, and cost optimization.

## 🚀 **Quick Start**

### **Pull and Run**
```bash
docker pull hello2avanish/dedalus-dashboard:latest
docker run -p 8050:8050 hello2avanish/dedalus-dashboard:latest
```

### **Docker Compose**
```yaml
version: '3.8'
services:
  dedalus-dashboard:
    image: hello2avanish/dedalus-dashboard:latest
    ports:
      - "8050:8050"
    environment:
      - SECRET_KEY=your-secret-key
      - DEBUG=false
    restart: unless-stopped
```

## 🔐 **Default Credentials**
- **Executive**: `admin` / `dedalus2024`
- **Operational**: `viewer` / `viewer2024`

## 🌐 **Access**
- **URL**: http://localhost:8050
- **Authentication**: Required (no anonymous access)

## ⚙️ **Environment Variables**
```bash
SECRET_KEY=dedalus-dashboard-secret-key-2024
HOST=0.0.0.0
PORT=8050
DEBUG=false
ADMIN_USERNAME=admin
ADMIN_PASSWORD=dedalus2024
VIEWER_USERNAME=viewer
VIEWER_PASSWORD=viewer2024
```

## 📊 **Features**
- ✅ **Secure Authentication** - Role-based access control
- ✅ **Executive Dashboard** - KPIs, ROI analysis, cost savings
- ✅ **Operational Dashboard** - Migration tracking, component status
- ✅ **Data Import** - Excel file upload with validation
- ✅ **Professional Charts** - Interactive visualizations
- ✅ **Multi-cloud Ready** - AWS, Azure, GCP compatible

## 🎯 **Use Cases**
- Tool migration tracking
- Cost optimization analysis
- Executive reporting
- Operational monitoring
- ROI visualization

## 🔧 **Production Deployment**
```bash
# Change default passwords
docker run -p 8050:8050 \
  -e ADMIN_PASSWORD=your-secure-password \
  -e VIEWER_PASSWORD=your-viewer-password \
  -e SECRET_KEY=your-unique-secret \
  hello2avanish/dedalus-dashboard:latest
```

## 📋 **Health Check**
- **Endpoint**: `/login`
- **Interval**: 30s
- **Timeout**: 10s

---
**Ready-to-use professional dashboard with security enabled by default!**
