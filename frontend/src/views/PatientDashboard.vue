<template>
  <div class="container mt-4 mb-5">
    <div class="d-flex justify-content-between align-items-center mb-4 border-bottom border-secondary pb-3">
      <div>
        <h2 class="text-light fw-bold m-0" style="text-shadow: 0 0 10px rgba(0, 243, 255, 0.3);">
          Welcome, <span style="color: var(--neon-cyan);">{{ dashboardData.patient_name || 'Patient' }}</span>
        </h2>
      </div>
      <div>
        <button @click="openProfileModal" class="btn btn-outline-info rounded-pill px-3 me-2" data-bs-toggle="modal" data-bs-target="#profileModal">
          <i class="bi bi-person"></i> Edit Profile
        </button>
        <button @click="handleLogout" class="btn btn-outline-danger rounded-pill px-4">Logout</button>
      </div>
    </div>

    <div class="row">
      <div class="col-lg-7 mb-4">
        <div class="card glass-card rounded-4 p-4 h-100">
          <div class="d-flex justify-content-between align-items-center mb-4 bg-dark p-3 rounded-3 shadow-sm" style="border: 1px solid rgba(255,255,255,0.1);">
            <h4 class="text-white fw-bold m-0">My Appointments</h4>
            <button @click="fetchHistory" class="btn btn-outline-light btn-sm rounded-pill" data-bs-toggle="modal" data-bs-target="#historyModal">
              View Medical History
            </button>
          </div>
          
          <div v-if="dashboardData.appointments.length === 0" class="text-center text-light py-4">
            No active appointments.
          </div>

          <div v-for="appt in dashboardData.appointments" :key="appt.id" class="mb-3">
            <div v-if="appt.status !== 'Completed'" class="card bg-transparent border-secondary rounded-4 p-3 border-start border-4" 
                 :class="appt.status === 'Cancelled' ? 'border-danger' : 'border-info'">
              <div class="d-flex justify-content-between align-items-center">
                <div>
                  <h5 class="text-light fw-bold m-0">Dr. {{ appt.doctor_name }}</h5>
                  <small class="text-light">{{ appt.department }} | <i class="bi bi-calendar-event"></i> {{ appt.date }} at {{ appt.time }}</small>
                </div>
                <div class="text-end">
                  <span class="badge rounded-pill mb-2 d-block" 
                        :class="appt.status === 'Cancelled' ? 'bg-danger' : 'bg-info text-dark'">
                    {{ appt.status }}
                  </span>
                  <button v-if="appt.status === 'Scheduled'" @click="cancelAppointment(appt.id)" class="btn btn-sm btn-outline-danger rounded-pill px-3">Cancel</button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="col-lg-5 mb-4">
        <div class="card glass-card rounded-4 p-4 h-100">
          <div class="d-flex justify-content-between align-items-center mb-4 bg-dark p-3 rounded-3 shadow-sm" style="border: 1px solid rgba(255,255,255,0.1);">
            <h4 class="text-white fw-bold m-0">Find a Doctor</h4>
          </div>
          
          <div class="mb-3">
            <label class="form-label text-light small">By Doctor Name</label>
            <input type="text" class="form-control glass-input mb-3" v-model="searchFilters.name" placeholder="e.g., John Heart">

            <label class="form-label text-light small">By Specialization</label>
            <select class="form-select glass-input mb-3" v-model="searchFilters.department">
              <option value="">Any Department</option>
              <option v-for="dept in dashboardData.departments" :key="dept.id" :value="dept.name">{{ dept.name }}</option>
            </select>
            
            <label class="form-label text-light small">By Availability Date</label>
            <input type="date" class="form-control glass-input mb-3" v-model="searchFilters.date" :min="minDate">
            
            <button @click="searchDoctors" class="btn btn-neon w-100 rounded-pill" style="color: var(--neon-mint); border-color: var(--neon-mint);">
              <i class="bi bi-search"></i> SEARCH
            </button>
          </div>

          <div class="mt-4 border-top border-secondary pt-3">
            <h6 class="text-light mb-3">Search Results ({{ searchResults.length }})</h6>
            <div v-if="searchResults.length === 0" class="text-center text-light small">
              No results found. Adjust filters and search.
            </div>
            <div v-else class="list-group bg-transparent" style="max-height: 300px; overflow-y: auto;">
              <button v-for="doc in searchResults" :key="doc.id" 
                      @click="openDoctorDetails(doc)"
                      class="list-group-item list-group-item-action bg-dark text-light border-secondary mb-2 rounded-3 hover-neon"
                      data-bs-toggle="modal" data-bs-target="#doctorDetailsModal">
                <div class="d-flex justify-content-between align-items-center">
                  <div>
                    <strong class="d-block">Dr. {{ doc.name }}</strong>
                    <small class="text-info">{{ doc.department }}</small>
                  </div>
                  <i class="bi bi-arrow-right"></i>
                </div>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="modal fade" id="profileModal" tabindex="-1" aria-hidden="true">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content glass-card rounded-4 border-0">
          <div class="modal-header border-secondary">
            <h5 class="modal-title" style="color: var(--neon-cyan);">Update Personal Profile</h5>
            <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal" id="closeProfileModal"></button>
          </div>
          <div class="modal-body p-4">
            <form @submit.prevent="submitProfileUpdate">
              <div class="mb-3">
                <label class="form-label text-light small">Full Name</label>
                <input type="text" class="form-control glass-input" v-model="profileForm.full_name" required>
              </div>
              <div class="mb-3">
                <label class="form-label text-light small">Email Address</label>
                <input type="email" class="form-control glass-input" v-model="profileForm.email" required placeholder="patient@example.com">
              </div>
              <div class="row mb-4">
                <div class="col-4">
                  <label class="form-label text-light small">Age</label>
                  <input type="number" class="form-control glass-input" v-model="profileForm.age" required>
                </div>
                <div class="col-8">
                  <label class="form-label text-light small">Contact Number</label>
                  <input type="text" class="form-control glass-input" v-model="profileForm.phone" required>
                </div>
              </div>
              <button type="submit" class="btn btn-outline-info w-100 rounded-pill">SAVE PROFILE</button>
            </form>
          </div>
        </div>
      </div>
    </div>

    <div class="modal fade" id="historyModal" tabindex="-1" aria-hidden="true">
      <div class="modal-dialog modal-dialog-centered modal-xl">
        <div class="modal-content glass-card rounded-4 border-0">
          <div class="modal-header border-secondary">
            <h5 class="modal-title" style="color: var(--neon-mint);">My Medical History</h5>
            <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
          </div>
          <div class="modal-body p-4">
            <div class="table-responsive">
              <table class="table table-dark table-hover table-borderless align-middle custom-table">
                <thead style="border-bottom: 1px solid var(--glass-border);">
                  <tr>
                    <th class="text-light">Date</th>
                    <th class="text-light">Doctor</th>
                    <th class="text-light">Visit Type</th>
                    <th class="text-light">Diagnosis</th>
                    <th class="text-light">Prescription & Notes</th>
                    <th class="text-light text-end">Billing</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="record in medicalHistory" :key="record.id">
                    <td>{{ record.date }}</td>
                    <td class="fw-bold">Dr. {{ record.doctor_name }} <br><small class="text-light">{{ record.department }}</small></td>
                    <td><span class="badge bg-secondary rounded-pill">{{ record.visit_type }}</span></td>
                    <td>{{ record.diagnosis }}</td>
                    <td>
                      <span class="d-block text-info">{{ record.prescription }}</span>
                      <small class="text-light">{{ record.notes }}</small>
                    </td>
                    <td class="text-end">
                      <button @click="openPaymentModal(record)" class="btn btn-sm rounded-pill px-3 text-dark fw-bold" style="background-color: var(--neon-mint);" data-bs-toggle="modal" data-bs-target="#paymentModal">
                        <i class="bi bi-credit-card"></i> Pay ₹{{ record.fees }}
                      </button>
                    </td>
                  </tr>
                  <tr v-if="medicalHistory.length === 0">
                    <td colspan="5" class="text-center text-light py-4">No completed consultation records found.</td>
                  </tr>
                </tbody>
              </table>
            </div>
            <div class="d-flex gap-2">
                <button @click="triggerExport" class="btn btn-outline-info rounded-pill">
                  <i class="bi bi-envelope-paper"></i> 1. Request Export
                </button>
                
                <button @click="downloadCSV" class="btn btn-outline-info rounded-pill">
                  <i class="bi bi-download"></i> 2. Download File
                </button>
              </div>
          </div>
        </div>
      </div>
    </div>

    <div class="modal fade" id="departmentModal" tabindex="-1" aria-hidden="true">
      <div class="modal-dialog modal-dialog-centered modal-lg">
        <div class="modal-content glass-card rounded-4 border-0">
          <div class="modal-header border-secondary">
            <h5 class="modal-title" style="color: var(--neon-cyan);">{{ activeDepartment.name }} Specialists</h5>
            <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal" id="closeDeptModal"></button>
          </div>
          <div class="modal-body p-4">
            <div v-if="departmentDoctors.length === 0" class="text-center text-light py-4">
              No specialists currently assigned to this department.
            </div>
            <div class="row g-3">
              <div v-for="doc in departmentDoctors" :key="doc.id" class="col-md-6">
                <div class="card bg-dark border-secondary rounded-4 p-3 h-100">
                  <h5 class="text-white fw-bold mb-1">Dr. {{ doc.name }}</h5>
                  <p class="text-info small mb-2">{{ doc.qualification || 'Senior Consultant' }}</p>
                  <p class="text-light small mb-3">Expert in {{ activeDepartment.name }} diagnostics and treatments. Committed to providing excellent patient care.</p>
                  <div class="mt-auto text-end">
                    <button @click="openDoctorDetails(doc)" class="btn btn-neon btn-sm rounded-pill px-4" data-bs-toggle="modal" data-bs-target="#doctorDetailsModal" style="color: var(--neon-mint); border-color: var(--neon-mint);">
                      View Availability & Book
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="modal fade" id="doctorDetailsModal" tabindex="-1" aria-hidden="true">
      <div class="modal-dialog modal-dialog-centered modal-lg">
        <div class="modal-content glass-card rounded-4 border-0">
          <div class="modal-header border-secondary">
            <h5 class="modal-title text-white">Book Appointment</h5>
            <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal" id="closeBookingModal"></button>
          </div>
          <div class="modal-body p-4">
            
            <div class="d-flex align-items-center mb-4 bg-dark p-3 rounded-4 shadow-sm border border-secondary">
              <div class="me-4">
                <div class="bg-secondary rounded-circle d-flex justify-content-center align-items-center" style="width: 70px; height: 70px;">
                  <i class="bi bi-person-fill text-dark fs-1"></i>
                </div>
              </div>
              <div>
                <h4 class="text-light fw-bold m-0">Dr. {{ selectedDoctor.name }}</h4>
                <p class="text-light mb-1">{{ activeDepartment.name }} | {{ selectedDoctor.qualification || 'Consultant' }}</p>
                <span class="badge bg-info text-dark rounded-pill">Consultation Fee: ₹{{ selectedDoctor.fees || '500' }}</span>
              </div>
            </div>

            <h6 class="text-light border-bottom border-secondary pb-2 mb-3">Available Slots (Next 7 Days)</h6>
            <div v-if="availableSlots.length > 0" class="row g-2">
              <div v-for="slot in availableSlots" :key="slot.date + slot.time" class="col-md-4">
                <button @click="confirmBooking(slot)" class="btn btn-outline-info w-100 rounded-3 text-start p-2 hover-neon">
                  <small class="d-block fw-bold">{{ slot.day_name }}, {{ slot.date }}</small>
                  <span style="color: var(--neon-mint);">{{ slot.display_time }}</span>
                </button>
              </div>
            </div>
            <div v-else class="text-center text-light p-4 bg-dark rounded-4">
              No available slots found for this doctor in the next 7 days.
            </div>

          </div>
        </div>
      </div>
    </div>

  </div>
  <div class="modal fade" id="paymentModal" tabindex="-1" aria-hidden="true">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content glass-card rounded-4 border-0">
          <div class="modal-header border-secondary">
            <h5 class="modal-title" style="color: var(--neon-cyan);">Secure Checkout</h5>
            <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal" id="closePaymentModal"></button>
          </div>
          <div class="modal-body p-4">
            
            <div class="alert bg-dark text-light border-secondary mb-4 rounded-3 d-flex justify-content-between">
              <span>Consultation Fee: Dr. {{ activePaymentDoc }}</span>
              <strong style="color: var(--neon-mint);">₹{{ activePaymentFee }}.00</strong>
            </div>

            <form @submit.prevent="processPayment">
              <div class="mb-3">
                <label class="form-label text-light small">Cardholder Name</label>
                <input type="text" class="form-control glass-input" v-model="paymentForm.name" required placeholder="Name on card">
              </div>
              
              <div class="mb-3">
                <label class="form-label text-light small">Card Number</label>
                <div class="input-group">
                  <span class="input-group-text glass-input text-light"><i class="bi bi-credit-card"></i></span>
                  <input type="text" class="form-control glass-input" v-model="paymentForm.card_number" required placeholder="0000 0000 0000 0000" maxlength="19">
                </div>
              </div>
              
              <div class="row mb-4">
                <div class="col-6">
                  <label class="form-label text-light small">Expiry Date</label>
                  <input type="text" class="form-control glass-input" v-model="paymentForm.expiry" required placeholder="MM/YY" maxlength="5">
                </div>
                <div class="col-6">
                  <label class="form-label text-light small">CVV</label>
                  <input type="password" class="form-control glass-input" v-model="paymentForm.cvv" required placeholder="123" maxlength="3">
                </div>
              </div>
              
              <button type="submit" class="btn w-100 rounded-pill fw-bold" style="background: var(--neon-cyan); color: #000;" :disabled="isProcessing">
                <span v-if="isProcessing" class="spinner-border spinner-border-sm me-2"></span>
                {{ isProcessing ? 'Processing...' : `PAY ₹${activePaymentFee}.00` }}
              </button>
            </form>

            <div class="text-center mt-3">
              <small class="text-light"><i class="bi bi-shield-lock"></i> Payments are secured by mock 256-bit encryption.</small>
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

const dashboardData = ref({ patient_name: '', appointments: [], departments: [] })

const profileForm = ref({ full_name: '', email: '', age: '', phone: '' })

const medicalHistory = ref([])

const activeDepartment = ref({})
const departmentDoctors = ref([])
const selectedDoctor = ref({})
const availableSlots = ref([])

const searchFilters = ref({ department: '', date: '', name: '' })
const searchResults = ref([])

const today = new Date()
const minDate = ref(today.toISOString().split('T')[0])

const activePaymentDoc = ref('')
const activePaymentFee = ref(0)
const paymentForm = ref({ name: '', card_number: '', expiry: '', cvv: '' })
const isProcessing = ref(false)

const fetchDashboardData = async () => {
  const token = localStorage.getItem('access_token')
  if (!token) { router.push('/'); return; }

  try {
    const response = await fetch(apiConfig.patientDashboard, {
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

const openProfileModal = async () => {
  const token = localStorage.getItem('access_token')
  try {
    const res = await fetch(apiConfig.patientProfile, {
      headers: { 'Authorization': `Bearer ${token}` }
    })
    if (res.ok) profileForm.value = await res.json()
  } catch (error) { console.error(error) }
}

const openPaymentModal = (record) => {
  activePaymentDoc.value = record.doctor_name
  activePaymentFee.value = record.fees || 0
  paymentForm.value = { name: '', card_number: '', expiry: '', cvv: '' }
  document.querySelector('#historyModal .btn-close').click()
}

const processPayment = async () => {
  isProcessing.value = true
  const token = localStorage.getItem('access_token')
  
  try {
    const res = await fetch(apiConfig.patientPayment, {
      method: 'POST',
      headers: { 'Authorization': `Bearer ${token}`, 'Content-Type': 'application/json' },
      body: JSON.stringify(paymentForm.value)
    })
    
    const data = await res.json()
    
    setTimeout(() => {
      isProcessing.value = false
      if (res.ok) {
        alert("✅ Transaction Approved: " + data.message)
        document.getElementById('closePaymentModal').click()
      } else {
        alert("❌ Payment Failed: " + data.error)
      }
    }, 1500)
    
  } catch (error) { 
    console.error(error)
    isProcessing.value = false
    alert("System Error connecting to payment gateway.")
  }
}

const submitProfileUpdate = async () => {
  const token = localStorage.getItem('access_token')
  try {
    const res = await fetch(apiConfig.patientProfile, {
      method: 'PUT',
      headers: { 'Authorization': `Bearer ${token}`, 'Content-Type': 'application/json' },
      body: JSON.stringify(profileForm.value)
    })
    const data = await res.json()
    if (res.ok) {
      alert("System Notice: " + data.message)
      document.getElementById('closeProfileModal').click()
      fetchDashboardData()
    } else alert("Error: " + data.error)
  } catch (error) { console.error(error) }
}

const fetchHistory = async () => {
  const token = localStorage.getItem('access_token')
  try {
    const res = await fetch(apiConfig.patientHistory, {
      headers: { 'Authorization': `Bearer ${token}` }
    })
    if (res.ok) medicalHistory.value = await res.json()
  } catch (error) { console.error(error) }
}

const triggerExport = async () => {
  const token = localStorage.getItem('access_token')
  try {
    const response = await fetch(apiConfig.patientExportHistory, {
      method: 'POST',
      headers: { 'Authorization': `Bearer ${token}`, 'Content-Type': 'application/json' }
    })
    const data = await response.json()
    if (response.ok) alert("System Notice: " + data.message)
    else alert("Error: " + data.error)
  } catch (error) { console.error("Export error:", error) }
}

const openDepartmentModal = async (dept) => {
  activeDepartment.value = dept
  departmentDoctors.value = []
  
  try {
    const res = await fetch(apiConfig.doctors)
    if (res.ok) {
      const allDocs = await res.json()
      departmentDoctors.value = allDocs.filter(d => d.department === dept.name)
    }
  } catch (error) { console.error(error) }
}

const searchDoctors = async () => {
  const token = localStorage.getItem('access_token')
  try {
    const res = await fetch(apiConfig.searchDoctors, {
      method: 'POST',
      headers: { 'Authorization': `Bearer ${token}`, 'Content-Type': 'application/json' },
      body: JSON.stringify(searchFilters.value)
    })
    if (res.ok) {
      searchResults.value = await res.json()
    }
  } catch (err) { console.error("Search error:", err) }
}

const openDoctorDetails = async (doc) => {
  document.getElementById('closeDeptModal').click()
  
  selectedDoctor.value = doc
  availableSlots.value = []
  
  const token = localStorage.getItem('access_token')
  try {
    const res = await fetch(apiConfig.getDoctorSlots(doc.id), {
      headers: { 'Authorization': `Bearer ${token}` }
    })
    if (res.ok) {
      const data = await res.json()
      availableSlots.value = data.slots
    }
  } catch (error) { console.error(error) }
}

const confirmBooking = async (slot) => {
  if(!confirm(`Book appointment with Dr. ${selectedDoctor.value.name} for ${slot.date} at ${slot.display_time}?`)) return;

  const token = localStorage.getItem('access_token')
  try {
    const response = await fetch(apiConfig.bookAppointment, {
      method: 'POST',
      headers: { 'Authorization': `Bearer ${token}`, 'Content-Type': 'application/json' },
      body: JSON.stringify({
        doctor_id: selectedDoctor.value.id,
        date: slot.date,
        time: slot.time
      })
    })

    const data = await response.json()
    if (response.ok) {
      alert("System Notice: " + data.message)
      document.getElementById('closeBookingModal').click() 
      fetchDashboardData()
    } else {
      alert("Booking Error: " + data.error)
    }
  } catch (error) { console.error(error) }
}

const cancelAppointment = async (apptId) => {
  if(!confirm("Are you sure you want to cancel this appointment?")) return;
  
  const token = localStorage.getItem('access_token')
  try {
    const res = await fetch(apiConfig.bookAppointment.replace('/book', `/appointment/${apptId}/cancel`), {
      method: 'PUT',
      headers: { 'Authorization': `Bearer ${token}` }
    })
    
    const data = await res.json()
    if (res.ok) {
      alert("System Notice: " + data.message)
      fetchDashboardData()
    } else {
      alert("Error: " + data.error)
    }
  } catch (err) { 
    console.error("Cancellation error:", err) 
  }
}

const downloadCSV = async () => {
  const token = localStorage.getItem('access_token')
  try {
    const res = await fetch(apiConfig.patientDownloadCSV, {
      headers: { 'Authorization': `Bearer ${token}` }
    })
    
    if (res.ok) {
      const blob = await res.blob()
      
      const url = window.URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = `medical_history.csv`
      document.body.appendChild(a)
      a.click()
    
      a.remove()
      window.URL.revokeObjectURL(url)
    } else {
      const data = await res.json()
      alert(data.error || "Failed to download CSV.")
    }
  } catch (err) {
    console.error("Download Error:", err)
  }
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

.hover-neon:hover {
  background: rgba(0, 243, 255, 0.1);
  border-color: var(--neon-cyan) !important;
  color: #fff !important;
}
.glass-input::placeholder {
  color: #ffffff;
  opacity: 0.5;
}
</style>