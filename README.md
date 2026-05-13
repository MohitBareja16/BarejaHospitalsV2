# Hospital Management System V2 (MAD-II)

A comprehensive, multi-role web application built to streamline hospital operations. This project serves as the submission for the Modern Application Development II course. It features a Flask backend, a Vue.js frontend, and asynchronous task management via Celery and Redis.

## System Roles
* **Admin:** Oversees the hospital system, registers doctors, manages departments, and can suspend/restore user access.
* **Doctor:** Manages their daily schedule, sets recurring availability, views patient medical histories, and logs consultation diagnoses and prescriptions.
* **Patient:** Browses available doctors by specialization, books appointments (with double-booking prevention), processes dummy payments, and downloads their medical history.

## Technical Stack
* **Frontend:** Vue.js 3, Bootstrap 5, Custom CSS
* **Backend:** Flask, Flask-RESTful, Flask-JWT-Extended
* **Database:** SQLite (managed via Flask-SQLAlchemy)
* **Caching & Broker:** Redis (Flask-Caching)
* **Background Jobs:** Celery (Beat scheduling for daily reminders and monthly PDF reports)

## Installation & Setup

### 1. Backend Setup
1. Navigate to the `backend` directory.
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment:
   * Windows: `venv\Scripts\activate`
   * Mac/Linux: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Seed the database: `python seed.py`
6. Start the Flask server: `python app.py`

### 2. Redis & Celery Setup
1. Ensure Redis is installed and running on `localhost:6379`.
2. Open a new terminal, activate the backend virtual environment, and start the Celery worker:
   `celery -A app.celery worker --loglevel=info`
3. Open another terminal, activate the environment, and start the Celery Beat scheduler:
   `celery -A app.celery beat --loglevel=info`

### 3. Frontend Setup
1. Navigate to the `frontend` directory.
2. Install dependencies: `npm install`
3. Start the development server: `npm run dev`

Have Fun Exploring my Website - BarejaHospitals
