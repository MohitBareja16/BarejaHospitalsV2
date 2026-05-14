"""
WSGI entry point for production deployment with Gunicorn
Usage: gunicorn -w 4 -b 0.0.0.0:5000 wsgi:app
"""

import os
from app import app, db, create_admin

# Initialize database and admin on startup
try:
    with app.app_context():
        db.create_all()
        print("Database tables created in PostgreSQL!")
except Exception as e:
    print(f"Database initialization failed: {e}")
    print("Continuing without database initialization...")

if __name__ == "__main__":
    app.run()
