# 🐳 Docker Deployment Guide

## Quick Start

### Option 1: Using Docker Run
```bash
# Build the image
docker build -t student-management-system .

# Run the container
docker run -d -p 8501:8501 --name student-app student-management-system

# Access the app
# Open browser: http://localhost:8501
```

### Option 2: Using Docker Compose
```bash
# Start the application
docker-compose up -d

# Stop the application
docker-compose down

# View logs
docker-compose logs -f
```

## Docker Commands

### Build Image
```bash
docker build -t student-management-system:v1.0 .
```

### Run Container
```bash
docker run -d \
  -p 8501:8501 \
  --name student-app \
  -v $(pwd)/data:/app/data \
  student-management-system:v1.0
```

### View Logs
```bash
docker logs -f student-app
```

### Stop Container
```bash
docker stop student-app
```

### Remove Container
```bash
docker rm student-app
```

### List Running Containers
```bash
docker ps
```

### Access Container Shell
```bash
docker exec -it student-app /bin/bash
```

## Health Check
```bash
curl http://localhost:8501/_stcore/health
```

## Troubleshooting

### Container won't start
```bash
docker logs student-app
```

### Port already in use
```bash
# Use a different port
docker run -p 8502:8501 student-management-system
```

### Reset everything
```bash
docker-compose down -v
docker-compose up -d --build
```