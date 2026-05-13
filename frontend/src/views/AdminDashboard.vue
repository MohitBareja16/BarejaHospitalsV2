<template>
  <div class="container mt-4 mb-5">
    <div class="d-flex justify-content-between align-items-center mb-4 border-bottom border-secondary pb-3">
      <h2 class="text-light fw-bold m-0" style="text-shadow: 0 0 10px rgba(0, 243, 255, 0.3);">
        <span style="color: var(--neon-cyan);">System</span> Overview
      </h2>
      <button @click="handleLogout" class="btn btn-outline-danger rounded-pill px-4">Logout</button>
    </div>

    <div class="row mb-4">
      <div class="col-md-4">
        <div class="card glass-card rounded-4 p-3 text-center mb-3">
          <h5 class="text-light opacity-75 mb-1">Total Doctors</h5>
          <h2 style="color: var(--neon-cyan);">{{ dashboardData.counts?.doctors || 0 }}</h2>
        </div>
      </div>
      <div class="col-md-4">
        <div class="card glass-card rounded-4 p-3 text-center mb-3">
          <h5 class="text-light opacity-75 mb-1">Total Patients</h5>
          <h2 style="color: var(--neon-mint);">{{ dashboardData.counts?.patients || 0 }}</h2>
        </div>
      </div>
      <div class="col-md-4">
        <div class="card glass-card rounded-4 p-3 text-center mb-3">
          <h5 class="text-light opacity-75 mb-1">Total Appointments</h5>
          <h2 class="text-warning">{{ dashboardData.counts?.appointments || 0 }}</h2>
        </div>
      </div>
    </div>

    <div class="row mb-4">
      <div class="col-12">
        <div class="input-group glass-card rounded-pill p-1">
          <span class="input-group-text bg-transparent border-0 text-light"><i class="bi bi-search"></i></span>
          <input type="text" class="form-control glass-input bg-transparent border-0 text-white shadow-none" 
                 v-model="searchQuery" 
                 placeholder="Search doctors, patients, or departments...">
        </div>
      </div>
    </div>

    <div class="card glass-card rounded-4 p-4 mb-4">
      <div class="d-flex justify-content-between align-items-center mb-4 bg-dark p-3 rounded-3 shadow-sm" style="border: 1px solid rgba(255,255,255,0.1);">
        <h4 class="text-white fw-bold m-0">Registered Doctors</h4>
        <div>
          <button class="btn btn-outline-info btn-sm rounded-pill px-3 me-2" data-bs-toggle="modal" data-bs-target="#addDeptModal">+ Add Dept</button>
          <button class="btn btn-outline-info btn-sm rounded-pill px-3 me-2" data-bs-toggle="modal" data-bs-target="#addDoctorModal">+ Add Doctor</button>
        </div>
      </div>
      <div class="table-responsive">
        <table class="table table-dark table-hover table-borderless align-middle custom-table">
          <thead style="border-bottom: 1px solid var(--glass-border);">
            <tr>
              <th class="text-light">Name</th>
              <th class="text-light">Department</th>
              <th class="text-light">Fees</th>
              <th class="text-light text-end">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="doc in filteredDoctors" :key="'doc-'+doc.id">
              <td class="fw-bold">{{ doc.name }}</td>
              <td><span class="badge bg-secondary rounded-pill">{{ doc.department }}</span></td>
              <td>₹{{ doc.fees }}</td>
              <td class="text-end">
                <button @click="openEditDoctor(doc)" class="btn btn-sm btn-outline-info rounded-pill me-2" data-bs-toggle="modal" data-bs-target="#editDoctorModal">Edit</button>
                <button v-if="doc.user_id" @click="openBlacklistModal(doc.user_id, doc.name, doc.is_blacklisted)" 
                    class="btn btn-sm rounded-pill me-2" 
                    :class="doc.is_blacklisted ? 'btn-success' : 'btn-outline-warning'" 
                    data-bs-toggle="modal" data-bs-target="#blacklistModal">
                    {{ doc.is_blacklisted ? 'Unblock' : 'Blacklist' }}
                </button>
                <button @click="removeDoctor(doc.id)" class="btn btn-sm btn-outline-danger rounded-pill">Remove</button>
                </td>
            </tr>
            <tr v-if="filteredDoctors.length === 0">
              <td colspan="4" class="text-center text-light py-4">No doctors found.</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <div class="card glass-card rounded-4 p-4 mb-4">
      <div class="d-flex justify-content-between align-items-center mb-4 bg-dark p-3 rounded-3 shadow-sm" style="border: 1px solid rgba(255,255,255,0.1);">
        <h4 class="text-white fw-bold m-0">Registered Patients</h4>
      </div>
      <div class="table-responsive">
        <table class="table table-dark table-hover table-borderless align-middle custom-table">
          <thead style="border-bottom: 1px solid var(--glass-border);">
            <tr>
              <th class="text-light">Name</th>
              <th class="text-light">Age</th>
              <th class="text-light">Contact</th>
              <th class="text-light text-end">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="pat in filteredPatients" :key="'pat-'+pat.id">
              <td class="fw-bold">{{ pat.name }}</td>
              <td>{{ pat.age }}</td>
              <td>{{ pat.phone }}</td>
              <td class="text-end">
                <button @click="openEditPatient(pat)" class="btn btn-sm btn-outline-light rounded-pill me-2" data-bs-toggle="modal" data-bs-target="#editPatientModal">Edit</button>
                <button @click="viewPatientHistory(pat.id)" class="btn btn-sm btn-outline-info rounded-pill me-2" data-bs-toggle="modal" data-bs-target="#patientHistoryModal">History</button>
                <button @click="openBlacklistModal(pat.user_id, pat.name, pat.is_blacklisted)" class="btn btn-sm rounded-pill me-2" :class="pat.is_blacklisted ? 'btn-success' : 'btn-outline-warning'" data-bs-toggle="modal" data-bs-target="#blacklistModal">
                    {{ pat.is_blacklisted ? 'Unblock' : 'Blacklist' }}
                </button>
                <button @click="removePatient(pat.id)" class="btn btn-sm btn-outline-danger rounded-pill me-2">Remove</button>
               </td>
            </tr>
            <tr v-if="filteredPatients.length === 0">
              <td colspan="4" class="text-center text-light py-4">No patients found.</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <div class="card glass-card rounded-4 p-4 mb-4">
      <div class="d-flex justify-content-between align-items-center mb-4 bg-dark p-3 rounded-3 shadow-sm" style="border: 1px solid rgba(255,255,255,0.1);">
        <h4 class="text-white fw-bold m-0">System Appointments</h4>
      </div>
      <div class="table-responsive">
        <table class="table table-dark table-hover table-borderless align-middle custom-table">
          <thead style="border-bottom: 1px solid var(--glass-border);">
            <tr>
              <th class="text-light">Date & Time</th>
              <th class="text-light">Patient</th>
              <th class="text-light">Doctor</th>
              <th class="text-light">Department</th>
              <th class="text-light">Status</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="appt in (dashboardData.appointments || [])" :key="'appt-'+appt.id">
              <td>{{ appt.date }} <br><small class="text-light">{{ appt.time }}</small></td>
              <td class="fw-bold">{{ appt.patient_name }}</td>
              <td>{{ appt.doctor_name }}</td>
              <td>{{ appt.department }}</td>
              <td>
                <span class="badge rounded-pill" :class="appt.status === 'Completed' ? 'bg-success' : (appt.status === 'Cancelled' ? 'bg-danger' : 'bg-info text-dark')">
                  {{ appt.status }}
                </span>
              </td>
            </tr>
            <tr v-if="!dashboardData.appointments || dashboardData.appointments.length === 0">
              <td colspan="5" class="text-center text-light py-4">No appointments in the system.</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <div class="modal fade" id="addDeptModal" tabindex="-1" aria-hidden="true">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content glass-card rounded-4 border-0">
          <div class="modal-header border-secondary">
            <h5 class="modal-title" style="color: var(--neon-cyan);">Add New Department</h5>
            <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal" id="closeDeptModal"></button>
          </div>
          <div class="modal-body p-4">
            <form @submit.prevent="submitAddDepartment">
              <div class="mb-3">
                <label class="form-label text-light small">Department Name</label>
                <input type="text" class="form-control glass-input" v-model="newDept.name" required placeholder="e.g., Cardiology">
              </div>
              <div class="mb-4">
                <label class="form-label text-light small">Description & Focus Area</label>
                <textarea class="form-control glass-input" v-model="newDept.description" rows="3" required placeholder="Describe the conditions treated..."></textarea>
              </div>
              <button type="submit" class="btn btn-outline-info w-100 rounded-pill">CREATE DEPARTMENT</button>
            </form>
          </div>
        </div>
      </div>
    </div>

    <div class="modal fade" id="addDoctorModal" tabindex="-1" aria-hidden="true">
      <div class="modal-dialog modal-dialog-centered modal-lg">
        <div class="modal-content glass-card rounded-4 border-0">
          <div class="modal-header border-secondary">
            <h5 class="modal-title" style="color: var(--neon-cyan);">Register New Doctor</h5>
            <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal" id="closeAddDoctorModal"></button>
          </div>
          <div class="modal-body p-4">
            <form @submit.prevent="submitAddDoctor">
              <h6 class="text-light border-bottom border-secondary pb-2 mb-3">1. Account Details</h6>
              <div class="row mb-3">
                <div class="col-md-4">
                  <label class="form-label text-light small">Full Name</label>
                  <input type="text" class="form-control glass-input" v-model="newDoctor.full_name" required>
                </div>
                <div class="col-md-6">
                  <label class="form-label text-light small">Email Address</label>
                  <input type="email" class="form-control glass-input" v-model="editDoctorData.email" required>
                </div>
                <div class="col-md-4">
                  <label class="form-label text-light small">Username (Login)</label>
                  <input type="text" class="form-control glass-input" v-model="newDoctor.username" required>
                </div>
                <div class="col-md-4">
                  <label class="form-label text-light small">Password</label>
                  <input type="password" class="form-control glass-input" v-model="newDoctor.password" required>
                </div>
              </div>

              <h6 class="text-light border-bottom border-secondary pb-2 mb-3 mt-4">2. Professional Profile</h6>
              <div class="row mb-3">
                <div class="col-md-6">
                  <label class="form-label text-light small">Department</label>
                  <select class="form-select glass-input" v-model="newDoctor.department_id" required>
                    <option value="" disabled selected>Select Dept...</option>
                    <option v-for="dept in departments" :key="dept.id" :value="dept.id">{{ dept.name }}</option>
                  </select>
                </div>
                <div class="col-md-6">
                  <label class="form-label text-light small">Consultation Fee (₹)</label>
                  <input type="number" class="form-control glass-input" v-model="newDoctor.doctor_fees" required>
                </div>
              </div>

              <div class="row mb-3">
                <div class="col-md-6">
                  <label class="form-label text-light small">Qualifications</label>
                  <input type="text" class="form-control glass-input" v-model="newDoctor.qualification" required>
                </div>
                <div class="col-md-4">
                  <label class="form-label text-light small">Designation</label>
                  <input type="text" class="form-control glass-input" v-model="newDoctor.designation" required>
                </div>
                <div class="col-md-2">
                  <label class="form-label text-light small">Exp. (Years)</label>
                  <input type="number" class="form-control glass-input" v-model="newDoctor.experience" required>
                </div>
              </div>

              <div class="mb-4">
                <label class="form-label text-light small">Brief Intro</label>
                <textarea class="form-control glass-input" v-model="newDoctor.intro" rows="2" required></textarea>
              </div>

              <button type="submit" class="btn btn-neon w-100 rounded-pill" style="color: var(--neon-mint); border-color: var(--neon-mint);">REGISTER DOCTOR</button>
            </form>
          </div>
        </div>
      </div>
    </div>

    <div class="modal fade" id="editPatientModal" tabindex="-1" aria-hidden="true">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content glass-card rounded-4 border-0">
          <div class="modal-header border-secondary">
            <h5 class="modal-title" style="color: var(--neon-mint);">Edit Patient Record</h5>
            <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal" id="closeEditPatientModal"></button>
          </div>
          <div class="modal-body p-4">
            <form @submit.prevent="submitEditPatient">
              <div class="mb-3">
                <label class="form-label text-light small">Full Name</label>
                <input type="text" class="form-control glass-input" v-model="editPatientData.full_name" required>
              </div>
              <div class="mb-3">
                <label class="form-label text-light small">Email Address</label>
                <input type="email" class="form-control glass-input" v-model="editPatientData.email" required>
              </div>
              <div class="row mb-4">
                <div class="col-4">
                  <label class="form-label text-light small">Age</label>
                  <input type="number" class="form-control glass-input" v-model="editPatientData.age" required>
                </div>
                <div class="col-8">
                  <label class="form-label text-light small">Contact Number</label>
                  <input type="text" class="form-control glass-input" v-model="editPatientData.phone" required>
                </div>
              </div>
              <button type="submit" class="btn w-100 rounded-pill fw-bold" style="background: var(--neon-mint); color: #000;">SAVE PATIENT</button>
            </form>
          </div>
        </div>
      </div>
    </div>

    <div class="modal fade" id="patientHistoryModal" tabindex="-1" aria-hidden="true">
      <div class="modal-dialog modal-dialog-centered modal-xl">
        <div class="modal-content glass-card rounded-4 border-0">
          <div class="modal-header border-secondary">
            <h5 class="modal-title" style="color: var(--neon-mint);">
              Medical History: <span class="text-white">{{ activePatientName }}</span>
            </h5>
            <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
          </div>
          <div class="modal-body p-4">
            <div class="table-responsive">
              <table class="table table-dark table-hover table-borderless align-middle custom-table">
                <thead style="border-bottom: 1px solid var(--glass-border);">
                  <tr>
                    <th class="text-light">Date</th>
                    <th class="text-light">Consulting Doctor</th>
                    <th class="text-light">Visit Type</th>
                    <th class="text-light">Diagnosis</th>
                    <th class="text-light">Prescription</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="record in patientHistoryData" :key="record.id">
                    <td>{{ record.date }}</td>
                    <td class="fw-bold">{{ record.doctor_name }} <br><small class="text-light">{{ record.department }}</small></td>
                    <td><span class="badge bg-secondary rounded-pill">{{ record.visit_type }}</span></td>
                    <td>{{ record.diagnosis }}</td>
                    <td>{{ record.prescription }}</td>
                  </tr>
                  <tr v-if="patientHistoryData.length === 0">
                    <td colspan="5" class="text-center text-light py-4">No completed consultation records found.</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </div>

  </div>
  <div class="modal fade" id="editDoctorModal" tabindex="-1" aria-hidden="true">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content glass-card rounded-4 border-0">
          <div class="modal-header border-secondary">
            <h5 class="modal-title" style="color: var(--neon-cyan);">Edit Doctor Profile</h5>
            <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal" id="closeEditDoctorModal"></button>
          </div>
          <div class="modal-body p-4">
            <form @submit.prevent="submitEditDoctor">
              <div class="mb-3">
                <label class="form-label text-light small">Full Name</label>
                <input type="text" class="form-control glass-input" v-model="editDoctorData.full_name" required>
              </div>
              <div class="row mb-4">
                <div class="col-6">
                  <label class="form-label text-light small">Department</label>
                  <select class="form-select glass-input" v-model="editDoctorData.department_id" required>
                    <option v-for="dept in departments" :key="dept.id" :value="dept.id">{{ dept.name }}</option>
                  </select>
                </div>
                <div class="col-6">
                  <label class="form-label text-light small">Consultation Fee (₹)</label>
                  <input type="number" class="form-control glass-input" v-model="editDoctorData.doctor_fees" required>
                </div>
              </div>
              
              <div class="row mb-3">
                <div class="col-md-6">
                  <label class="form-label text-light small">Qualifications</label>
                  <input type="text" class="form-control glass-input" v-model="editDoctorData.qualification" required>
                </div>
                <div class="col-md-4">
                  <label class="form-label text-light small">Designation</label>
                  <input type="text" class="form-control glass-input" v-model="editDoctorData.designation" required>
                </div>
                <div class="col-md-2">
                  <label class="form-label text-light small">Exp.</label>
                  <input type="number" class="form-control glass-input" v-model="editDoctorData.experience" required>
                </div>
              </div>
              <div class="mb-4">
                <label class="form-label text-light small">Brief Intro</label>
                <textarea class="form-control glass-input" v-model="editDoctorData.intro" rows="2" required></textarea>
              </div>

              <button type="submit" class="btn btn-outline-info w-100 rounded-pill">SAVE CHANGES</button>
            </form>
          </div>
        </div>
      </div>
    </div>

    <div class="modal fade" id="blacklistModal" tabindex="-1" aria-hidden="true">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content glass-card rounded-4 border-0">
          <div class="modal-header border-secondary">
            <h5 class="modal-title" :class="blacklistData.is_blacklisted ? 'text-success' : 'text-warning'">
              {{ blacklistData.is_blacklisted ? 'Restore Access' : 'Suspend Account' }}
            </h5>
            <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal" id="closeBlacklistModal"></button>
          </div>
          <div class="modal-body p-4 text-center">
            <i class="bi fs-1 mb-3 d-block" :class="blacklistData.is_blacklisted ? 'bi-shield-check text-success' : 'bi-shield-lock text-warning'"></i>
            <p class="text-light mb-4">
              Are you sure you want to {{ blacklistData.is_blacklisted ? 'restore' : 'suspend' }} access for <strong>{{ blacklistData.name }}</strong>?
            </p>
            <div class="d-flex justify-content-center gap-3">
              <button type="button" class="btn btn-outline-light rounded-pill px-4" data-bs-dismiss="modal">Cancel</button>
              <button @click="confirmBlacklist" type="button" class="btn rounded-pill px-4" :class="blacklistData.is_blacklisted ? 'btn-success' : 'btn-warning'">
                Confirm {{ blacklistData.is_blacklisted ? 'Restore' : 'Suspend' }}
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { apiConfig } from '../config'

const router = useRouter()

const dashboardData = ref({
  counts: { doctors: 0, patients: 0, appointments: 0 },
  doctors: [],
  patients: [],
  appointments: []
})

const departments = ref([])
const searchQuery = ref('')

const newDept = ref({ name: '', description: '' })
const newDoctor = ref({ 
  username: '', password: '', full_name: '', email: '', department_id: '', doctor_fees: 500,
  qualification: '', designation: '', experience: 0, intro: ''
})

const patientHistoryData = ref([])
const activePatientName = ref('')
const editDoctorData = ref({ 
  id: null, full_name: '', email: '', department_id: '', doctor_fees: 0,
  qualification: '', designation: '', experience: 0, intro: '' 
})
const editPatientData = ref({ id: null, full_name: '', email: '', age: '', phone: '' })
const blacklistData = ref({ user_id: null, name: '', is_blacklisted: false })

const filteredDoctors = computed(() => {
  const docs = dashboardData.value.doctors || []
  if (!searchQuery.value) return docs
  
  return docs.filter(d => {
    const docName = d.name || ''
    const docDept = d.department || ''
    return docName.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
           docDept.toLowerCase().includes(searchQuery.value.toLowerCase())
  })
})

const filteredPatients = computed(() => {
  const pats = dashboardData.value.patients || []
  if (!searchQuery.value) return pats
  
  const term = searchQuery.value.toLowerCase()
  
  return pats.filter(p => {
    const matchName = (p.name || '').toLowerCase().includes(term)
    const matchPhone = (p.phone || '').includes(term)
    const matchId = String(p.id) === term
    
    return matchName || matchPhone || matchId
  })
})

const fetchDashboardData = async () => {
  const token = localStorage.getItem('access_token')
  if (!token) { router.push('/'); return; }
  
  try {
    const res = await fetch(apiConfig.adminDashboard, {
      headers: { 'Authorization': `Bearer ${token}` }
    })
    
    if (res.ok) {
      dashboardData.value = await res.json()
    } else if (res.status === 401 || res.status === 403) {
      handleLogout()
    }
  } catch (err) { console.error("Error fetching dashboard:", err) }
}

const fetchDepartments = async () => {
  try {
    const res = await fetch(apiConfig.departments)
    if (res.ok) departments.value = await res.json()
  } catch (err) { console.error("Error fetching departments:", err) }
}

onMounted(() => {
  fetchDashboardData()
  fetchDepartments()
})


const submitAddDepartment = async () => {
  const token = localStorage.getItem('access_token')
  try {
    const res = await fetch(apiConfig.addDepartment, {
      method: 'POST',
      headers: { 'Authorization': `Bearer ${token}`, 'Content-Type': 'application/json' },
      body: JSON.stringify(newDept.value)
    })
    const data = await res.json()
    if (res.ok) {
      alert("System Notice: " + data.message)
      document.getElementById('closeDeptModal').click()
      newDept.value = { name: '', description: '' }
      fetchDepartments()
      fetchDashboardData()
    } else alert("Error: " + data.error)
  } catch (err) { console.error(err) }
}

const submitAddDoctor = async () => {
  const token = localStorage.getItem('access_token')
  try {
    const res = await fetch(apiConfig.addDoctor, {
      method: 'POST',
      headers: { 'Authorization': `Bearer ${token}`, 'Content-Type': 'application/json' },
      body: JSON.stringify(newDoctor.value)
    })
    const data = await res.json()
    if (res.ok) {
      alert("System Notice: " + data.message)
      document.getElementById('closeAddDoctorModal').click()
      newDoctor.value = { 
        username: '', password: '', full_name: '', email: '', department_id: '', doctor_fees: 500,
        qualification: '', designation: '', experience: 0, intro: '' 
      }
      fetchDashboardData() 
    } else alert("Error: " + data.error)
  } catch (err) { console.error(err) }
}

const openEditDoctor = (doc) => {
  const dept = departments.value.find(d => d.name === doc.department)
  editDoctorData.value = {
    id: doc.id,
    full_name: doc.name,
    department_id: dept ? dept.id : '',
    email: doc.email,
    doctor_fees: doc.fees,
    qualification: doc.qualification,
    designation: doc.designation,
    experience: doc.experience,
    intro: doc.intro
  }
}

const openEditPatient = (pat) => {
  editPatientData.value = {
    id: pat.id,
    full_name: pat.name,
    email: pat.email,
    age: pat.age,
    phone: pat.phone
  }
}

const submitEditDoctor = async () => {
  const token = localStorage.getItem('access_token')
  try {
    const res = await fetch(apiConfig.manageDoctors(editDoctorData.value.id), {
      method: 'PUT',
      headers: { 'Authorization': `Bearer ${token}`, 'Content-Type': 'application/json' },
      body: JSON.stringify(editDoctorData.value)
    })
    const data = await res.json()
    if (res.ok) {
      document.getElementById('closeEditDoctorModal').click()
      fetchDashboardData()
    } else alert("Error: " + data.error)
  } catch (err) { console.error(err) }
}

const submitEditPatient = async () => {
  const token = localStorage.getItem('access_token')
  try {
    const res = await fetch(apiConfig.managePatients(editPatientData.value.id), {
      method: 'PUT',
      headers: { 'Authorization': `Bearer ${token}`, 'Content-Type': 'application/json' },
      body: JSON.stringify(editPatientData.value)
    })
    const data = await res.json()
    if (res.ok) {
      document.getElementById('closeEditPatientModal').click()
      fetchDashboardData()
    } else alert("Error: " + data.error)
  } catch (err) { console.error(err) }
}

const openBlacklistModal = (userId, name, isBlacklisted) => {
  blacklistData.value = { 
    user_id: userId, 
    name: name, 
    is_blacklisted: isBlacklisted 
  }
}

const confirmBlacklist = async () => {
  const token = localStorage.getItem('access_token')
  if (!blacklistData.value.user_id) {
    alert("Error: Missing User ID.")
    return
  }

  try {
    const res = await fetch(apiConfig.toggleBlacklist(blacklistData.value.user_id), {
      method: 'PUT',
      headers: { 'Authorization': `Bearer ${token}` }
    })
    
    const data = await res.json()
    
    if (res.ok) {
      alert("System Notice: " + data.message)
      document.getElementById('closeBlacklistModal').click()
      fetchDashboardData()
    } else {
      alert("Error: " + (data.error || "Failed to update status."))
    }
  } catch (err) { 
    console.error("Network Error:", err) 
    alert("Critical Error connecting to server.")
  }
}

const removeDoctor = async (id) => {
  if (!confirm("Are you sure you want to permanently delete this doctor?")) return;
  const token = localStorage.getItem('access_token')
  try {
    const res = await fetch(apiConfig.manageDoctors(id), {
      method: 'DELETE',
      headers: { 'Authorization': `Bearer ${token}` }
    })
    if (res.ok) fetchDashboardData()
    else alert("Error removing doctor.")
  } catch (err) { console.error(err) }
}

const removePatient = async (id) => {
  if (!confirm("Are you sure you want to permanently delete this patient?")) return;
  const token = localStorage.getItem('access_token')
  try {
    const res = await fetch(apiConfig.managePatients(id), {
      method: 'DELETE',
      headers: { 'Authorization': `Bearer ${token}` }
    })
    if (res.ok) fetchDashboardData()
    else alert("Error removing patient.")
  } catch (err) { console.error(err) }
}

const toggleBlacklist = async (userId) => {
  const token = localStorage.getItem('access_token')
  try {
    const res = await fetch(apiConfig.toggleBlacklist(userId), {
      method: 'PUT',
      headers: { 'Authorization': `Bearer ${token}` }
    })
    const data = await res.json()
    if (res.ok) {
      alert("System Notice: " + data.message)
      fetchDashboardData()
    } else alert("Error: " + data.error)
  } catch (err) { console.error(err) }
}

const viewPatientHistory = async (id) => {
  patientHistoryData.value = []
  activePatientName.value = 'Loading...'
  const token = localStorage.getItem('access_token')
  try {
    const res = await fetch(apiConfig.patientHistory(id), {
      headers: { 'Authorization': `Bearer ${token}` }
    })
    if (res.ok) {
      const data = await res.json()
      patientHistoryData.value = data.history
      activePatientName.value = data.patient_name
    } else {
      activePatientName.value = "Error loading data"
    }
  } catch (err) { console.error(err) }
}

const handleLogout = () => {
  localStorage.clear()
  router.push('/')
}
</script>

<style scoped>
.custom-table { background: transparent !important; }
.custom-table tbody tr { border-bottom: 1px solid rgba(255, 255, 255, 0.05); }
.custom-table td { background: transparent !important; color: #e0e0e0; }

.glass-input::placeholder {
  color: #e0e0e0 !important;
  opacity: 1 !important; 
}
</style>