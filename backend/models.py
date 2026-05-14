from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = 'app_user' # Successfully renamed to avoid Postgres keyword conflict
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    role = db.Column(db.String(50), nullable=False) # Roles: Admin, Doctor, Patient

    is_blacklisted = db.Column(db.Boolean, default=False)

    # Relationships remain the same as they point to Class names
    admin_profile = db.relationship("Admin", backref="user", uselist=False)
    doctor_profile = db.relationship("Doctor", backref="user", uselist=False)
    patient_profile = db.relationship("Patient", backref="user", uselist=False)


class Admin(db.Model):
    __tablename__ = 'admin'
    id = db.Column(db.Integer, primary_key=True)
    # UPDATED: Points to 'app_user.id' instead of 'user.id'
    user_id = db.Column(db.Integer, db.ForeignKey("app_user.id"), nullable=False)
    full_name = db.Column(db.String(150), nullable=False)


class Department(db.Model):
    __tablename__ = 'department'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=True)

    doctors = db.relationship("Doctor", backref="department", lazy=True)


class Doctor(db.Model):
    __tablename__ = 'doctor'
    id = db.Column(db.Integer, primary_key=True)
    # UPDATED: Points to 'app_user.id' instead of 'user.id'
    user_id = db.Column(db.Integer, db.ForeignKey("app_user.id"), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey("department.id"), nullable=True)

    full_name = db.Column(db.String(150), nullable=False)
    qualification = db.Column(db.String(100), nullable=True)
    designation = db.Column(db.String(150), nullable=True)
    experience = db.Column(db.Integer, nullable=True)
    intro = db.Column(db.Text, nullable=True)
    doctor_fees = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(150), nullable=True)

    availabilities = db.relationship(
        "DoctorAvailability", backref="doctor", lazy=True, cascade="all, delete-orphan"
    )
    appointments = db.relationship(
        "Appointment", backref="doctor", lazy=True, cascade="all, delete-orphan"
    )


class Patient(db.Model):
    __tablename__ = 'patient'
    id = db.Column(db.Integer, primary_key=True)
    # UPDATED: Points to 'app_user.id' instead of 'user.id'
    user_id = db.Column(db.Integer, db.ForeignKey("app_user.id"), nullable=False)

    full_name = db.Column(db.String(150), nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    address = db.Column(db.Text, nullable=True)
    age = db.Column(db.Integer, nullable=True)
    email = db.Column(db.String(150), nullable=True)

    appointments = db.relationship(
        "Appointment", backref="patient", lazy=True, cascade="all, delete-orphan"
    )


class DoctorAvailability(db.Model):
    __tablename__ = 'doctor_availability'
    id = db.Column(db.Integer, primary_key=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey("doctor.id"), nullable=False, index=True) 
    date = db.Column(db.Date, nullable=False, index=True) 
    day_of_week = db.Column(db.String(20), nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    is_available = db.Column(db.Boolean, default=True)


class Appointment(db.Model):
    __tablename__ = 'appointment'
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey("patient.id"), nullable=False, index=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey("doctor.id"), nullable=False, index=True)
    date_scheduled = db.Column(db.Date, nullable=False, index=True)
    time_scheduled = db.Column(db.Time, nullable=False)
    status = db.Column(db.String(50), default="Scheduled")

    treatment = db.relationship(
        "Treatment", backref="appointment", uselist=False, cascade="all, delete-orphan"
    )


class Treatment(db.Model):
    __tablename__ = 'treatment'
    id = db.Column(db.Integer, primary_key=True)
    appointment_id = db.Column(db.Integer, db.ForeignKey("appointment.id"), nullable=False)

    diagnosis = db.Column(db.Text, nullable=False)
    prescription = db.Column(db.Text, nullable=False)
    notes = db.Column(db.Text, nullable=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    visit_type = db.Column(db.String(50), nullable=True)
    tests_done = db.Column(db.Text, nullable=True)