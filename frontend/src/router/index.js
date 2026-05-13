import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: () => import('../views/HomeView.vue')
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('../views/LoginView.vue')
    },
    {
      path: '/register',
      name: 'register',
      component: () => import('../views/RegisterView.vue')
    },
    {
      path: '/admin',
      name: 'admin-dashboard',
      component: () => import('../views/AdminDashboard.vue')
    },
    {
      path: '/doctor',
      name: 'doctor-dashboard',
      component: () => import('../views/DoctorDashboard.vue')
    },
    {
      path: '/patient',
      name: 'patient-dashboard',
      component: () => import('../views/PatientDashboard.vue')
    }
  ]
})

export default router