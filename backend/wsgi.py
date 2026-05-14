"""
WSGI entry point for production deployment with Gunicorn
Usage: gunicorn -w 4 -b 0.0.0.0:5000 wsgi:app
"""

import os
from app import app, db, create_admin

# Initialize database and admin on startup
with app.app_context():
    db.create_all()
    create_admin()

if __name__ == "__main__":
    app.run()
