# ⚡ QUICK EC2 DEPLOYMENT

## 🚀 **One-Command Deployment**

### **Step 1: Launch EC2 Instance**
- **AMI**: Amazon Linux 2023
- **Type**: t2.micro (free tier)
- **Security**: Allow ports 22, 80, 8050

### **Step 2: SSH and Deploy**
```bash
# SSH to your instance
ssh -i your-key.pem ec2-user@your-ec2-ip

# One command deployment
curl -sSL https://raw.githubusercontent.com/your-repo/deploy-ec2-free.sh | bash
```

### **Step 3: Access Dashboard**
```bash
# Get your public IP
curl http://169.254.169.254/latest/meta-data/public-ipv4

# Access at: http://your-ec2-ip
# Login: admin/dedalus2024
```

## 🔧 **Manual Quick Deploy**
```bash
# Install Docker
sudo yum update -y && sudo yum install -y docker
sudo systemctl start docker && sudo usermod -a -G docker ec2-user

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Deploy Dashboard
mkdir ~/dashboard && cd ~/dashboard
cat > docker-compose.yml << 'EOF'
version: '3.8'
services:
  dashboard:
    image: hello2avanish/dedalus-tooling-dashboard:latest
    ports:
      - "80:8050"
    restart: unless-stopped
EOF

docker-compose up -d
```

## 💡 **Free Tier Optimized**
- **Cost**: $0/month (within free tier limits)
- **Performance**: Suitable for demo/development
- **Access**: Public IP with HTTP
- **Features**: Full dashboard functionality

**Dashboard deployed in under 5 minutes!**
