import os
import csv
import resend
import base64
import io
import smtplib
from datetime import datetime, date, timedelta
from email.message import EmailMessage
from flask_migrate import Migrate

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash, check_password_hash

from celery import Celery
from celery.schedules import crontab
from flask_caching import Cache
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

from models import (
    db, User, Doctor, Patient, Admin, Department,
    Appointment, DoctorAvailability, Treatment
)

from xhtml2pdf import pisa

load_dotenv()

app = Flask(__name__)

# CORS Configuration - restrict to specific origins in production
cors_origins = [origin.strip().rstrip('/') for origin in os.environ.get("CORS_ORIGINS", "").split(",") if origin]
if not cors_origins:
    cors_origins = ["http://localhost:5173", "http://127.0.0.1:5173"]
CORS(app, resources={r"/api/*": {"origins": cors_origins, "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"]}})

# Database Configuration
env = os.environ.get("FLASK_ENV", "development")
if env == "production":
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "postgresql://localhost/hospital_db")
else:
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///hospital.db"

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-secret-change-in-production")
app.config["DEBUG"] = os.environ.get("FLASK_DEBUG", "False") == "True"
app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY", "super-secret-futuristic-key-change-in-production")
app.config["PROPAGATE_EXCEPTIONS"] = True

db.init_app(app)
jwt = JWTManager(app)
migrate = Migrate(app, db)

app.config['CACHE_TYPE'] = 'RedisCache'
app.config['CACHE_REDIS_URL'] = os.environ.get('REDIS_URL', 'redis://localhost:6379/1')
app.config['CACHE_DEFAULT_TIMEOUT'] = 300 

app.config.update(
    broker_use_ssl={
        'ssl_cert_reqs': 'none' # Often required for cloud Redis providers
    },
    redis_backend_use_ssl={
        'ssl_cert_reqs': 'none'
    }
)

try:
    cache = Cache(app)
except Exception as e:
    print(f"Warning: Redis cache not available. Error: {e}")
    app.config['CACHE_TYPE'] = 'SimpleCache'
    cache = Cache(app)

app.config['CELERY_BROKER_URL'] = os.environ.get('CELERY_BROKER_URL', 'redis://localhost:6379/0')
app.config['result_backend'] = os.environ.get('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0')
app.config['TIMEZONE'] = os.environ.get('TIMEZONE', 'UTC')

try:
    celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
except:
    print("⚠️  Celery/Redis disabled - background tasks won't run")
    celery = None
celery.conf.update(app.config)

# Celery Beat schedule with proper cron expressions
celery.conf.beat_schedule = {
    'send-daily-reminders-morning': {
        'task': 'app.send_daily_reminders',
        'schedule': crontab(hour=8, minute=0),  # 8 AM daily
    },
    'send-monthly-doctor-reports': {
        'task': 'app.send_monthly_reports',
        'schedule': crontab(day_of_month=1, hour=9, minute=0),  # 1st of month at 9 AM
    }
}

resend.api_key = os.environ.get("RESEND_API_KEY")

def send_email(to_address, subject, body_content, is_html=False, attachment_name=None, attachment_data=None):
    """Send email using Resend API"""
    params = {
        "from": os.environ.get("SENDER_EMAIL", "onboarding@resend.dev"),
        "to": [to_address],
        "subject": subject,
    }

    # Set content type
    if is_html:
        params["html"] = body_content
    else:
        params["text"] = body_content

    # Handle Attachments (Resend expects base64 strings for content)
    if attachment_data and attachment_name:
        # If data is already bytes (like your PDF buffer), encode it
        if isinstance(attachment_data, bytes):
            encoded_content = base64.b64encode(attachment_data).decode()
        else:
            # If it's a string (like CSV text), encode then base64
            encoded_content = base64.b64encode(attachment_data.encode('utf-8')).decode()
            
        params["attachments"] = [
            {
                "filename": attachment_name,
                "content": encoded_content,
            }
        ]

    try:
        response = resend.Emails.send(params)
        return response
    except Exception as e:
        print(f"Resend failed to send email to {to_address}. Error: {e}")

@celery.task
def send_daily_reminders():
    with app.app_context():
        today = date.today()
        # Filtering for today's scheduled appointments
        appointments = Appointment.query.filter_by(date_scheduled=today, status="Scheduled").all()
        
        for appt in appointments:
            patient = appt.patient
            if patient and patient.email:
                subject = f"Reminder: Your Appointment Today at {appt.time_scheduled.strftime('%I:%M %p')}"
                body = (f"Hello {patient.full_name},\n\n"
                        f"This is a reminder for your visit with Dr. {appt.doctor.full_name} "
                        f"at {appt.time_scheduled.strftime('%I:%M %p')}.\n\n"
                        "Please arrive 10 minutes early.")
                
                # Using the updated helper
                send_email(patient.email, subject, body, is_html=False)
        return f"Daily reminders sent to {len(appointments)} patients."

@celery.task
def send_monthly_reports():
    with app.app_context():
        today = date.today()
        first_day_this_month = today.replace(day=1)
        last_day_prev_month = first_day_this_month - timedelta(days=1)
        first_day_prev_month = last_day_prev_month.replace(day=1)
        month_name = last_day_prev_month.strftime('%B %Y')

        doctors = Doctor.query.all()
        for doc in doctors:
            if not doc.email:
                continue
                
            appts = Appointment.query.filter(
                Appointment.doctor_id == doc.id,
                Appointment.status == "Completed",
                Appointment.date_scheduled >= first_day_prev_month,
                Appointment.date_scheduled <= last_day_prev_month
            ).all()

            html_content = f"""
            <html>
            <head>
                <style>
                    body {{ font-family: Helvetica, sans-serif; color: #333; }}
                    h1 {{ color: #008080; text-align: center; border-bottom: 2px solid #008080; padding-bottom: 10px; }}
                    h3 {{ color: #555; margin-top: 20px; }}
                    table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
                    th, td {{ border: 1px solid #ddd; padding: 10px; text-align: left; }}
                    th {{ background-color: #f2f2f2; color: #333; font-weight: bold; }}
                    .footer {{ text-align: center; margin-top: 50px; font-size: 12px; color: #888; }}
                </style>
            </head>
            <body>
                <h1>Hospital Management System</h1>
                <h2>Monthly Activity Report: {month_name}</h2>
                <h3>Attending Physician: Dr. {doc.full_name}</h3>
                <p><strong>Total Consultations Completed:</strong> {len(appts)}</p>
                
                <table>
                    <tr>
                        <th>Date</th>
                        <th>Patient</th>
                        <th>Diagnosis</th>
                        <th>Prescription</th>
                    </tr>
            """
            
            for a in appts:
                diag = a.treatment.diagnosis if a.treatment else "N/A"
                presc = a.treatment.prescription if a.treatment else "N/A"
                html_content += f"<tr><td>{a.date_scheduled}</td><td>{a.patient.full_name}</td><td>{diag}</td><td>{presc}</td></tr>"
            
            html_content += """
                </table>
                <div class="footer">Thank you for providing excellent patient care this month.</div>
            </body>
            </html>
            """

            pdf_buffer = io.BytesIO()
            pisa_status = pisa.CreatePDF(html_content, dest=pdf_buffer)
            
            if pisa_status.err:
                print(f"Error generating PDF for Dr. {doc.full_name}")
                pdf_data = None
            else:
                pdf_data = pdf_buffer.getvalue()

            email_body = f"Hello Dr. {doc.full_name},\n\nPlease find attached your official monthly activity report for {month_name} as a PDF.\n\nThank you,\nHospital Administration"
            
            send_email(
                to_address=doc.email, 
                subject=f"Official Monthly Report - {month_name}", 
                body_content=email_body, 
                is_html=False, 
                attachment_name=f"Report_{doc.full_name.replace(' ', '_')}_{month_name}.pdf", 
                attachment_data=pdf_data
            )
            
        return "Monthly PDF reports generated and sent."

@celery.task
def export_patient_history(patient_id):
    with app.app_context():
        patient = Patient.query.get(patient_id)
        if not patient or not patient.email:
            return "Export failed: No patient or email found."
            
        history = Appointment.query.filter_by(patient_id=patient_id, status="Completed").order_by(Appointment.date_scheduled.desc()).all()
        
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(['Date', 'Consulting Doctor', 'Department', 'Diagnosis', 'Prescription', 'Notes'])
        
        for appt in history:
            doc_name = f"Dr. {appt.doctor.full_name}" if appt.doctor else "Unknown"
            dept = appt.doctor.department.name if appt.doctor and appt.doctor.department else "General"
            diag = appt.treatment.diagnosis if appt.treatment else "N/A"
            presc = appt.treatment.prescription if appt.treatment else "N/A"
            notes = appt.treatment.notes if appt.treatment else "N/A"
            writer.writerow([appt.date_scheduled, doc_name, dept, diag, presc, notes])
            
        csv_data = output.getvalue()
        
        export_dir = os.path.join(os.path.dirname(__file__), 'exports')
        os.makedirs(export_dir, exist_ok=True)
        
        file_path = os.path.join(export_dir, f"history_patient_{patient_id}.csv")
        with open(file_path, 'w', newline='') as f:
            f.write(csv_data)
        
        subject = "Your Medical History Export is Ready"
        body = f"Hello {patient.full_name},\n\nYour requested medical history export is attached. You can also download it directly from your dashboard now.\n\nStay healthy!"
        
        send_email(patient.email, subject, body, attachment_name="medical_history.csv", attachment_data=csv_data)
        
        return "Export saved and sent successfully."

# Health check endpoint for monitoring
@app.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint for load balancers and monitoring"""
    try:
        # Check database connection
        db.session.execute("SELECT 1")
        db_status = "healthy"
    except Exception as e:
        db_status = f"unhealthy: {str(e)}"
    
    return jsonify({
        "status": "healthy" if db_status == "healthy" else "unhealthy",
        "database": db_status,
        "version": "2.0.0"
    }), 200 if db_status == "healthy" else 503


@app.route("/api/login", methods=["POST"], endpoint="api_login")
def ApiLogin():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    current_account = User.query.filter_by(username=username).first()

    if current_account and check_password_hash(current_account.password, password):
        if current_account.is_blacklisted:
            return jsonify({"error": "ACCOUNT SUSPENDED. Please contact administration."}), 403
        
        access_token = create_access_token(identity=str(current_account.id))
        return jsonify({
            "message": "Login Successful!",
            "access_token": access_token,
            "role": current_account.role,
            "username": current_account.username
        }), 200
    return jsonify({"error": "Invalid username or password"}), 401

@app.route("/api/register", methods=["POST"], endpoint="api_register")
def ApiRegister():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    
    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({"error": "Username already exists"}), 400

    hashed_pw = generate_password_hash(password, method="pbkdf2:sha256")
    new_user = User(username=username, password=hashed_pw, role="patient")
    db.session.add(new_user)
    db.session.commit()

    new_profile = Patient(
        user_id=new_user.id, 
        full_name=data.get("full_name"),
        email=data.get("email"),
        age=data.get("age"),
        phone=data.get("phone")
    )
    db.session.add(new_profile)
    db.session.commit()

    return jsonify({"message": "Registration Successful! You may now login."}), 201

@app.route("/api/departments", methods=["GET"], endpoint="api_get_departments")
@cache.cached(timeout=3600)
def ApiGetDepartments():
    depts = Department.query.all()
    data = [{"id": d.id, "name": d.name, "description": d.description} for d in depts]
    return jsonify(data), 200

@app.route("/api/doctors", methods=["GET"], endpoint="api_get_doctors")
@cache.cached(timeout=120)
def ApiGetDoctors():
    docs = Doctor.query.all()
    data = [{
        "id": d.id, "name": d.full_name, "department": d.department.name if d.department else "General",
        "fees": d.doctor_fees, "qualification": d.qualification, "intro": d.intro
    } for d in docs]
    return jsonify(data), 200

@app.route("/api/admin/dashboard", methods=["GET"], endpoint="api_admin_dashboard")
@jwt_required()
@cache.cached(timeout=60, key_prefix='admin_dashboard_data')
def ApiAdminDashboard():
    current_user_id = get_jwt_identity()
    user = db.session.get(User, int(current_user_id))
    if not user or user.role != "admin":
        return jsonify({"error": "Access denied."}), 403

    doctors, patients, all_appointments = Doctor.query.all(), Patient.query.all(), Appointment.query.all()
    
    dept_stats = {d.name: 0 for d in Department.query.all()}
    for appt in all_appointments:
        if appt.doctor and appt.doctor.department:
            dept_stats[appt.doctor.department.name] += 1

    return jsonify({
        "counts": {"doctors": len(doctors), "patients": len(patients), "appointments": len(all_appointments)},
        "chart_labels": list(dept_stats.keys()),
        "chart_values": list(dept_stats.values()),
        "doctors": [{
            "id": d.id, "user_id": d.user_id, "name": d.full_name, "email": d.email,
            "department": d.department.name if d.department else "Unassigned",
            "fees": d.doctor_fees, "is_blacklisted": d.user.is_blacklisted if d.user else False,
            "qualification": d.qualification, "designation": d.designation, "experience": d.experience, "intro": d.intro
        } for d in doctors],
        "patients": [{
            "id": p.id, "user_id": p.user_id, "name": p.full_name, "email": p.email,
            "age": p.age, "phone": p.phone, "is_blacklisted": p.user.is_blacklisted if p.user else False
        } for p in patients],
        "appointments": [{
            "id": a.id, "patient_name": a.patient.full_name if a.patient else "Deleted",
            "doctor_name": a.doctor.full_name if a.doctor else "Deleted",
            "department": a.doctor.department.name if a.doctor and a.doctor.department else "General",
            "date": a.date_scheduled.strftime("%Y-%m-%d"), "time": a.time_scheduled.strftime("%I:%M %p"), "status": a.status
        } for a in all_appointments]
    }), 200

@app.route("/api/admin/toggle_blacklist/<int:user_id>", methods=["PUT"], endpoint="api_toggle_blacklist")
@jwt_required()
def ApiToggleBlacklist(user_id):
    try:
        current_admin_id = get_jwt_identity()
        admin = db.session.get(User, int(current_admin_id))
        if not admin or admin.role != "admin": return jsonify({"error": "Unauthorized"}), 403

        target_user = db.session.get(User, user_id)
        if not target_user: return jsonify({"error": "User not found."}), 404
        if target_user.id == admin.id: return jsonify({"error": "Cannot suspend yourself."}), 400

        target_user.is_blacklisted = not target_user.is_blacklisted
        db.session.commit()
        cache.clear()
        return jsonify({"message": f"User access successfully {'suspended' if target_user.is_blacklisted else 'restored'}."}), 200
    except Exception as e:
        return jsonify({"error": f"Server Error: {str(e)}"}), 500

@app.route("/api/department", methods=["POST"], endpoint="api_add_department")
@jwt_required()
def ApiAddDepartment():
    current_user_id = get_jwt_identity()
    user = db.session.get(User, int(current_user_id))
    if not user or user.role != "admin": return jsonify({"error": "Unauthorized"}), 403

    data = request.get_json()
    if Department.query.filter_by(name=data.get("name")).first():
        return jsonify({"error": "Department already exists"}), 400

    new_dept = Department(name=data.get("name"), description=data.get("description"))
    db.session.add(new_dept)
    db.session.commit()
    cache.clear()
    return jsonify({"message": "Department created successfully!"}), 201

@app.route("/api/admin/add_doctor", methods=["POST"], endpoint="api_admin_add_doctor")
@jwt_required()
def ApiAdminAddDoctor():
    current_user_id = get_jwt_identity()
    user = db.session.get(User, int(current_user_id))
    if not user or user.role != "admin": return jsonify({"error": "Unauthorized"}), 403

    data = request.get_json()
    if User.query.filter_by(username=data.get("username")).first():
        return jsonify({"error": "Username already exists"}), 400

    hashed_pw = generate_password_hash(data.get("password"), method="pbkdf2:sha256")
    new_user = User(username=data.get("username"), password=hashed_pw, role="doctor")
    db.session.add(new_user)
    db.session.commit() 

    new_doctor = Doctor(
        user_id=new_user.id, full_name=data.get("full_name"), department_id=data.get("department_id"), 
        doctor_fees=data.get("doctor_fees"), email=data.get("email"), qualification=data.get("qualification"),
        designation=data.get("designation"), experience=data.get("experience"), intro=data.get("intro")
    )
    db.session.add(new_doctor)
    db.session.commit()
    cache.clear()
    return jsonify({"message": "Doctor registered successfully!"}), 201

@app.route("/api/admin/doctor/<int:id>", methods=["PUT", "DELETE"], endpoint="api_admin_manage_doctor")
@jwt_required()
def ApiAdminManageDoctor(id):
    current_user_id = get_jwt_identity()
    admin_user = db.session.get(User, int(current_user_id))
    if not admin_user or admin_user.role != "admin": return jsonify({"error": "Unauthorized"}), 403

    doctor = Doctor.query.get_or_404(id)
    
    if request.method == "DELETE":
        user_account = User.query.get(doctor.user_id)
        db.session.delete(doctor)
        db.session.delete(user_account)
        db.session.commit()
        cache.clear()
        return jsonify({"message": "Doctor securely removed."}), 200

    if request.method == "PUT":
        data = request.get_json()
        doctor.full_name = data.get("full_name", doctor.full_name)
        doctor.doctor_fees = data.get("doctor_fees", doctor.doctor_fees)
        doctor.department_id = data.get("department_id", doctor.department_id)
        doctor.qualification = data.get("qualification", doctor.qualification)
        doctor.designation = data.get("designation", doctor.designation)
        doctor.experience = data.get("experience", doctor.experience)
        doctor.intro = data.get("intro", doctor.intro)
        doctor.email = data.get("email", doctor.email)
        db.session.commit()
        cache.clear()
        return jsonify({"message": "Doctor profile updated successfully!"}), 200

@app.route("/api/admin/patient/<int:id>", methods=["PUT", "DELETE"], endpoint="api_admin_manage_patient")
@jwt_required()
def ApiAdminManagePatient(id):
    current_admin_id = get_jwt_identity()
    admin = db.session.get(User, int(current_admin_id))
    if not admin or admin.role != "admin": return jsonify({"error": "Unauthorized"}), 403

    patient = Patient.query.get_or_404(id)
    
    if request.method == "DELETE":
        user_account = User.query.get(patient.user_id)
        db.session.delete(patient)
        db.session.delete(user_account)
        db.session.commit()
        cache.clear()
        return jsonify({"message": "Patient records securely removed."}), 200

    if request.method == "PUT":
        data = request.get_json()
        patient.full_name = data.get("full_name", patient.full_name)
        patient.email = data.get("email", patient.email)
        patient.age = data.get("age", patient.age)
        patient.phone = data.get("phone", patient.phone)
        db.session.commit()
        cache.clear()
        return jsonify({"message": "Patient profile updated successfully!"}), 200

@app.route("/api/admin/patient/<int:id>/history", methods=["GET"], endpoint="api_admin_patient_history")
@jwt_required()
def ApiAdminPatientHistory(id):
    current_user_id = get_jwt_identity()
    admin_user = db.session.get(User, int(current_user_id))
    if not admin_user or admin_user.role != "admin": return jsonify({"error": "Unauthorized"}), 403

    patient = Patient.query.get_or_404(id)
    history = Appointment.query.filter_by(patient_id=id, status="Completed").order_by(Appointment.date_scheduled.desc()).all()
    
    history_list = [{
        "id": a.id, "date": a.date_scheduled.strftime("%Y-%m-%d"), "doctor_name": a.doctor.full_name,
        "department": a.doctor.department.name if a.doctor.department else "General",
        "diagnosis": a.treatment.diagnosis if a.treatment else "N/A", "prescription": a.treatment.prescription if a.treatment else "N/A",
        "notes": a.treatment.notes if a.treatment else "N/A", "visit_type": a.treatment.visit_type if a.treatment else "In-person"
    } for a in history]
        
    return jsonify({"patient_name": patient.full_name, "history": history_list}), 200

@app.route("/api/doctor/dashboard", methods=["GET"], endpoint="api_doctor_dashboard")
@jwt_required()
def ApiDoctorDashboard():
    current_user_id = get_jwt_identity()
    user = db.session.get(User, int(current_user_id))
    if not user or user.role != "doctor": return jsonify({"error": "Unauthorized"}), 403

    doctor = user.doctor_profile
    appointments = Appointment.query.filter_by(doctor_id=doctor.id).order_by(Appointment.date_scheduled).all()
    
    patient_ids = set(a.patient_id for a in appointments)
    my_patients = Patient.query.filter(Patient.id.in_(patient_ids)).all()

    return jsonify({
        "doctor_name": doctor.full_name,
        "department": doctor.department.name if doctor.department else "General",
        "appointments": [{"id": a.id, "date": a.date_scheduled.strftime("%Y-%m-%d"), "time": a.time_scheduled.strftime("%H:%M"), "status": a.status, "patient_name": a.patient.full_name} for a in appointments],
        "patients": [{"id": p.id, "name": p.full_name, "age": p.age, "phone": p.phone} for p in my_patients]
    }), 200

@app.route("/api/doctor/availability", methods=["POST"], endpoint="api_add_availability")
@jwt_required()
def ApiAddAvailability():
    current_user_id = get_jwt_identity()
    user = db.session.get(User, int(current_user_id))
    if not user or user.role != "doctor": return jsonify({"error": "Unauthorized"}), 403

    data = request.get_json()
    try:
        slot_date = datetime.strptime(data.get("date"), "%Y-%m-%d").date()
        start_time = datetime.strptime(data.get("start_time"), "%H:%M").time()
        end_time = datetime.strptime(data.get("end_time"), "%H:%M").time()
    except ValueError:
        return jsonify({"error": "Invalid date or time format."}), 400

    if slot_date < date.today():
        return jsonify({"error": "Cannot set availability for past dates."}), 400

    day_name = slot_date.strftime("%A")

    new_slot = DoctorAvailability(doctor_id=user.doctor_profile.id, date=slot_date, day_of_week=day_name, start_time=start_time, end_time=end_time)
    db.session.add(new_slot)
    db.session.commit()
    return jsonify({"message": f"Availability added for {slot_date.strftime('%B %d, %Y')}!"}), 201

@app.route("/api/doctor/treatment/<int:appointment_id>", methods=["POST"], endpoint="api_add_treatment")
@jwt_required()
def ApiAddTreatment(appointment_id):
    current_user_id = get_jwt_identity()
    user = db.session.get(User, int(current_user_id))
    if not user or user.role != "doctor": return jsonify({"error": "Unauthorized"}), 403

    appointment = Appointment.query.get_or_404(appointment_id)
    if appointment.doctor_id != user.doctor_profile.id: return jsonify({"error": "Unauthorized."}), 403

    data = request.get_json()
    new_treatment = Treatment(
        appointment_id=appointment_id, diagnosis=data.get("diagnosis"), prescription=data.get("prescription"),
        notes=data.get("notes"), visit_type=data.get("visit_type", "In-person"), tests_done=data.get("tests_done", "None")
    )

    appointment.status = "Completed"
    db.session.add(new_treatment)
    db.session.commit()
    return jsonify({"message": "Consultation saved and appointment marked as completed!"}), 201

@app.route("/api/doctor/appointment/<int:id>/cancel", methods=["PUT"], endpoint="api_doctor_cancel_appt")
@jwt_required()
def ApiDoctorCancelAppt(id):
    current_user_id = get_jwt_identity()
    user = db.session.get(User, int(current_user_id))
    if not user or user.role != "doctor": return jsonify({"error": "Unauthorized"}), 403

    appt = Appointment.query.get_or_404(id)
    if appt.doctor_id != user.doctor_profile.id: return jsonify({"error": "Unauthorized"}), 403

    appt.status = "Cancelled"
    db.session.commit()
    return jsonify({"message": "Appointment cancelled."}), 200

@app.route("/api/doctor/patient/<int:id>/history", methods=["GET"], endpoint="api_doctor_patient_history")
@jwt_required()
def ApiDoctorPatientHistory(id):
    current_user_id = get_jwt_identity()
    user = db.session.get(User, int(current_user_id))
    if not user or user.role != "doctor": return jsonify({"error": "Unauthorized"}), 403

    patient = Patient.query.get_or_404(id)
    history = Appointment.query.filter_by(patient_id=id, status="Completed").order_by(Appointment.date_scheduled.desc()).all()
    
    return jsonify({"patient_name": patient.full_name, "history": [{
        "id": a.id, "date": a.date_scheduled.strftime("%Y-%m-%d"), "doctor_name": a.doctor.full_name,
        "diagnosis": a.treatment.diagnosis if a.treatment else "N/A", "prescription": a.treatment.prescription if a.treatment else "N/A"
    } for a in history]}), 200

@app.route("/api/patient/dashboard", methods=["GET"], endpoint="api_patient_dashboard")
@jwt_required()
def ApiPatientDashboard():
    current_user_id = get_jwt_identity()
    user = db.session.get(User, int(current_user_id))
    if not user or user.role != "patient": return jsonify({"error": "Unauthorized"}), 403

    patient = user.patient_profile
    my_appointments = Appointment.query.filter_by(patient_id=patient.id).order_by(Appointment.date_scheduled.desc()).all()
    
    return jsonify({
        "patient_name": patient.full_name,
        "appointments": [{"id": a.id, "date": a.date_scheduled.strftime("%Y-%m-%d"), "time": a.time_scheduled.strftime("%H:%M"), "status": a.status, "doctor_name": a.doctor.full_name, "department": a.doctor.department.name if a.doctor.department else "General"} for a in my_appointments],
        "departments": [{"id": d.id, "name": d.name} for d in Department.query.all()]
    }), 200

@app.route("/api/patient/profile", methods=["GET", "PUT"], endpoint="api_patient_profile")
@jwt_required()
def ApiPatientProfile():
    current_user_id = get_jwt_identity()
    user = db.session.get(User, int(current_user_id))
    if not user or user.role != "patient": return jsonify({"error": "Unauthorized"}), 403

    patient = user.patient_profile

    if request.method == "GET":
        return jsonify({"full_name": patient.full_name, "age": patient.age, "phone": patient.phone, "email": patient.email or ""}), 200

    if request.method == "PUT":
        data = request.get_json()
        patient.full_name = data.get("full_name", patient.full_name)
        patient.age = data.get("age", patient.age)
        patient.email = data.get("email", patient.email)
        patient.phone = data.get("phone", patient.phone)
        db.session.commit()
        return jsonify({"message": "Profile updated successfully!"}), 200

@app.route("/api/patient/search_doctors", methods=["POST"], endpoint="api_patient_search_doctors")
@jwt_required()
def ApiPatientSearchDoctors():
    data = request.get_json()
    query = Doctor.query

    if data.get("department"):
        query = query.join(Department).filter(Department.name == data.get("department"))
        
    if data.get("date"):
        try:
            date_obj = datetime.strptime(data.get("date"), "%Y-%m-%d").date()
            query = query.join(DoctorAvailability).filter(DoctorAvailability.date == date_obj)
        except ValueError:
            return jsonify({"error": "Invalid date format"}), 400
            
    if data.get("name"):
        query = query.filter(Doctor.full_name.ilike(f"%{data.get('name')}%"))

    return jsonify([{
        "id": d.id, "name": d.full_name, "department": d.department.name if d.department else "General",
        "fees": d.doctor_fees, "qualification": d.qualification, "experience": d.experience
    } for d in query.all()]), 200

@app.route("/api/doctor/<int:id>/slots", methods=["GET"], endpoint="api_get_doctor_slots")
@jwt_required()
def ApiGetDoctorSlots(id):
    today = date.today()
    availability_blocks = DoctorAvailability.query.filter(DoctorAvailability.doctor_id == id, DoctorAvailability.date >= today).order_by(DoctorAvailability.date, DoctorAvailability.start_time).all()

    available_slots = []
    for block in availability_blocks:
        current_time = datetime.combine(block.date, block.start_time)
        end_datetime = datetime.combine(block.date, block.end_time)
        
        while current_time + timedelta(minutes=30) <= end_datetime:
            is_booked = Appointment.query.filter_by(doctor_id=id, date_scheduled=block.date, time_scheduled=current_time.time(), status="Scheduled").first()
            if not is_booked:
                available_slots.append({
                    "date": block.date.strftime("%Y-%m-%d"), "day_name": block.date.strftime("%A"),
                    "time": current_time.time().strftime("%H:%M"), "display_time": current_time.strftime("%I:%M %p")
                })
            current_time += timedelta(minutes=30)

    return jsonify({"slots": available_slots}), 200

@app.route("/api/patient/book", methods=["POST"], endpoint="api_patient_book")
@jwt_required()
def ApiPatientBook():
    current_user_id = get_jwt_identity()
    user = db.session.get(User, int(current_user_id))
    if not user or user.role != "patient": return jsonify({"error": "Unauthorized"}), 403

    data = request.get_json()
    date_obj = datetime.strptime(data.get("date"), "%Y-%m-%d").date()
    time_obj = datetime.strptime(data.get("time"), "%H:%M").time()

    if Appointment.query.filter_by(doctor_id=data.get("doctor_id"), date_scheduled=date_obj, time_scheduled=time_obj).first():
        return jsonify({"error": "Slot was just taken by another patient!"}), 409

    new_appt = Appointment(patient_id=user.patient_profile.id, doctor_id=data.get("doctor_id"), date_scheduled=date_obj, time_scheduled=time_obj, status="Scheduled")
    db.session.add(new_appt)
    db.session.commit()
    return jsonify({"message": "Appointment Booked Successfully!"}), 201

@app.route("/api/patient/history", methods=["GET"], endpoint="api_patient_own_history")
@jwt_required()
def ApiPatientOwnHistory():
    current_user_id = get_jwt_identity()
    user = db.session.get(User, int(current_user_id))
    if not user or user.role != "patient": return jsonify({"error": "Unauthorized"}), 403

    history = Appointment.query.filter_by(patient_id=user.patient_profile.id, status="Completed").order_by(Appointment.date_scheduled.desc()).all()
    return jsonify([{
        "id": a.id, "date": a.date_scheduled.strftime("%Y-%m-%d"), "doctor_name": a.doctor.full_name,
        "department": a.doctor.department.name if a.doctor.department else "General",
        "diagnosis": a.treatment.diagnosis if a.treatment else "N/A", "prescription": a.treatment.prescription if a.treatment else "N/A",
        "notes": a.treatment.notes if a.treatment else "N/A", "visit_type": a.treatment.visit_type if a.treatment else "In-person",
        "fees": a.doctor.doctor_fees if a.doctor else 0
    } for a in history]), 200

@app.route("/api/patient/export_history", methods=["POST"], endpoint="api_patient_export_history")
@jwt_required()
def ApiPatientExportHistory():
    current_user_id = get_jwt_identity()
    user = db.session.get(User, int(current_user_id))
    if not user or user.role != "patient": return jsonify({"error": "Unauthorized"}), 403

    if not user.patient_profile.email: return jsonify({"error": "No email address found in profile."}), 400

    export_patient_history.delay(user.patient_profile.id)
    return jsonify({"message": "Export initiated! An alert with the CSV will be sent to your email shortly."}), 200

@app.route("/api/patient/download_csv", methods=["GET"], endpoint="api_patient_download_csv")
@jwt_required()
def ApiPatientDownloadCSV():
    current_user_id = get_jwt_identity()
    user = db.session.get(User, int(current_user_id))
    if not user or user.role != "patient": return jsonify({"error": "Unauthorized"}), 403

    file_path = os.path.join(os.path.dirname(__file__), 'exports', f"history_patient_{user.patient_profile.id}.csv")
    if os.path.exists(file_path):
        return send_file(file_path, mimetype='text/csv', as_attachment=True, download_name=f"medical_history_{date.today()}.csv")
    return jsonify({"error": "No export found. Please generate an export first."}), 404

@app.route("/api/patient/appointment/<int:id>/cancel", methods=["PUT"], endpoint="api_patient_cancel_appt")
@jwt_required()
def ApiPatientCancelAppt(id):
    current_user_id = get_jwt_identity()
    user = db.session.get(User, int(current_user_id))
    if not user or user.role != "patient": 
        return jsonify({"error": "Unauthorized"}), 403

    appt = Appointment.query.get_or_404(id)
    if appt.patient_id != user.patient_profile.id: 
        return jsonify({"error": "Unauthorized"}), 403

    appt.status = "Cancelled"
    db.session.commit()
    return jsonify({"message": "Appointment cancelled successfully."}), 200

@app.route("/api/patient/payment", methods=["POST"], endpoint="api_patient_payment")
@jwt_required()
def ApiPatientPayment():
    current_user_id = get_jwt_identity()
    user = db.session.get(User, int(current_user_id))
    if not user or user.role != "patient": 
        return jsonify({"error": "Unauthorized"}), 403

    data = request.get_json()
    card_number = data.get("card_number", "")
    
    if len(card_number.replace(" ", "")) < 15:
        return jsonify({"error": "Invalid card number. Please check your details."}), 400

    
    return jsonify({"message": "Payment processed successfully! Thank you."}), 200

def create_admin():
    """
    Creates a default Admin account if one doesn't exist.
    Credential: admin / admin
    """
    with app.app_context():
        admin_user = User.query.filter_by(role="admin").first()
        if not admin_user:
            print("--- NO ADMIN FOUND. CREATING DEFAULT ADMIN... ---")

            hashed_pw = generate_password_hash("admin", method="pbkdf2:sha256")
            new_admin_user = User(username="admin", password=hashed_pw, role="admin")
            db.session.add(new_admin_user)
            db.session.commit()

            new_admin_profile = Admin(
                user_id=new_admin_user.id, full_name="Super Admin"
            )
            db.session.add(new_admin_profile)
            db.session.commit()

            print("--- ADMIN CREATED: Login with 'admin' / 'admin' ---")
        else:
            print("--- Admin account already exists. ---")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        create_admin()
    
    # Use Gunicorn for production, Flask dev server for development
    if os.environ.get("FLASK_ENV") == "production":
        print("Running in PRODUCTION mode")
        app.run(debug=False, host="0.0.0.0", port=5000)
    else:
        print("Running in DEVELOPMENT mode")
        app.run(debug=app.config.get("DEBUG", False), host="127.0.0.1", port=5000)