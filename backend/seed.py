from app import app, db
from models import User, Admin, Department, Doctor, Patient, DoctorAvailability, Appointment, Treatment
from werkzeug.security import generate_password_hash
from datetime import date, time, timedelta
import random

def seed_database():
    with app.app_context():
        print("🗑️  Dropping all existing tables...")
        db.drop_all()
        
        print("📦 Creating new tables...")
        db.create_all()

        # ============ ADMINS ============
        print("\n👨‍💼 Seeding Admins...")
        admin_user = User(
            username="admin", 
            password=generate_password_hash("admin", method="pbkdf2:sha256"), 
            role="admin"
        )
        db.session.add(admin_user)
        db.session.commit()
        admin1 = Admin(user_id=admin_user.id, full_name="Dr. Rajesh Kumar")
        db.session.add(admin1)
        db.session.commit()

        # ============ DEPARTMENTS ============
        print("🏥 Seeding Departments...")
        departments_data = [
            ("Cardiology", "Heart and cardiovascular system specialists"),
            ("Neurology", "Brain, spinal cord, and nervous system treatment"),
            ("Orthopedics", "Bones, joints, ligaments, tendons, and muscles"),
            ("Dermatology", "Skin, hair, and nail care"),
            ("General Medicine", "General health and wellness"),
            ("Pediatrics", "Children's healthcare services"),
            ("Psychiatry", "Mental health and behavioral services"),
        ]
        
        departments = {}
        for dept_name, dept_desc in departments_data:
            dept = Department(name=dept_name, description=dept_desc)
            db.session.add(dept)
            db.session.flush()
            departments[dept_name] = dept
        db.session.commit()

        # ============ DOCTORS ============
        print("👨‍⚕️  Seeding Doctors...")
        doctors_data = [
            # Cardiology
            ("Dr. Amit Patel", "MBBS, MD Cardiology", "Senior Consultant", 18, 1200, "amit.patel@hospital.com", "Expert in complex cardiac surgeries"),
            ("Dr. Priya Singh", "MBBS, DM Cardiology", "Consultant", 12, 1000, "priya.singh@hospital.com", "Specializes in coronary interventions"),
            
            # Neurology
            ("Dr. Rajesh Sharma", "MBBS, MD Neurology", "Senior Consultant", 15, 1100, "rajesh.sharma@hospital.com", "Brain and spine disorder specialist"),
            ("Dr. Neha Gupta", "MBBS, DM Neurology", "Consultant", 10, 950, "neha.gupta@hospital.com", "Neurological emergency specialist"),
            
            # Orthopedics
            ("Dr. Vikram Desai", "MBBS, MS Orthopedics", "Senior Consultant", 16, 1000, "vikram.desai@hospital.com", "Joint replacement and sports injuries"),
            ("Dr. Anjali Reddy", "MBBS, MS Orthopedics", "Consultant", 9, 850, "anjali.reddy@hospital.com", "Pediatric and adult bone fractures"),
            
            # Dermatology
            ("Dr. Sangeeta Nair", "MBBS, MD Dermatology", "Consultant", 11, 800, "sangeeta.nair@hospital.com", "Skin treatments and cosmetic procedures"),
            
            # General Medicine
            ("Dr. Arjun Mishra", "MBBS, MD General Medicine", "Senior Consultant", 14, 700, "arjun.mishra@hospital.com", "General health and wellness"),
            ("Dr. Meera Iyer", "MBBS, MD General Medicine", "Consultant", 8, 600, "meera.iyer@hospital.com", "Chronic disease management"),
            
            # Pediatrics
            ("Dr. Rohan Kapoor", "MBBS, MD Pediatrics", "Consultant", 10, 750, "rohan.kapoor@hospital.com", "Child health and development"),
            
            # Psychiatry
            ("Dr. Shruti Malhotra", "MBBS, MD Psychiatry", "Senior Consultant", 13, 900, "shruti.malhotra@hospital.com", "Mental health and counseling"),
        ]

        doctors = []
        dept_list = list(departments.values())
        dept_index = 0
        
        for full_name, qualification, designation, experience, fees, email, intro in doctors_data:
            doc_user = User(
                username=full_name.lower().replace(" ", "").replace(".", ""),
                password=generate_password_hash("password", method="pbkdf2:sha256"),
                role="doctor"
            )
            db.session.add(doc_user)
            db.session.flush()
            
            doctor = Doctor(
                user_id=doc_user.id,
                department_id=dept_list[dept_index].id,
                full_name=full_name,
                qualification=qualification,
                designation=designation,
                experience=experience,
                doctor_fees=fees,
                email=email,
                intro=intro
            )
            db.session.add(doctor)
            doctors.append(doctor)
            db.session.flush()
            dept_index = (dept_index + 1) % len(dept_list)
        
        db.session.commit()

        # ============ DOCTOR AVAILABILITY ============
        print("📅 Seeding Doctor Availability...")
        today = date.today()
        
        for doctor in doctors:
            # Add availability for next 14 days
            for day_offset in range(1, 15):
                avail_date = today + timedelta(days=day_offset)
                
                # Random working hours
                if avail_date.weekday() < 5:  # Weekdays only
                    start_hour = random.choice([8, 9, 10])
                    avail = DoctorAvailability(
                        doctor_id=doctor.id,
                        date=avail_date,
                        day_of_week=avail_date.strftime("%A"),
                        start_time=time(start_hour, 0),
                        end_time=time(start_hour + 4, 30),
                        is_available=True
                    )
                    db.session.add(avail)
            
            db.session.flush()
        db.session.commit()

        # ============ PATIENTS ============
        print("👥 Seeding Patients...")
        patient_names = [
            ("Rahul Verma", "rahul.verma", 32, "9876543210", "Mumbai"),
            ("Divya Kulkarni", "divya.kulkarni", 28, "9876543211", "Pune"),
            ("Sanjay Nambiar", "sanjay.nambiar", 45, "9876543212", "Bangalore"),
            ("Priya Rao", "priya.rao", 35, "9876543213", "Hyderabad"),
            ("Arun Banerjee", "arun.banerjee", 52, "9876543214", "Kolkata"),
            ("Sneha Chopra", "sneha.chopra", 29, "9876543215", "Delhi"),
            ("Vikram Sharma", "vikram.sharma", 41, "9876543216", "Chennai"),
            ("Anjali Singh", "anjali.singh", 26, "9876543217", "Jaipur"),
            ("Rohit Saxena", "rohit.saxena", 38, "9876543218", "Ahmedabad"),
            ("Pooja Bhat", "pooja.bhat", 31, "9876543219", "Goa"),
        ]

        patients = []
        for full_name, username, age, phone, address in patient_names:
            pat_user = User(
                username=username,
                password=generate_password_hash("password", method="pbkdf2:sha256"),
                role="patient"
            )
            db.session.add(pat_user)
            db.session.flush()
            
            patient = Patient(
                user_id=pat_user.id,
                full_name=full_name,
                phone=phone,
                address=f"{age} Park Street, {address}",
                age=age,
                email=f"{username}@example.com"
            )
            db.session.add(patient)
            patients.append(patient)
            db.session.flush()
        
        db.session.commit()

        # ============ APPOINTMENTS & TREATMENTS ============
        print("📋 Seeding Appointments and Treatments...")
        
        diagnoses = [
            "Hypertension", "Migraine", "Acute Bronchitis", "Anxiety Disorder",
            "Arthritis", "Gastritis", "Acne Vulgaris", "Insomnia",
            "Type 2 Diabetes", "Lower Back Pain", "Seasonal Allergies"
        ]
        
        prescriptions = [
            "Aspirin 100mg once daily",
            "Paracetamol 500mg as needed",
            "Amoxicillin 500mg thrice daily",
            "Metformin 1000mg twice daily",
            "Atorvastatin 10mg once daily",
            "Lisinopril 10mg once daily",
            "Omeprazole 20mg once daily",
            "Cetirizine 10mg once daily"
        ]

        # Create past appointments (Completed)
        past_date = today - timedelta(days=30)
        for patient in patients[:5]:
            for _ in range(random.randint(1, 3)):
                doctor = random.choice(doctors)
                appt_date = past_date + timedelta(days=random.randint(0, 25))
                
                appt = Appointment(
                    patient_id=patient.id,
                    doctor_id=doctor.id,
                    date_scheduled=appt_date,
                    time_scheduled=time(random.randint(9, 16), 0),
                    status="Completed"
                )
                db.session.add(appt)
                db.session.flush()
                
                # Add treatment for completed appointments
                treatment = Treatment(
                    appointment_id=appt.id,
                    diagnosis=random.choice(diagnoses),
                    prescription=random.choice(prescriptions),
                    notes=f"Patient reported {random.choice(['improvement', 'no change', 'slight discomfort'])}. Advised lifestyle changes.",
                    visit_type=random.choice(["In-person", "Tele-consultation"]),
                    tests_done=random.choice(["Blood Test, ECG", "X-Ray", "Ultrasound", "Complete Blood Count", "Thyroid Profile"])
                )
                db.session.add(treatment)

        db.session.commit()

        # Create upcoming appointments (Scheduled)
        for patient in patients:
            for _ in range(random.randint(1, 2)):
                doctor = random.choice(doctors)
                future_date = today + timedelta(days=random.randint(1, 7))
                
                appt = Appointment(
                    patient_id=patient.id,
                    doctor_id=doctor.id,
                    date_scheduled=future_date,
                    time_scheduled=time(random.randint(9, 16), random.choice([0, 30])),
                    status="Scheduled"
                )
                db.session.add(appt)

        db.session.commit()

        # ============ SUMMARY ============
        print("\n" + "="*60)
        print("✅ DATABASE SUCCESSFULLY SEEDED!")
        print("="*60)
        print("\n📊 STATISTICS:")
        print(f"   • Admins: 1")
        print(f"   • Departments: {len(departments_data)}")
        print(f"   • Doctors: {len(doctors_data)}")
        print(f"   • Patients: {len(patient_names)}")
        print(f"   • Appointments: {len(patients) * 2 + len(patients[:5]) * 2}")
        print(f"   • Completed Treatments: {len(patients[:5]) * 2}")

        print("\n🔐 TEST CREDENTIALS:")
        print("-" * 60)
        print("Admin Account:")
        print("  Username: admin    | Password: admin")
        print("\nDoctor Accounts (all use password: 'password'):")
        for fname, _, _, _, _, _, _ in doctors_data[:3]:
            username = fname.lower().replace(" ", "").replace(".", "")
            print(f"  Username: {username}")
        print("  ... and more doctors available")
        print("\nPatient Accounts (all use password: 'password'):")
        for fname, username, _, _, _ in patient_names[:3]:
            print(f"  Username: {username}")
        print("  ... and more patients available")
        print("="*60)

if __name__ == "__main__":
    seed_database()