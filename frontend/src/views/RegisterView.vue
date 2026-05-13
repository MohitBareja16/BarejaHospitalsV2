<template>
  <div class="row justify-content-center align-items-center" style="min-height: 80vh;">
    <div class="col-md-6 col-lg-5">
      <div class="card glass-card rounded-4 p-4 mt-5">
        <div class="text-center mb-4">
          <h2 class="fw-bold" style="color: var(--neon-mint);">BarejaHospitals</h2>
          <p class="text-light">Patient Registration Portal</p>
        </div>

        <form @submit.prevent="handleRegister">
          <h6 class="text-light border-bottom border-secondary pb-2 mb-3">Account Details</h6>
          <div class="row mb-3">
            <div class="col-6">
              <label class="form-label text-light small">Username</label>
              <input type="text" class="form-control glass-input" v-model="formData.username" required placeholder="Login ID">
            </div>
            <div class="col-6">
              <label class="form-label text-light small">Password</label>
              <input type="password" class="form-control glass-input" v-model="formData.password" required placeholder="••••••••">
            </div>
          </div>

          <h6 class="text-light border-bottom border-secondary pb-2 mb-3 mt-4">Personal Information</h6>
          <div class="mb-3">
            <label class="form-label text-light small">Full Name</label>
            <input type="text" class="form-control glass-input" v-model="formData.full_name" required placeholder="e.g., John Doe">
          </div>

          <div class="mb-3">
            <label class="form-label text-light small">Email Address</label>
            <input type="text" class="form-control glass-input" v-model="formData.email" required placeholder="">
          </div>
          
          <div class="row mb-4">
            <div class="col-4">
              <label class="form-label text-light small">Age</label>
              <input type="number" class="form-control glass-input" v-model="formData.age" required placeholder="e.g., 25">
            </div>
            <div class="col-8">
              <label class="form-label text-light small">Contact Number</label>
              <input type="tel" class="form-control glass-input" v-model="formData.phone" required placeholder="e.g., 9876543210">
            </div>
          </div>

          <button type="submit" class="btn btn-neon w-100 fw-bold py-2 rounded-pill mb-3" style="color: var(--neon-mint); border-color: var(--neon-mint);">
            REGISTER AS PATIENT
          </button>
        </form>

        <div class="text-center mt-3 border-top border-secondary pt-3">
          <small class="text-light">
            Already have an account? 
            <router-link to="/" class="text-decoration-none" style="color: var(--neon-cyan);">
              Login Here
            </router-link>
          </small>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { apiConfig } from '../config'

const router = useRouter()

const formData = ref({
  username: '',
  password: '',
  full_name: '',
  age: '',
  phone: ''
})

const handleRegister = async () => {
  try {
    const response = await fetch(apiConfig.register, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(formData.value)
    })

    const data = await response.json()

    if (response.ok) {
      alert("System Notice: " + data.message)
      router.push('/')
    } else {
      alert("Registration Error: " + (data.error || "Failed to create account"))
    }
  } catch (error) {
    console.error("API connection error:", error)
    alert("CRITICAL: Cannot connect to backend servers.")
  }
}
</script>

<style scoped>
.btn-neon:hover {
  background: var(--neon-mint) !important;
  color: #000 !important;
  box-shadow: 0 0 15px var(--neon-mint) !important;
}
</style>