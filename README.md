# Dedalus BI Dashboard

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Docker](https://img.shields.io/badge/docker-ready-blue.svg)](https://www.docker.com/)

> **Executive Business Intelligence Dashboard for Enterprise Tool Migration Analytics**

Professional dashboard solution for tracking tool migration progress, ROI analysis, and cost optimization across enterprise tooling landscapes. Built for C-level executives and operational teams.

## 🎯 Key Metrics

- **$1,087,776** Annual Cost Savings
- **388%** Return on Investment
- **56** Tools Migration Tracking
- **Real-time** Analytics & Reporting

## 🚀 Quick Start

### Local Development
```bash
# Clone repository
git clone https://github.com/hi-avanish/bi-dashboard.git
cd bi-dashboard

# Install dependencies
pip install -r requirements.txt

# Start dashboard
python3 start_dashboard.py
```

**Access**: http://localhost:8050

### Docker Deployment
```bash
# Build and run
docker-compose up -d

# Or use pre-built image
docker run -p 8050:8050 dedalus/bi-dashboard
```

### Cloud Deployment
- **AWS**: `./deploy-aws.sh`
- **Azure**: `./deploy-azure.sh`
- **EC2 Free Tier**: `./deploy-ec2-free.sh`

## 🔐 Authentication

| Role | Username | Password | Access Level |
|------|----------|----------|--------------|
| Executive | `admin` | `dedalus2024` | Full Analytics |
| Operational | `viewer` | `viewer2024` | Read-only |

*Credentials configurable via environment variables*

## 📊 Features

### Executive Dashboard
- **KPI Overview**: Cost savings, ROI, completion rates
- **Interactive Charts**: Pie, Bar, Donut visualizations
- **Migration Timeline**: Progress tracking across tools
- **Financial Analytics**: Budget vs actual, savings projections

### Operational Views
- **Tool Status**: Individual migration progress
- **Resource Allocation**: Team and budget distribution
- **Risk Assessment**: Migration challenges and blockers
- **Detailed Reports**: Exportable analytics

### Technical Features
- **Role-based Access**: Executive and operational views
- **Real-time Updates**: Live data synchronization
- **Mobile Responsive**: Cross-device compatibility
- **Export Capabilities**: PDF, Excel report generation
- **Security**: Flask-Login authentication system

## 🏗️ Architecture

```
bi-dashboard/
├── src/
│   └── unified_dashboard.py    # Main application
├── data/
│   ├── populated_migration_template.xlsx
│   └── migration_template.xlsx
├── static/
│   └── Dedalus_fav.png        # Company branding
├── deploy-*.sh                # Cloud deployment scripts
├── docker-compose.yml         # Container orchestration
├── Dockerfile                 # Container definition
└── start_dashboard.py         # Application entry point
```

## 🛠️ Technology Stack

- **Frontend**: Dash, Plotly, Bootstrap
- **Backend**: Flask, Python 3.11+
- **Data**: Pandas, Excel integration
- **Visualization**: Plotly, Matplotlib, Seaborn
- **Authentication**: Flask-Login
- **Deployment**: Docker, AWS, Azure

## 📈 Data Sources

- **Primary**: Excel templates with migration data
- **Metrics**: 56 enterprise tools tracking
- **Updates**: Real-time data synchronization
- **Calculations**: Automated ROI and savings analysis

## 🚀 Deployment Options

### 1. Local Development
```bash
python3 start_dashboard.py
```

### 2. Docker Container
```bash
docker-compose up -d
```

### 3. AWS Deployment
```bash
./deploy-aws.sh
```

### 4. Azure Deployment
```bash
./deploy-azure.sh
```

### 5. EC2 Free Tier
```bash
./deploy-ec2-free.sh
```

## 🔧 Configuration

### Environment Variables
```bash
# Authentication
ADMIN_USERNAME=admin
ADMIN_PASSWORD=dedalus2024
VIEWER_USERNAME=viewer
VIEWER_PASSWORD=viewer2024

# Server Configuration
HOST=0.0.0.0
PORT=8050
DEBUG=false
SECRET_KEY=your-secret-key
```

### Data Configuration
- Update Excel files in `/data/` directory
- Modify chart configurations in `unified_dashboard.py`
- Customize branding in `/static/` directory

## 📋 Requirements

- **Python**: 3.11+
- **Memory**: 512MB minimum
- **Storage**: 100MB
- **Network**: HTTP/HTTPS access

## 🤝 Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature/new-feature`
3. Commit changes: `git commit -am 'Add new feature'`
4. Push to branch: `git push origin feature/new-feature`
5. Submit pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Documentation**: See `/docs/` directory
- **Issues**: GitHub Issues
- **Security**: Report to security@dedalus.com

## 🏢 About Dedalus

Professional enterprise software solutions for healthcare and business intelligence.

---

**Dedalus BI Dashboard** - Transforming Enterprise Analytics
