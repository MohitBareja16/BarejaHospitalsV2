<template>
  <div class="row justify-content-center align-items-center" style="min-height: 80vh;">
    <div class="col-md-5 col-lg-4">
      <div class="card glass-card rounded-4 p-4 mt-5">
        <div class="text-center mb-4">
          <h2 class="fw-bold" style="color: var(--neon-cyan);">BarejaHospitals</h2>
          <p class="text-light">Secure Access Portal</p>
        </div>

        <form @submit.prevent="handleLogin">
          <div class="mb-3">
            <label class="form-label text-light">Username</label>
            <input type="text" class="form-control glass-input" v-model="username" required placeholder="Enter username">
          </div>
          
          <div class="mb-4">
            <label class="form-label text-light">Password</label>
            <input type="password" class="form-control glass-input" v-model="password" required placeholder="••••••••">
          </div>

          <button type="submit" class="btn btn-neon w-100 fw-bold py-2 rounded-pill mb-3" style="color: var(--neon-mint); border-color: var(--neon-mint);">
            LOGIN HERE
          </button>
        </form>

        <div class="text-center mt-3 border-top border-secondary pt-3">
          <small class="text-light">
            New Patient? 
            <router-link to="/register" class="text-decoration-none" style="color: var(--neon-mint);">
              Register Here
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

const username = ref('')
const password = ref('')
const router = useRouter()

const handleLogin = async () => {
  try {
    const response = await fetch(apiConfig.login, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ 
        username: username.value, 
        password: password.value 
      })
    })

    const data = await response.json()

    if (response.ok) {
      localStorage.setItem('access_token', data.access_token)
      localStorage.setItem('user_role', data.role)
      localStorage.setItem('username', data.username)

      if (data.role === 'admin') router.push('/admin')
      else if (data.role === 'doctor') router.push('/doctor')
      else router.push('/patient')
      
    } else {
      alert("System Alert: " + (data.error || "Authentication Failed"))
    }
  } catch (error) {
    console.error("API connection error:", error)
    alert("CRITICAL: Cannot connect to backend servers.")
  }
}
</script>

<style>
.btn-neon:hover {
  background: var(--neon-mint) !important;
  color: #000 !important;
  box-shadow: 0 0 15px var(--neon-mint) !important;
}
</style>