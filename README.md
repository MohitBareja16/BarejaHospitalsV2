# Hospital Management System V2 (MAD-II)

A comprehensive, multi-role web application built to streamline hospital operations. This project serves as the submission for the Modern Application Development II course. It features a Flask backend, a Vue.js frontend, and asynchronous task management via Celery and Redis.

## System Roles
* **Admin:** Oversees the hospital system, registers doctors, manages departments, and can suspend/restore user access.
* **Doctor:** Manages their daily schedule, sets recurring availability, views patient medical histories, and logs consultation diagnoses and prescriptions.
* **Patient:** Browses available doctors by specialization, books appointments (with double-booking prevention), processes dummy payments, and downloads their medical history.

## Technical Stack
* **Frontend:** Vue.js 3, Bootstrap 5, Custom CSS, Vite
* **Backend:** Flask, Flask-RESTful, Flask-JWT-Extended, SQLAlchemy
* **Database:** SQLite (development) / PostgreSQL (production)
* **Caching & Broker:** Redis (Flask-Caching, Celery)
* **Background Jobs:** Celery with Beat scheduler
* **Deployment:** Docker, Gunicorn, Nginx
* **Production Ready:** Environment variables, CORS config, health checks

## Installation & Setup

### Local Development

#### 1. Backend Setup
```bash
cd backend
python -m venv venv

# Activate (choose based on OS)
source venv/bin/activate      # Linux/Mac
venv\Scripts\activate          # Windows

pip install -r requirements.txt
python seed.py                 # Initialize database with demo data
python app.py                  # Start server at http://localhost:5000
```

#### 2. Redis & Celery Setup
```bash
# Terminal 2 - Celery Worker
source venv/bin/activate
celery -A app.celery worker --loglevel=info

# Terminal 3 - Celery Beat (scheduled tasks)
source venv/bin/activate
celery -A app.celery beat --loglevel=info
```

#### 3. Frontend Setup
```bash
cd frontend
npm install
npm run dev                    # Start at http://localhost:5173
```

**Default Credentials:**
- Admin: `admin` / `admin`
- Doctor: `drheart` / `password`

### Production Deployment

See [PRODUCTION_DEPLOYMENT.md](backend/PRODUCTION_DEPLOYMENT.md) for:
- Docker Compose setup
- Linux server manual deployment
- Railway/Render deployment
- Nginx reverse proxy configuration
- SSL/HTTPS setup
- Monitoring and logging

## Deployment Guides

- **Frontend:** [DEPLOYMENT.md](frontend/DEPLOYMENT.md) - Deploy to Vercel
- **Backend:** [PRODUCTION_DEPLOYMENT.md](backend/PRODUCTION_DEPLOYMENT.md) - Deploy to Railway, Render, or self-hosted

## API Documentation

See [api.yaml](api.yaml) for OpenAPI specification.

Health check endpoint: `GET /health`

Have Fun Exploring - BarejaHospitals
