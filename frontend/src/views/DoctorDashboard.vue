<template>
  <div class="container mt-4 mb-5">
    <div class="d-flex justify-content-between align-items-center mb-4 border-bottom border-secondary pb-3">
      <div>
        <h2 class="text-light fw-bold m-0" style="text-shadow: 0 0 10px rgba(0, 243, 255, 0.3);">
          Dr. <span style="color: var(--neon-mint);">{{ dashboardData.doctor_name || 'Loading...' }}</span>
        </h2>
        <p class="text-light mb-0">{{ dashboardData.department || 'Department' }} Division</p>
      </div>
      <div>
        <button class="btn btn-outline-info rounded-pill px-3 me-2" data-bs-toggle="modal" data-bs-target="#addAvailabilityModal">
          <i class="bi bi-clock"></i> Set Availability
        </button>
        <button @click="handleLogout" class="btn btn-outline-danger rounded-pill px-4">Logout</button>
      </div>
    </div>

    <div class="row">
      <div class="col-lg-7 mb-4">
        <div class="card glass-card rounded-4 p-4 h-100">
          <div class="d-flex justify-content-between align-items-center mb-4 bg-dark p-3 rounded-3 shadow-sm" style="border: 1px solid rgba(255,255,255,0.1);">
            <h4 class="text-white fw-bold m-0">Today & Upcoming Appointments</h4>
          </div>
          
          <div v-if="dashboardData.appointments.length === 0" class="text-center text-light py-4">
            No appointments scheduled at this time.
          </div>

          <div v-for="appt in dashboardData.appointments" :key="appt.id" 
               class="card bg-transparent border-secondary rounded-4 p-3 mb-3 border-start border-4" 
               :class="appt.status === 'Completed' ? 'border-success' : (appt.status === 'Cancelled' ? 'border-danger' : 'border-info')">
            <div class="d-flex justify-content-between align-items-center">
              <div>
                <h5 class="text-light fw-bold m-0">{{ appt.patient_name }}</h5>
                <small class="text-light"><i class="bi bi-calendar-event"></i> {{ appt.date }} at {{ appt.time }}</small>
              </div>
              <div class="text-end">
                <span class="badge rounded-pill mb-2 d-block" 
                      :class="appt.status === 'Completed' ? 'bg-success' : (appt.status === 'Cancelled' ? 'bg-danger' : 'bg-info text-dark')">
                  {{ appt.status }}
                </span>
                
                <div v-if="appt.status === 'Scheduled'">
                  <button @click="openTreatmentModal(appt.id)" class="btn btn-sm btn-neon rounded-pill px-3 me-1" data-bs-toggle="modal" data-bs-target="#treatmentModal" style="color: var(--neon-mint); border-color: var(--neon-mint);">Complete</button>
                  <button @click="cancelAppointment(appt.id)" class="btn btn-sm btn-outline-danger rounded-pill px-2">Cancel</button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="col-lg-5 mb-4">
        <div class="card glass-card rounded-4 p-4 h-100">
          <div class="d-flex justify-content-between align-items-center mb-4 bg-dark p-3 rounded-3 shadow-sm" style="border: 1px solid rgba(255,255,255,0.1);">
            <h4 class="text-white fw-bold m-0">My Patients</h4>
          </div>
          
          <ul class="list-group list-group-flush bg-transparent">
            <li v-for="pat in dashboardData.patients" :key="pat.id" class="list-group-item bg-transparent text-light border-secondary d-flex justify-content-between align-items-center px-0 py-3">
              <div>
                <strong class="fs-5">{{ pat.name }}</strong><br>
                <small class="text-light">Age: {{ pat.age || 'N/A' }} | Contact: {{ pat.phone || 'N/A' }}</small>
              </div>
              <button @click="viewPatientHistory(pat.id)" class="btn btn-sm btn-outline-light rounded-pill px-3" data-bs-toggle="modal" data-bs-target="#patientHistoryModal">
                History
              </button>
            </li>
            <li v-if="dashboardData.patients.length === 0" class="list-group-item bg-transparent text-light text-center border-0 py-4">
              No assigned patients found.
            </li>
          </ul>
        </div>
      </div>
    </div>

    <div class="modal fade" id="addAvailabilityModal" tabindex="-1" aria-hidden="true">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content glass-card rounded-4 border-0">
          <div class="modal-header border-secondary">
            <h5 class="modal-title" style="color: var(--neon-cyan);">Set Availability</h5>
            <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal" id="closeAvailabilityModal"></button>
          </div>
          <div class="modal-body p-4">

            <form @submit.prevent="submitAvailability">
              
              <div class="mb-4">
                <label class="form-label text-light small mb-2">Select Upcoming Date</label>
                <div class="d-flex flex-wrap gap-2">
                  <button type="button" 
                          v-for="dayObj in next7Days" 
                          :key="dayObj.fullDate"
                          @click="availabilityForm.date = dayObj.fullDate"
                          class="btn btn-sm rounded-pill px-3"
                          :class="availabilityForm.date === dayObj.fullDate ? 'btn-neon text-dark fw-bold' : 'btn-outline-secondary text-light'"
                          style="transition: all 0.2s ease;">
                    {{ dayObj.display }}
                  </button>
                </div>
              </div>

              <div class="mb-4">
                <label class="form-label text-light small mb-2">Quick Presets</label>
                <div class="d-flex gap-2">
                  <button type="button" @click="setShift('09:00', '13:00')" class="btn btn-sm btn-outline-info rounded-pill">Morning (9am-1pm)</button>
                  <button type="button" @click="setShift('14:00', '18:00')" class="btn btn-sm btn-outline-info rounded-pill">Afternoon (2pm-6pm)</button>
                  <button type="button" @click="setShift('18:00', '22:00')" class="btn btn-sm btn-outline-info rounded-pill">Evening (6pm-10pm)</button>
                </div>
              </div>

              <div class="row mb-4">
                <div class="col-6">
                  <label class="form-label text-light small">Start Time</label>
                  <select class="form-select glass-input" v-model="availabilityForm.start_time" required>
                    <option value="" disabled selected>Start time...</option>
                    <option v-for="time in timeOptions" :key="'start'+time" :value="time">{{ time }}</option>
                  </select>
                </div>
                <div class="col-6">
                  <label class="form-label text-light small">End Time</label>
                  <select class="form-select glass-input" v-model="availabilityForm.end_time" required>
                    <option value="" disabled selected>End time...</option>
                    <option v-for="time in timeOptions" :key="'end'+time" :value="time">{{ time }}</option>
                  </select>
                </div>
              </div>

              <button type="submit" class="btn btn-neon w-100 rounded-pill" :disabled="!availabilityForm.date" style="color: var(--neon-mint); border-color: var(--neon-mint);">
                ADD TIME SLOT
              </button>
            </form>
          </div>
        </div>
      </div>
    </div>

    <div class="modal fade" id="treatmentModal" tabindex="-1" aria-hidden="true">
      <div class="modal-dialog modal-dialog-centered modal-lg">
        <div class="modal-content glass-card rounded-4 border-0">
          <div class="modal-header border-secondary">
            <h5 class="modal-title" style="color: var(--neon-mint);">Consultation & Notes</h5>
            <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal" id="closeTreatmentModal"></button>
          </div>
          <div class="modal-body p-4">
            <form @submit.prevent="submitTreatment">
              <div class="row mb-3">
                <div class="col-md-6">
                  <label class="form-label text-light small">Visit Type</label>
                  <select class="form-select glass-input" v-model="treatmentForm.visit_type">
                    <option value="In-person">In-person</option>
                    <option value="Online">Online / Telehealth</option>
                  </select>
                </div>
                <div class="col-md-6">
                  <label class="form-label text-light small">Tests Done (Optional)</label>
                  <input type="text" class="form-control glass-input" v-model="treatmentForm.tests_done" placeholder="e.g., Blood Pressure">
                </div>
              </div>
              <div class="mb-3">
                <label class="form-label text-light small">Primary Diagnosis</label>
                <textarea class="form-control glass-input" v-model="treatmentForm.diagnosis" rows="2" required placeholder="Enter diagnosis"></textarea>
              </div>
              <div class="mb-3">
                <label class="form-label text-light small">Prescription</label>
                <textarea class="form-control glass-input" v-model="treatmentForm.prescription" rows="2" required placeholder="Medication and dosage"></textarea>
              </div>
              <div class="mb-4">
                <label class="form-label text-light small">Additional Notes</label>
                <textarea class="form-control glass-input" v-model="treatmentForm.notes" rows="2" placeholder="Dietary restrictions, rest advised, etc."></textarea>
              </div>
              <button type="submit" class="btn btn-neon w-100 rounded-pill" style="color: var(--neon-mint); border-color: var(--neon-mint);">
                SUBMIT & MARK COMPLETED
              </button>
            </form>
          </div>
        </div>
      </div>
    </div>

    <div class="modal fade" id="patientHistoryModal" tabindex="-1" aria-hidden="true">
      <div class="modal-dialog modal-dialog-centered modal-lg">
        <div class="modal-content glass-card rounded-4 border-0">
          <div class="modal-header border-secondary">
            <h5 class="modal-title" style="color: var(--neon-cyan);">
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
                    <th class="text-light">Diagnosis</th>
                    <th class="text-light">Prescription</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="record in patientHistoryData" :key="record.id">
                    <td>{{ record.date }}</td>
                    <td class="fw-bold">{{ record.doctor_name }}</td>
                    <td>{{ record.diagnosis }}</td>
                    <td>{{ record.prescription }}</td>
                  </tr>
                  <tr v-if="patientHistoryData.length === 0">
                    <td colspan="4" class="text-center text-light py-4">No past records found for this patient.</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { apiConfig } from '../config'

const router = useRouter()

const dashboardData = ref({ doctor_name: '', department: '', appointments: [], patients: [] })

const availabilityForm = ref({ date: '', start_time: '', end_time: '' })
const treatmentForm = ref({ diagnosis: '', prescription: '', notes: '', visit_type: 'In-person', tests_done: '' })
const selectedApptId = ref(null)

const patientHistoryData = ref([])
const activePatientName = ref('')

const fetchDashboardData = async () => {
  const token = localStorage.getItem('access_token')
  if (!token) { router.push('/'); return; }

  try {
    const response = await fetch(apiConfig.doctorDashboard, {
      headers: { 'Authorization': `Bearer ${token}` }
    })
    if (response.ok) {
      dashboardData.value = await response.json()
    } else if (response.status === 401 || response.status === 403) handleLogout()
  } catch (error) { console.error("Fetch error:", error) }
}

onMounted(() => {
  fetchDashboardData()
})

const next7Days = ref([])

const generateNext7Days = () => {
  const days = []
  const today = new Date()
  
  for (let i = 0; i < 7; i++) {
    const nextDate = new Date(today)
    nextDate.setDate(today.getDate() + i)
    
    const yyyy = nextDate.getFullYear()
    const mm = String(nextDate.getMonth() + 1).padStart(2, '0')
    const dd = String(nextDate.getDate()).padStart(2, '0')
    const fullDate = `${yyyy}-${mm}-${dd}`
    
    const shortDay = nextDate.toLocaleDateString('en-US', { weekday: 'short' })
    const shortDateStr = nextDate.toLocaleDateString('en-US', { month: 'short', day: 'numeric' })
    
    days.push({
      fullDate: fullDate,
      display: `${shortDay} (${shortDateStr})`
    })
  }
  next7Days.value = days
}

generateNext7Days()

const timeOptions = ref([])
for (let h = 6; h <= 22; h++) {
  let hour = h < 10 ? `0${h}` : `${h}`
  timeOptions.value.push(`${hour}:00`)
  timeOptions.value.push(`${hour}:30`)
}

const setShift = (start, end) => {
  availabilityForm.value.start_time = start
  availabilityForm.value.end_time = end
}


const submitAvailability = async () => {
  const token = localStorage.getItem('access_token')
  try {
    const res = await fetch(apiConfig.addAvailability, {
      method: 'POST',
      headers: { 'Authorization': `Bearer ${token}`, 'Content-Type': 'application/json' },
      body: JSON.stringify(availabilityForm.value)
    })
    const data = await res.json()
    if (res.ok) {
      alert("System Notice: " + data.message)
      document.getElementById('closeAvailabilityModal').click()
      availabilityForm.value = { day: '', start_time: '', end_time: '' }
    } else alert("Error: " + data.error)
  } catch (err) { console.error(err) }
}

const cancelAppointment = async (apptId) => {
  if (!confirm("Are you sure you want to cancel this appointment?")) return;
  const token = localStorage.getItem('access_token')
  try {
    const res = await fetch(apiConfig.cancelAppointment(apptId), {
      method: 'PUT',
      headers: { 'Authorization': `Bearer ${token}` }
    })
    if (res.ok) fetchDashboardData()
    else alert("Error cancelling appointment.")
  } catch (err) { console.error(err) }
}

const openTreatmentModal = (apptId) => {
  selectedApptId.value = apptId
  treatmentForm.value = { diagnosis: '', prescription: '', notes: '', visit_type: 'In-person', tests_done: '' }
}

const submitTreatment = async () => {
  const token = localStorage.getItem('access_token')
  if (!selectedApptId.value) return

  try {
    const res = await fetch(apiConfig.addTreatment(selectedApptId.value), {
      method: 'POST',
      headers: { 'Authorization': `Bearer ${token}`, 'Content-Type': 'application/json' },
      body: JSON.stringify(treatmentForm.value)
    })
    const data = await res.json()
    if (res.ok) {
      alert("System Notice: " + data.message)
      document.getElementById('closeTreatmentModal').click()
      fetchDashboardData()
    } else alert("Error: " + data.error)
  } catch (err) { console.error(err) }
}

const viewPatientHistory = async (patientId) => {
  patientHistoryData.value = []
  activePatientName.value = 'Loading...'
  const token = localStorage.getItem('access_token')
  try {
    const res = await fetch(apiConfig.doctorPatientHistory(patientId), {
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
.glass-input::placeholder { color: #e0e0e0 !important; opacity: 1 !important; }
</style>