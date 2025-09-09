# 🚀 AWS EC2 Free Tier Deployment

## 📋 **Prerequisites**
- AWS Account with EC2 free tier available
- Basic AWS CLI knowledge (optional)

## 🖥️ **Step 1: Launch EC2 Instance**

### **Instance Configuration**
- **AMI**: Amazon Linux 2023 (free tier eligible)
- **Instance Type**: t2.micro (1 vCPU, 1GB RAM)
- **Storage**: 8GB GP2 (free tier limit)
- **Security Group**: Allow HTTP (80) and SSH (22)

### **Security Group Rules**
```
Type        Protocol    Port    Source
SSH         TCP         22      Your IP
HTTP        TCP         80      0.0.0.0/0
Custom TCP  TCP         8050    0.0.0.0/0 (optional)
```

## 🔧 **Step 2: Connect and Deploy**

### **Connect to Instance**
```bash
# SSH to your instance
ssh -i your-key.pem ec2-user@your-ec2-public-ip
```

### **Run Deployment Script**
```bash
# Download and run deployment script
curl -O https://raw.githubusercontent.com/your-repo/deploy-ec2-free.sh
chmod +x deploy-ec2-free.sh
./deploy-ec2-free.sh
```

### **Manual Deployment (Alternative)**
```bash
# Update system
sudo yum update -y

# Install Docker
sudo yum install -y docker
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -a -G docker ec2-user

# Logout and login again for group changes
exit
# SSH back in

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Create deployment directory
mkdir -p ~/dedalus-dashboard
cd ~/dedalus-dashboard

# Create docker-compose.yml
cat > docker-compose.yml << 'EOF'
version: '3.8'

services:
  dedalus-dashboard:
    image: hello2avanish/dedalus-tooling-dashboard:latest
    ports:
      - "80:8050"
    environment:
      - SECRET_KEY=your-production-secret
      - ADMIN_PASSWORD=your-secure-password
      - VIEWER_PASSWORD=your-viewer-password
    restart: unless-stopped
EOF

# Deploy dashboard
docker-compose up -d
```

## 🌐 **Step 3: Access Dashboard**

### **Get Public IP**
```bash
# Get your EC2 public IP
curl http://169.254.169.254/latest/meta-data/public-ipv4
```

### **Access URLs**
- **Dashboard**: `http://your-ec2-public-ip`
- **Direct Port**: `http://your-ec2-public-ip:8050`

### **Login Credentials**
- **Executive**: `admin` / `dedalus2024`
- **Operational**: `viewer` / `viewer2024`

## 💰 **Free Tier Considerations**

### **Resource Limits**
- **CPU**: 1 vCPU (sufficient for dashboard)
- **Memory**: 1GB RAM (adequate for single user)
- **Storage**: 8GB (dashboard image ~683MB)
- **Network**: 15GB/month outbound

### **Cost Optimization**
```bash
# Monitor resource usage
docker stats

# Check disk usage
df -h

# Monitor memory
free -h
```

## 🔒 **Security Best Practices**

### **Change Default Passwords**
```bash
# Edit docker-compose.yml
nano docker-compose.yml

# Update environment variables
- ADMIN_PASSWORD=your-secure-password
- VIEWER_PASSWORD=your-viewer-password
- SECRET_KEY=your-unique-secret-key

# Restart container
docker-compose restart
```

### **Enable HTTPS (Optional)**
```bash
# Install Certbot for Let's Encrypt
sudo yum install -y certbot

# Get SSL certificate (requires domain)
sudo certbot certonly --standalone -d your-domain.com
```

## 📊 **Monitoring & Maintenance**

### **Check Status**
```bash
# Check container status
docker-compose ps

# View logs
docker-compose logs -f

# Check health
curl http://localhost/login
```

### **Updates**
```bash
# Update dashboard
cd ~/dedalus-dashboard
docker-compose pull
docker-compose up -d
```

## 🚨 **Troubleshooting**

### **Common Issues**
```bash
# Container not starting
docker-compose logs dedalus-dashboard

# Port conflicts
sudo netstat -tlnp | grep :80

# Memory issues
free -h
docker system prune -f
```

### **Restart Services**
```bash
# Restart dashboard
docker-compose restart

# Full restart
docker-compose down
docker-compose up -d
```

## 🎯 **Production Checklist**

- ✅ **Security Group** - Only necessary ports open
- ✅ **Passwords Changed** - Default credentials updated
- ✅ **SSL Certificate** - HTTPS enabled (if domain available)
- ✅ **Monitoring** - Health checks working
- ✅ **Backups** - Data export capability tested
- ✅ **Updates** - Regular maintenance scheduled

**Your Dedalus Dashboard is now running on AWS EC2 Free Tier!**
