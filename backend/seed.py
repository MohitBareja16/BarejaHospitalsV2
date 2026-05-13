from app import app, db
from models import User, Admin, Department, Doctor, Patient, DoctorAvailability, Appointment, Treatment
from werkzeug.security import generate_password_hash
from datetime import date, time, timedelta

def seed_database():
    with app.app_context():
        print("Dropping all existing tables...")
        db.drop_all()
        
        print("Creating new tables...")
        db.create_all()

        print("Seeding Admin...")
        admin_user = User(
            username="admin", 
            password=generate_password_hash("admin", method="pbkdf2:sha256"), 
            role="admin"
        )
        db.session.add(admin_user)
        db.session.commit()
        
        admin_profile = Admin(user_id=admin_user.id, full_name="System Administrator")
        db.session.add(admin_profile)
        db.session.commit()

        print("Seeding Departments...")
        cardio = Department(name="Cardiology", description="Heart and cardiovascular system.")
        neuro = Department(name="Neurology", description="Brain, spinal cord, and nervous system.")
        ortho = Department(name="Orthopedics", description="Bones, joints, ligaments, tendons, and muscles.")
        db.session.add_all([cardio, neuro, ortho])
        db.session.commit()

        print("Seeding Doctors...")
        doc1_user = User(
            username="drheart", 
            password=generate_password_hash("password", method="pbkdf2:sha256"), 
            role="doctor"
        )
        db.session.add(doc1_user)
        db.session.commit()
        
        doc1 = Doctor(
            user_id=doc1_user.id, 
            department_id=cardio.id,
            full_name="Dr. John Heart", 
            qualification="MBBS, MD Cardiology",
            designation="Senior Consultant", 
            experience=15, 
            intro="Specializes in complex cardiovascular surgeries and health management.",
            doctor_fees=1000,
            email="john.heart@hospital.com"
        )
        db.session.add(doc1)
        db.session.commit()

        print("Seeding Doctor Availability...")
        today = date.today()
        tomorrow = today + timedelta(days=1)
        
        avail1 = DoctorAvailability(
            doctor_id=doc1.id, 
            date=today, 
            day_of_week=today.strftime("%A"),
            start_time=time(9, 0), 
            end_time=time(13, 0),  
            is_available=True
        )
        avail2 = DoctorAvailability(
            doctor_id=doc1.id, 
            date=tomorrow, 
            day_of_week=tomorrow.strftime("%A"),
            start_time=time(14, 0),
            end_time=time(18, 0), 
            is_available=True
        )
        db.session.add_all([avail1, avail2])
        db.session.commit()

        print("Seeding Patients...")
        pat1_user = User(
            username="patient1", 
            password=generate_password_hash("password", method="pbkdf2:sha256"), 
            role="patient"
        )
        db.session.add(pat1_user)
        db.session.commit()

        pat1 = Patient(
            user_id=pat1_user.id, 
            full_name="Alice Smith", 
            phone="9876543210",
            address="123 Main Street, Cityville",
            age=30,
            email="alice.smith@example.com"
        )
        db.session.add(pat1)
        db.session.commit()

        print("Seeding Appointments and Treatments...")
        
        appt_today = Appointment(
            patient_id=pat1.id, 
            doctor_id=doc1.id, 
            date_scheduled=today, 
            time_scheduled=time(10, 0),
            status="Scheduled"
        )
        db.session.add(appt_today)

        past_date = today.replace(day=1) - timedelta(days=15)
        appt_past = Appointment(
            patient_id=pat1.id, 
            doctor_id=doc1.id, 
            date_scheduled=past_date, 
            time_scheduled=time(11, 30), 
            status="Completed"
        )
        db.session.add(appt_past)
        db.session.commit()

        treatment = Treatment(
            appointment_id=appt_past.id, 
            diagnosis="Mild Arrhythmia", 
            prescription="Beta Blockers 50mg once daily", 
            notes="Advised to reduce caffeine intake. Follow up in 3 months.", 
            visit_type="In-person", 
            tests_done="ECG, Complete Blood Count"
        )
        db.session.add(treatment)
        db.session.commit()

        print("\n✅ Database Successfully Seeded!")
        print("-" * 50)
        print("TEST ACCOUNTS:")
        print("Admin   -> Username: admin    | Password: admin")
        print("Doctor  -> Username: drheart  | Password: password")
        print("Patient -> Username: patient1 | Password: password")
        print("-" * 50)

if __name__ == "__main__":
    seed_database()