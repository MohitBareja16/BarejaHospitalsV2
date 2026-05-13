// API Configuration
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:5000'

export const apiConfig = {
  baseURL: API_BASE_URL,
  
  // Auth endpoints
  login: `${API_BASE_URL}/api/login`,
  register: `${API_BASE_URL}/api/register`,
  
  // Public endpoints
  departments: `${API_BASE_URL}/api/departments`,
  doctors: `${API_BASE_URL}/api/doctors`,
  
  // Admin endpoints
  adminDashboard: `${API_BASE_URL}/api/admin/dashboard`,
  addDepartment: `${API_BASE_URL}/api/department`,
  addDoctor: `${API_BASE_URL}/api/admin/add_doctor`,
  manageDoctors: (id) => `${API_BASE_URL}/api/admin/doctor/${id}`,
  managePatients: (id) => `${API_BASE_URL}/api/admin/patient/${id}`,
  patientHistory: (id) => `${API_BASE_URL}/api/admin/patient/${id}/history`,
  toggleBlacklist: (id) => `${API_BASE_URL}/api/admin/toggle_blacklist/${id}`,
  
  // Doctor endpoints
  doctorDashboard: `${API_BASE_URL}/api/doctor/dashboard`,
  addAvailability: `${API_BASE_URL}/api/doctor/availability`,
  addTreatment: (id) => `${API_BASE_URL}/api/doctor/treatment/${id}`,
  cancelAppointment: (id) => `${API_BASE_URL}/api/doctor/appointment/${id}/cancel`,
  doctorPatientHistory: (id) => `${API_BASE_URL}/api/doctor/patient/${id}/history`,
  
  // Patient endpoints
  patientDashboard: `${API_BASE_URL}/api/patient/dashboard`,
  patientProfile: `${API_BASE_URL}/api/patient/profile`,
  patientPayment: `${API_BASE_URL}/api/patient/payment`,
  patientHistory: `${API_BASE_URL}/api/patient/history`,
  patientExportHistory: `${API_BASE_URL}/api/patient/export_history`,
  patientDownloadCSV: `${API_BASE_URL}/api/patient/download_csv`,
  searchDoctors: `${API_BASE_URL}/api/patient/search_doctors`,
  getDoctorSlots: (id) => `${API_BASE_URL}/api/doctor/${id}/slots`,
  bookAppointment: `${API_BASE_URL}/api/patient/book`,
  cancelAppointmentPatient: (id) => `${API_BASE_URL}/api/patient/appointment/${id}/cancel`,
  exportMedicalHistory: `${API_BASE_URL}/api/patient/export_medical_history`
}

export default apiConfig
