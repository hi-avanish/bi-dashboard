#!/bin/bash
# Deploy Dedalus Dashboard on AWS EC2 Free Tier

echo "🚀 Deploying Dedalus Dashboard on AWS EC2 Free Tier..."

# Update system
sudo yum update -y

# Install Docker
sudo yum install -y docker
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -a -G docker ec2-user

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
      - PYTHONUNBUFFERED=1
      - SECRET_KEY=dedalus-production-secret-2024
      - HOST=0.0.0.0
      - PORT=8050
      - DEBUG=false
      - ADMIN_USERNAME=admin
      - ADMIN_PASSWORD=dedalus2024
      - VIEWER_USERNAME=viewer
      - VIEWER_PASSWORD=viewer2024
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8050/login"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
EOF

# Pull and start the dashboard
docker-compose pull
docker-compose up -d

echo "✅ Dedalus Dashboard deployed successfully!"
echo "🌐 Access at: http://$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4)"
echo "🔐 Login: admin/dedalus2024 or viewer/viewer2024"
