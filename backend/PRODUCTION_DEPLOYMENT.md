# Backend Production Deployment Guide

## Overview
This guide covers deploying the Flask backend for the Hospital Management System to production.

## Prerequisites
- Python 3.11+
- PostgreSQL 13+
- Redis 7+
- Gunicorn or similar WSGI server

## Option 1: Docker Deployment (Recommended)

### 1. Build and Run with Docker Compose
```bash
# Clone your repository
git clone https://github.com/your-repo/hospital-management-system.git
cd hospital-management-system/backend

# Create .env file from example
cp .env.example .env

# Edit .env with your production values
nano .env

# Start all services
docker-compose up -d

# View logs
docker-compose logs -f backend
```

### 2. Environment Variables
Create `.env` file with:
```
FLASK_ENV=production
FLASK_DEBUG=False
SECRET_KEY=your-very-long-random-key-here
JWT_SECRET_KEY=another-long-random-key-here
DATABASE_URL=postgresql://hospital_user:password@postgres:5432/hospital_db
REDIS_URL=redis://redis:6379/0
CELERY_BROKER_URL=redis://redis:6379/0
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password
CORS_ORIGINS=https://your-frontend-domain.com
```

## Option 2: Manual Linux Server Deployment

### 1. Setup Virtual Environment
```bash
# SSH into your server
ssh user@your-server.com

# Clone repository
git clone https://github.com/your-repo/hospital-management-system.git
cd hospital-management-system/backend

# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure PostgreSQL
```bash
# Install PostgreSQL (Ubuntu/Debian)
sudo apt-get install postgresql postgresql-contrib

# Create database and user
sudo -u postgres psql
CREATE DATABASE hospital_db;
CREATE USER hospital_user WITH PASSWORD 'your-secure-password';
GRANT ALL PRIVILEGES ON DATABASE hospital_db TO hospital_user;
\q
```

### 3. Configure Redis
```bash
# Install Redis
sudo apt-get install redis-server

# Start Redis
sudo systemctl start redis-server
sudo systemctl enable redis-server
```

### 4. Setup Environment File
```bash
cp .env.example .env
nano .env
# Fill in your production values
```

### 5. Initialize Database
```bash
source venv/bin/activate
python -c "from app import app, db, create_admin; app.app_context().push(); db.create_all(); create_admin()"
```

### 6. Setup Systemd Service
```bash
# Copy service file
sudo cp hospital-api.service /etc/systemd/system/

# Edit the paths in the service file
sudo nano /etc/systemd/system/hospital-api.service

# Enable and start the service
sudo systemctl daemon-reload
sudo systemctl enable hospital-api
sudo systemctl start hospital-api

# Check status
sudo systemctl status hospital-api
```

### 7. Start Celery Worker and Beat
```bash
# In separate terminal windows or use supervisor/systemd

# Terminal 1: Celery Worker
source venv/bin/activate
celery -A app.celery worker --loglevel=info

# Terminal 2: Celery Beat (for scheduled tasks)
source venv/bin/activate
celery -A app.celery beat --loglevel=info
```

### 8. Setup Nginx as Reverse Proxy
```bash
sudo apt-get install nginx

# Create Nginx config
sudo nano /etc/nginx/sites-available/hospital-api

# Add this configuration:
```

```nginx
upstream flask_app {
    server 127.0.0.1:5000;
}

server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://flask_app;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static {
        alias /home/your-user/hospital-management-system/backend/exports;
    }
}
```

```bash
# Enable Nginx config
sudo ln -s /etc/nginx/sites-available/hospital-api /etc/nginx/sites-enabled/

# Test Nginx config
sudo nginx -t

# Start Nginx
sudo systemctl start nginx
sudo systemctl enable nginx
```

### 9. Setup SSL with Certbot
```bash
sudo apt-get install certbot python3-certbot-nginx

sudo certbot --nginx -d your-domain.com

# Auto-renew certificate
sudo systemctl enable certbot.timer
```

## Option 3: Railway/Render Deployment

### Railway
1. Sign up at https://railway.app
2. Create new project
3. Add PostgreSQL and Redis from marketplace
4. Add code from GitHub
5. Set environment variables in dashboard
6. Deploy!

### Render
1. Sign up at https://render.com
2. Create new Web Service
3. Connect GitHub repository
4. Set Build Command: `pip install -r requirements.txt`
5. Set Start Command: `gunicorn -c gunicorn_config.py wsgi:app`
6. Add PostgreSQL from dashboard
7. Set environment variables
8. Deploy!

## Monitoring

### Health Check
```bash
curl https://your-api-domain.com/health
```

Response:
```json
{
  "status": "healthy",
  "database": "healthy",
  "version": "2.0.0"
}
```

### View Logs
```bash
# Systemd service logs
sudo journalctl -u hospital-api -f

# Docker logs
docker-compose logs -f backend
```

## Database Migrations

For schema updates, use Flask-Migrate (not yet setup):
```bash
pip install Flask-Migrate
flask db init
flask db migrate
flask db upgrade
```

## Production Checklist

- [ ] Change SECRET_KEY and JWT_SECRET_KEY to strong random values
- [ ] Set FLASK_DEBUG=False
- [ ] Use PostgreSQL (not SQLite)
- [ ] Configure CORS_ORIGINS to your frontend domain
- [ ] Setup email SMTP credentials
- [ ] Enable HTTPS/SSL
- [ ] Configure backups for PostgreSQL
- [ ] Setup monitoring and alerting
- [ ] Configure log aggregation
- [ ] Test API endpoints thoroughly
- [ ] Set up health checks
- [ ] Configure rate limiting
- [ ] Setup database connection pooling

## Troubleshooting

### Redis Connection Issues
```bash
# Test Redis connection
redis-cli ping
# Should respond with PONG
```

### PostgreSQL Connection Issues
```bash
# Test connection
psql postgresql://hospital_user:password@localhost:5432/hospital_db
```

### Celery Not Running
```bash
# Check Celery worker
celery -A app.celery inspect active

# Check Celery Beat schedule
celery -A app.celery inspect scheduled
```

## Security Notes

- Always use HTTPS in production
- Rotate SECRET_KEY and JWT_SECRET_KEY regularly
- Never commit .env file
- Use strong database passwords
- Configure firewall rules
- Enable database backups
- Monitor API logs for suspicious activity
- Rate limit API endpoints
- Validate and sanitize all inputs
