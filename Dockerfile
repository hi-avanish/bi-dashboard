FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Set default environment variables
ENV SECRET_KEY=dedalus-dashboard-secret-key-2024
ENV HOST=0.0.0.0
ENV PORT=8050
ENV DEBUG=false
ENV ADMIN_USERNAME=admin
ENV ADMIN_PASSWORD=dedalus2024
ENV VIEWER_USERNAME=viewer
ENV VIEWER_PASSWORD=viewer2024

# Expose port
EXPOSE 8050

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8050/login || exit 1

# Run application
CMD ["python", "start_dashboard.py"]
