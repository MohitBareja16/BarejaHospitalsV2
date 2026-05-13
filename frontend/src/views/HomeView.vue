<template>
  <div class="home-wrapper">

    <!-- Animated background particles -->
    <canvas ref="particleCanvas" class="particle-canvas"></canvas>

    <!-- Navbar -->
    <nav class="home-nav">
      <div class="nav-inner">
        <div class="nav-brand">
          <span class="brand-icon">✦</span>
          <span class="brand-name">BarejaHospitals</span>
        </div>
        <div class="nav-links">
          <a href="#features" class="nav-link" @click.prevent="smoothScroll('features')">Services</a>
          <a href="#stats" class="nav-link" @click.prevent="smoothScroll('stats')">About</a>
          <a href="#departments" class="nav-link" @click.prevent="smoothScroll('departments')">Departments</a>
        </div>
        <div class="nav-actions">
          <router-link to="/login" class="btn-ghost">Sign In</router-link>
          <router-link to="/register" class="btn-neon-home">Get Started</router-link>
        </div>
      </div>
    </nav>

    <!-- HERO SECTION -->
    <section class="hero-section">
      <div class="hero-grid-overlay"></div>

      <div class="hero-content">
        <div class="hero-badge" ref="heroBadge">
          <span class="pulse-dot"></span>
          <span>Now accepting new patients</span>
        </div>

        <h1 class="hero-title" ref="heroTitle">
            <span class="line">Welcome To</span>
            <span class="line line-2">Bareja Hospitals</span>
        </h1>

        <p class="hero-subtitle" ref="heroSubtitle">
          World-class care, seamlessly managed. Book appointments, access records,
          and connect with top specialists — all in one secure portal.
        </p>

        <div class="hero-ctas" ref="heroCtas">
          <router-link to="/register" class="cta-primary">
            <span>Book Appointment</span>
            <svg width="16" height="16" viewBox="0 0 16 16" fill="none"><path d="M3 8h10M9 4l4 4-4 4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>
          </router-link>
          <a href="#features" class="cta-secondary" @click.prevent="smoothScroll('features')">
            <span class="play-icon">▶</span>
            <span>How it works</span>
          </a>
        </div>

        <div class="hero-trust" ref="heroTrust">
          <div class="trust-item">
            <span class="trust-num" data-target="15000">0</span>
            <span class="trust-label">Patients Served</span>
          </div>
          <div class="trust-divider"></div>
          <div class="trust-item">
            <span class="trust-num" data-target="120">0</span>
            <span class="trust-label">Specialists</span>
          </div>
          <div class="trust-divider"></div>
          <div class="trust-item">
            <span class="trust-num" data-target="24">0</span>
            <span class="trust-label">Departments</span>
          </div>
        </div>
      </div>

      <!-- Floating cards -->
      <div class="hero-floating-cards">
        <div class="float-card card-1 glass-card-home">
          <div class="fc-icon fc-cyan">🩺</div>
          <div>
            <div class="fc-label">Next Available</div>
            <div class="fc-value">Dr. Sharma</div>
            <div class="fc-sub">Cardiology · Today 3PM</div>
          </div>
        </div>
        <div class="float-card card-2 glass-card-home">
          <div class="fc-icon fc-mint">✓</div>
          <div>
            <div class="fc-label">Appointment Confirmed</div>
            <div class="fc-value">Dr. Mehta</div>
            <div class="fc-sub">Neurology · Tomorrow</div>
          </div>
        </div>
        <div class="float-card card-3 glass-card-home">
          <div class="fc-row">
            <div class="fc-icon fc-cyan">📋</div>
            <div>
              <div class="fc-label">Records Updated</div>
              <div class="fc-sub">2 new prescriptions</div>
            </div>
          </div>
        </div>
      </div>

      <div class="scroll-hint">
        <span>Scroll</span>
        <div class="scroll-line"></div>
      </div>
    </section>

    <!-- FEATURES SECTION -->
    <section id="features" class="features-section">
      <div class="section-header">
        <span class="section-tag">Why BarejaHospitals</span>
        <h2 class="section-title">Everything you need,<br>nothing you don't.</h2>
      </div>

      <div class="features-grid">
        <div
          v-for="(feat, i) in features"
          :key="feat.title"
          class="feature-card glass-card-home"
          :style="{ animationDelay: i * 0.1 + 's' }"
          @mouseenter="featHover = i"
          @mouseleave="featHover = -1"
          :class="{ 'feat-active': featHover === i }"
        >
          <div class="feat-icon-wrap" :class="feat.color">
            <span class="feat-icon">{{ feat.icon }}</span>
          </div>
          <h3 class="feat-title">{{ feat.title }}</h3>
          <p class="feat-desc">{{ feat.desc }}</p>
          <div class="feat-arrow">→</div>
        </div>
      </div>
    </section>

    <!-- STATS SECTION -->
    <section id="stats" class="stats-section">
      <div class="stats-bg-glow"></div>
      <div class="stats-inner">
        <div class="stats-text">
          <span class="section-tag">Our Impact</span>
          <h2 class="section-title">Trusted by patients<br>across the region.</h2>
          <p class="stats-body">
            BarejaHospitals has been at the forefront of modern healthcare for over two decades.
            Our digital-first approach makes world-class care more accessible than ever.
          </p>
          <router-link to="/register" class="cta-primary" style="display:inline-flex; margin-top: 2rem;">
            <span>Join Our Network</span>
            <svg width="16" height="16" viewBox="0 0 16 16" fill="none"><path d="M3 8h10M9 4l4 4-4 4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>
          </router-link>
        </div>
        <div class="stats-cards">
          <div v-for="stat in stats" :key="stat.label" class="stat-card glass-card-home">
            <div class="stat-num" :style="{ color: stat.color }">{{ stat.val }}</div>
            <div class="stat-label">{{ stat.label }}</div>
            <div class="stat-bar">
              <div class="stat-bar-fill" :style="{ width: stat.pct, background: stat.color }"></div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- DEPARTMENTS SECTION -->
    <section id="departments" class="dept-section">
      <div class="section-header">
        <span class="section-tag">Specializations</span>
        <h2 class="section-title">Our Departments</h2>
      </div>

      <div class="dept-grid">
        <div
          v-for="dept in departments"
          :key="dept.name"
          class="dept-card"
          @mouseenter="deptHover = dept.name"
          @mouseleave="deptHover = ''"
          :class="{ 'dept-hovered': deptHover === dept.name }"
        >
          <div class="dept-icon">{{ dept.icon }}</div>
          <div class="dept-name">{{ dept.name }}</div>
          <div class="dept-count">{{ dept.docs }} specialists</div>
          <div class="dept-glow" :style="{ background: dept.glow }"></div>
        </div>
      </div>
    </section>

    <!-- HOW IT WORKS -->
    <section class="steps-section">
      <div class="section-header">
        <span class="section-tag">Getting Started</span>
        <h2 class="section-title">Up and running<br>in 3 steps.</h2>
      </div>

      <div class="steps-track">
        <div class="steps-line"></div>
        <div v-for="(step, i) in steps" :key="step.title" class="step-item">
          <div class="step-num">{{ String(i+1).padStart(2,'0') }}</div>
          <div class="step-body glass-card-home">
            <span class="step-icon">{{ step.icon }}</span>
            <h4 class="step-title">{{ step.title }}</h4>
            <p class="step-desc">{{ step.desc }}</p>
          </div>
        </div>
      </div>
    </section>

    <!-- CTA BANNER -->
    <section class="cta-banner">
      <div class="cta-bg-glow"></div>
      <div class="cta-content">
        <h2 class="cta-title">Your health journey<br>starts here.</h2>
        <p class="cta-sub">Join thousands of patients who've made BarejaHospitals their healthcare home.</p>
        <div class="cta-btns">
          <router-link to="/register" class="cta-primary cta-large">Create Free Account</router-link>
          <router-link to="/login" class="cta-ghost">Sign In →</router-link>
        </div>
      </div>
    </section>

    <!-- FOOTER -->
    <footer class="home-footer">
      <div class="footer-inner">
        <div class="footer-brand">
          <span class="brand-icon">✦</span>
          <span class="brand-name">BarejaHospitals</span>
        </div>
        <p class="footer-copy">© 2025 BarejaHospitals. All rights reserved.</p>
        <div class="footer-links">
          <a href="#">Privacy</a>
          <a href="#">Terms</a>
          <a href="#">Contact</a>
        </div>
      </div>
    </footer>

  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const particleCanvas = ref(null)
const heroBadge = ref(null)
const heroTitle = ref(null)
const heroSubtitle = ref(null)
const heroCtas = ref(null)
const heroTrust = ref(null)
const featHover = ref(-1)
const deptHover = ref('')

const features = [
  { icon: '🗓', title: 'Smart Scheduling', desc: 'Book appointments in seconds. Real-time availability across all departments and specialists.', color: 'icon-cyan' },
  { icon: '📊', title: 'Medical Records', desc: 'Complete digital health history at your fingertips. Secure, exportable, and always up to date.', color: 'icon-mint' },
  { icon: '💬', title: 'Doctor Connect', desc: 'Search specialists by department, name, or availability. View profiles and book instantly.', color: 'icon-cyan' },
  { icon: '💳', title: 'Seamless Billing', desc: 'Transparent fee structures with integrated payment processing. No surprise charges.', color: 'icon-mint' },
  { icon: '🔒', title: 'Bank-Grade Security', desc: 'JWT-protected access, encrypted data, and role-based permissions keep your data safe.', color: 'icon-cyan' },
  { icon: '📱', title: 'Anywhere Access', desc: 'Fully responsive portal accessible from any device. Your health data wherever you are.', color: 'icon-mint' },
]

const stats = [
  { val: '98%', label: 'Patient Satisfaction', pct: '98%', color: 'var(--neon-cyan)' },
  { val: '< 24h', label: 'Avg. Appointment Wait', pct: '85%', color: 'var(--neon-mint)' },
  { val: '120+', label: 'Qualified Specialists', pct: '75%', color: 'var(--neon-cyan)' },
  { val: '15K+', label: 'Patients Served', pct: '90%', color: 'var(--neon-mint)' },
]

const departments = [
  { icon: '❤️', name: 'Cardiology', docs: 12, glow: 'radial-gradient(circle, rgba(255,80,80,0.3), transparent)' },
  { icon: '🧠', name: 'Neurology', docs: 8, glow: 'radial-gradient(circle, rgba(0,243,255,0.3), transparent)' },
  { icon: '🦴', name: 'Orthopedics', docs: 10, glow: 'radial-gradient(circle, rgba(255,200,0,0.3), transparent)' },
  { icon: '👁', name: 'Ophthalmology', docs: 6, glow: 'radial-gradient(circle, rgba(0,255,157,0.3), transparent)' },
  { icon: '🫁', name: 'Pulmonology', docs: 7, glow: 'radial-gradient(circle, rgba(100,100,255,0.3), transparent)' },
  { icon: '🦷', name: 'Dental', docs: 9, glow: 'radial-gradient(circle, rgba(255,150,0,0.3), transparent)' },
  { icon: '🧬', name: 'Oncology', docs: 5, glow: 'radial-gradient(circle, rgba(200,0,255,0.3), transparent)' },
  { icon: '🩻', name: 'Radiology', docs: 8, glow: 'radial-gradient(circle, rgba(0,200,255,0.3), transparent)' },
]

const steps = [
  { icon: '👤', title: 'Create Your Account', desc: 'Register in under a minute. Set up your patient profile with basic health information.' },
  { icon: '🔍', title: 'Find Your Specialist', desc: 'Search across 120+ specialists by department, availability, or name. See real-time slots.' },
  { icon: '✅', title: 'Book & Manage', desc: 'Confirm your appointment, receive reminders, and manage everything from your dashboard.' },
]

const smoothScroll = (id) => {
  document.getElementById(id)?.scrollIntoView({ behavior: 'smooth' })
}

// Particle animation
let animFrame = null
let particles = []

const initParticles = () => {
  const canvas = particleCanvas.value
  if (!canvas) return
  const ctx = canvas.getContext('2d')
  canvas.width = window.innerWidth
  canvas.height = window.innerHeight

  particles = Array.from({ length: 60 }, () => ({
    x: Math.random() * canvas.width,
    y: Math.random() * canvas.height,
    r: Math.random() * 1.5 + 0.3,
    vx: (Math.random() - 0.5) * 0.3,
    vy: (Math.random() - 0.5) * 0.3,
    alpha: Math.random() * 0.5 + 0.1,
    color: Math.random() > 0.5 ? '0,243,255' : '0,255,157'
  }))

  const draw = () => {
    ctx.clearRect(0, 0, canvas.width, canvas.height)
    particles.forEach(p => {
      p.x += p.vx
      p.y += p.vy
      if (p.x < 0) p.x = canvas.width
      if (p.x > canvas.width) p.x = 0
      if (p.y < 0) p.y = canvas.height
      if (p.y > canvas.height) p.y = 0
      ctx.beginPath()
      ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2)
      ctx.fillStyle = `rgba(${p.color},${p.alpha})`
      ctx.fill()
    })

    // Draw connecting lines
    for (let i = 0; i < particles.length; i++) {
      for (let j = i + 1; j < particles.length; j++) {
        const dx = particles[i].x - particles[j].x
        const dy = particles[i].y - particles[j].y
        const dist = Math.sqrt(dx*dx + dy*dy)
        if (dist < 120) {
          ctx.beginPath()
          ctx.moveTo(particles[i].x, particles[i].y)
          ctx.lineTo(particles[j].x, particles[j].y)
          ctx.strokeStyle = `rgba(0,243,255,${0.05 * (1 - dist/120)})`
          ctx.lineWidth = 0.5
          ctx.stroke()
        }
      }
    }
    animFrame = requestAnimationFrame(draw)
  }
  draw()
}

// Counter animation
const animateCounters = () => {
  document.querySelectorAll('.trust-num[data-target]').forEach(el => {
    const target = parseInt(el.dataset.target)
    let current = 0
    const step = target / 60
    const timer = setInterval(() => {
      current += step
      if (current >= target) {
        current = target
        clearInterval(timer)
      }
      el.textContent = Math.floor(current).toLocaleString()
      if (target >= 1000) el.textContent = (Math.floor(current)/1000).toFixed(1) + 'K+'
      else el.textContent = Math.floor(current) + (target === 24 ? '' : '+')
    }, 25)
  })
}

// Scroll-triggered entrance animations
const observeElements = () => {
  const io = new IntersectionObserver((entries) => {
    entries.forEach(e => {
      if (e.isIntersecting) {
        e.target.classList.add('visible')
        io.unobserve(e.target)
      }
    })
  }, { threshold: 0.15 })

  document.querySelectorAll('.feature-card, .stat-card, .dept-card, .step-item').forEach(el => {
    el.classList.add('reveal')
    io.observe(el)
  })
}

const onResize = () => {
  if (particleCanvas.value) {
    particleCanvas.value.width = window.innerWidth
    particleCanvas.value.height = window.innerHeight
  }
}

onMounted(() => {
  initParticles()
  window.addEventListener('resize', onResize)

  // Staggered hero entrance
  setTimeout(() => heroBadge.value?.classList.add('enter'), 200)
  setTimeout(() => heroTitle.value?.classList.add('enter'), 400)
  setTimeout(() => heroSubtitle.value?.classList.add('enter'), 600)
  setTimeout(() => heroCtas.value?.classList.add('enter'), 800)
  setTimeout(() => {
    heroTrust.value?.classList.add('enter')
    animateCounters()
  }, 1000)

  setTimeout(observeElements, 300)
})

onUnmounted(() => {
  cancelAnimationFrame(animFrame)
  window.removeEventListener('resize', onResize)
})
</script>

<style scoped>
/* ===== BASE ===== */
.home-wrapper {
  position: relative;
  overflow-x: hidden;
  color: #e0e0e0;
  font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
}

.particle-canvas {
  position: fixed;
  top: 0; left: 0;
  width: 100%; height: 100%;
  pointer-events: none;
  z-index: 0;
  opacity: 0.7;
}

.glass-card-home {
  background: rgba(15, 20, 25, 0.65);
  backdrop-filter: blur(14px);
  -webkit-backdrop-filter: blur(14px);
  border: 1px solid rgba(255,255,255,0.08);
  box-shadow: 0 8px 40px rgba(0,0,0,0.5);
}

/* ===== NAVBAR ===== */
.home-nav {
  position: fixed;
  top: 0; left: 0; right: 0;
  z-index: 100;
  padding: 1rem 0;
  backdrop-filter: blur(20px);
  border-bottom: 1px solid rgba(255,255,255,0.05);
  transition: all 0.3s ease;
}

.nav-inner {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 2rem;
}

.nav-brand {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  text-decoration: none;
}

.brand-icon {
  color: var(--neon-cyan);
  font-size: 1.2rem;
  animation: spinSlow 8s linear infinite;
}

@keyframes spinSlow {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.brand-name {
  font-size: 1.15rem;
  font-weight: 700;
  color: #fff;
  letter-spacing: 0.5px;
}

.nav-links {
  display: flex;
  gap: 2.5rem;
}

.nav-link {
  color: rgba(255,255,255,0.6);
  text-decoration: none;
  font-size: 0.9rem;
  letter-spacing: 0.5px;
  transition: color 0.2s ease;
  position: relative;
}

.nav-link::after {
  content: '';
  position: absolute;
  bottom: -4px; left: 0;
  width: 0; height: 1px;
  background: var(--neon-cyan);
  transition: width 0.3s ease;
}

.nav-link:hover {
  color: var(--neon-cyan);
}

.nav-link:hover::after { width: 100%; }

.nav-actions {
  display: flex;
  gap: 0.75rem;
  align-items: center;
}

.btn-ghost {
  color: rgba(255,255,255,0.7);
  text-decoration: none;
  font-size: 0.9rem;
  padding: 0.4rem 1rem;
  border-radius: 20px;
  transition: color 0.2s ease;
}

.btn-ghost:hover { color: #fff; }

.btn-neon-home {
  background: transparent;
  color: var(--neon-cyan);
  border: 1px solid var(--neon-cyan);
  text-decoration: none;
  font-size: 0.85rem;
  font-weight: 600;
  padding: 0.45rem 1.2rem;
  border-radius: 20px;
  letter-spacing: 0.5px;
  transition: all 0.3s ease;
}

.btn-neon-home:hover {
  background: var(--neon-cyan);
  color: #000;
  box-shadow: 0 0 18px rgba(0,243,255,0.5);
}

/* ===== HERO ===== */
.hero-section {
  position: relative;
  min-height: 100vh;
  display: flex;
  align-items: center;
  padding: 8rem 2rem 4rem;
  overflow: hidden;
  z-index: 1;
  grid-template-columns: 1.5fr 1fr; /* Gives the text area 60% of the width */
}

.hero-grid-overlay {
  position: absolute;
  inset: 0;
  background-image:
    linear-gradient(rgba(0,243,255,0.03) 1px, transparent 1px),
    linear-gradient(90deg, rgba(0,243,255,0.03) 1px, transparent 1px);
  background-size: 60px 60px;
  pointer-events: none;
}

.hero-content {
  max-width: 1200px; 
  width: 100%;
  margin: 0 auto;
  padding: 0 2rem;
  
  /* Ensure children can expand */
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}

/* Entrance animations */
.hero-badge, .hero-title, .hero-subtitle, .hero-ctas, .hero-trust {
  opacity: 0;
  transform: translateY(24px);
  transition: opacity 0.7s ease, transform 0.7s ease;
}

.hero-badge.enter, .hero-title.enter, .hero-subtitle.enter,
.hero-ctas.enter, .hero-trust.enter {
  opacity: 1;
  transform: translateY(0);
}

.hero-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  background: rgba(0,243,255,0.08);
  border: 1px solid rgba(0,243,255,0.2);
  border-radius: 20px;
  padding: 0.3rem 0.9rem;
  font-size: 0.8rem;
  color: var(--neon-cyan);
  margin-bottom: 1.5rem;
  letter-spacing: 0.5px;
}

.pulse-dot {
  width: 7px; height: 7px;
  background: var(--neon-cyan);
  border-radius: 50%;
  animation: pulse 2s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% { box-shadow: 0 0 0 0 rgba(0,243,255,0.6); }
  50% { box-shadow: 0 0 0 6px rgba(0,243,255,0); }
}

.hero-title {
  font-size: clamp(3rem, 7vw, 5.5rem);
  font-weight: 800;
  line-height: 1.05;
  letter-spacing: -2px;
  margin-bottom: 1.5rem;
  display: flex;
  flex-direction: column;
  flex-wrap: wrap; /* Allows wrapping on small mobile screens if needed */
  gap: 0.5rem;
}

.line { display: inline-block;color: #fff; }

.line-2 {
  background: linear-gradient(135deg, var(--neon-cyan), var(--neon-mint));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.title-accent {
  color: var(--neon-cyan);
  -webkit-text-fill-color: var(--neon-cyan);
}

.hero-subtitle {
  max-width: 700px; 
  font-size: 1.125rem;
  line-height: 1.6;
  color: rgba(255, 255, 255, 0.7);
  margin-bottom: 2.5rem;
  
  /* Ensure it doesn't center-align if you want the "wide" look */
  text-align: left;
}

.hero-ctas {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  flex-wrap: wrap;
  margin-bottom: 3.5rem;
}

.cta-primary {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  background: linear-gradient(135deg, var(--neon-cyan), var(--neon-mint));
  color: #000;
  text-decoration: none;
  font-weight: 700;
  font-size: 0.95rem;
  padding: 0.75rem 1.75rem;
  border-radius: 30px;
  transition: all 0.3s ease;
  letter-spacing: 0.3px;
}

.cta-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 30px rgba(0,243,255,0.4);
  color: #000;
}

.cta-primary:active { transform: translateY(0); }

.cta-secondary {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  color: rgba(255,255,255,0.6);
  text-decoration: none;
  font-size: 0.9rem;
  transition: color 0.2s ease;
}

.cta-secondary:hover { color: #fff; }

.play-icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 34px; height: 34px;
  background: rgba(255,255,255,0.08);
  border: 1px solid rgba(255,255,255,0.15);
  border-radius: 50%;
  font-size: 0.65rem;
  transition: all 0.3s ease;
}

.cta-secondary:hover .play-icon {
  background: rgba(0,243,255,0.15);
  border-color: var(--neon-cyan);
  color: var(--neon-cyan);
}

.hero-trust {
  display: flex;
  align-items: center;
  gap: 2rem;
}

.trust-item { text-align: center; }

.trust-num {
  display: block;
  font-size: 1.6rem;
  font-weight: 800;
  color: var(--neon-cyan);
  letter-spacing: -1px;
}

.trust-label {
  font-size: 0.75rem;
  color: rgba(255,255,255,0.4);
  letter-spacing: 0.5px;
  text-transform: uppercase;
}

.trust-divider {
  width: 1px; height: 40px;
  background: rgba(255,255,255,0.1);
}

/* Floating cards */
.hero-floating-cards {
  position: absolute;
  right: 15%;
  top: 50%;
  transform: translateY(-50%);
  display: flex;
  flex-direction: column;
  gap: 1.2rem;
  z-index: 3;
}

.float-card {
  border-radius: 16px;
  padding: 1rem 1.2rem;
  display: flex;
  align-items: center;
  gap: 0.85rem;
  min-width: 220px;
  transition: transform 0.3s ease;
}

.float-card:hover { transform: translateX(-4px); }

.card-1 { animation: floatA 4s ease-in-out infinite; }
.card-2 { animation: floatB 4.5s ease-in-out infinite; }
.card-3 { animation: floatA 5s ease-in-out infinite; }

@keyframes floatA {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-8px); }
}

@keyframes floatB {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-6px); }
}

.fc-row { display: flex; align-items: center; gap: 0.85rem; }

.fc-icon {
  width: 38px; height: 38px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.1rem;
  flex-shrink: 0;
}

.fc-cyan { background: rgba(0,243,255,0.15); border: 1px solid rgba(0,243,255,0.3); }
.fc-mint { background: rgba(0,255,157,0.15); border: 1px solid rgba(0,255,157,0.3); }

.fc-label { font-size: 0.7rem; color: rgba(255,255,255,0.4); text-transform: uppercase; letter-spacing: 0.5px; }
.fc-value { font-size: 0.95rem; font-weight: 600; color: #fff; }
.fc-sub { font-size: 0.75rem; color: var(--neon-cyan); }

/* Scroll hint */
.scroll-hint {
  position: absolute;
  bottom: 2.5rem;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.7rem;
  letter-spacing: 2px;
  text-transform: uppercase;
  color: rgba(255,255,255,0.3);
}

.scroll-line {
  width: 1px; height: 40px;
  background: linear-gradient(to bottom, rgba(0,243,255,0.5), transparent);
  animation: scrollDrop 1.8s ease-in-out infinite;
}

@keyframes scrollDrop {
  0% { transform: scaleY(0); transform-origin: top; opacity: 1; }
  50% { transform: scaleY(1); transform-origin: top; opacity: 1; }
  100% { transform: scaleY(1); transform-origin: bottom; opacity: 0; }
}

/* ===== SECTION SHARED ===== */
.features-section, .dept-section, .steps-section {
  position: relative;
  z-index: 1;
  max-width: 1200px;
  margin: 0 auto;
  padding: 5rem 2rem;
}

.section-header {
  text-align: center;
  margin-bottom: 3.5rem;
}

.section-tag {
  display: inline-block;
  font-size: 0.75rem;
  letter-spacing: 2px;
  text-transform: uppercase;
  color: var(--neon-cyan);
  background: rgba(0,243,255,0.08);
  border: 1px solid rgba(0,243,255,0.2);
  border-radius: 20px;
  padding: 0.25rem 0.9rem;
  margin-bottom: 1rem;
}

.section-title {
  font-size: clamp(2rem, 4vw, 3rem);
  font-weight: 800;
  color: #fff;
  letter-spacing: -1px;
  line-height: 1.2;
}

/* ===== FEATURES ===== */
.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  gap: 1.25rem;
}

.feature-card {
  border-radius: 20px;
  padding: 2rem;
  cursor: default;
  transition: transform 0.3s ease, border-color 0.3s ease, box-shadow 0.3s ease;
  position: relative;
  overflow: hidden;
}

.feature-card::before {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg, rgba(0,243,255,0.04), transparent);
  opacity: 0;
  transition: opacity 0.3s ease;
  border-radius: 20px;
}

.feature-card.feat-active {
  transform: translateY(-4px);
  border-color: rgba(0,243,255,0.25) !important;
  box-shadow: 0 16px 50px rgba(0,0,0,0.6), 0 0 30px rgba(0,243,255,0.08);
}

.feature-card.feat-active::before { opacity: 1; }

.feat-icon-wrap {
  width: 50px; height: 50px;
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 1.25rem;
}

.icon-cyan { background: rgba(0,243,255,0.12); border: 1px solid rgba(0,243,255,0.25); }
.icon-mint { background: rgba(0,255,157,0.12); border: 1px solid rgba(0,255,157,0.25); }

.feat-icon { font-size: 1.4rem; }

.feat-title {
  font-size: 1.05rem;
  font-weight: 700;
  color: #fff;
  margin-bottom: 0.6rem;
}

.feat-desc {
  font-size: 0.88rem;
  color: rgba(255,255,255,0.5);
  line-height: 1.65;
  margin-bottom: 1rem;
}

.feat-arrow {
  color: var(--neon-cyan);
  font-size: 1.1rem;
  opacity: 0;
  transform: translateX(-8px);
  transition: all 0.3s ease;
}

.feature-card.feat-active .feat-arrow {
  opacity: 1;
  transform: translateX(0);
}

/* ===== STATS ===== */
.stats-section {
  position: relative;
  z-index: 1;
  padding: 5rem 2rem;
  overflow: hidden;
}

.stats-bg-glow {
  position: absolute;
  top: 50%; left: 50%;
  transform: translate(-50%, -50%);
  width: 600px; height: 600px;
  background: radial-gradient(circle, rgba(0,243,255,0.05), transparent 70%);
  pointer-events: none;
}

.stats-inner {
  max-width: 1200px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 5rem;
  align-items: center;
}

.stats-body {
  font-size: 0.95rem;
  color: rgba(255,255,255,0.5);
  line-height: 1.75;
  margin-top: 1rem;
}

.stats-cards {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.stat-card {
  border-radius: 18px;
  padding: 1.5rem;
  transition: transform 0.3s ease;
}

.stat-card:hover { transform: translateY(-4px); }

.stat-num {
  font-size: 2rem;
  font-weight: 800;
  letter-spacing: -1px;
  margin-bottom: 0.3rem;
}

.stat-label {
  font-size: 0.8rem;
  color: rgba(255,255,255,0.45);
  margin-bottom: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.stat-bar {
  height: 3px;
  background: rgba(255,255,255,0.08);
  border-radius: 2px;
  overflow: hidden;
}

.stat-bar-fill {
  height: 100%;
  border-radius: 2px;
  transition: width 1.5s ease;
}

/* ===== DEPARTMENTS ===== */
.dept-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
  gap: 1rem;
}

.dept-card {
  position: relative;
  background: rgba(15,20,25,0.65);
  border: 1px solid rgba(255,255,255,0.07);
  border-radius: 18px;
  padding: 1.75rem 1rem;
  text-align: center;
  cursor: default;
  overflow: hidden;
  transition: border-color 0.3s ease, transform 0.3s ease;
  backdrop-filter: blur(10px);
}

.dept-card.dept-hovered {
  transform: translateY(-5px) scale(1.02);
  border-color: rgba(0,243,255,0.2);
}

.dept-glow {
  position: absolute;
  inset: 0;
  opacity: 0;
  transition: opacity 0.4s ease;
  pointer-events: none;
}

.dept-card.dept-hovered .dept-glow { opacity: 1; }

.dept-icon {
  font-size: 2rem;
  margin-bottom: 0.75rem;
  display: block;
  transition: transform 0.3s ease;
}

.dept-card.dept-hovered .dept-icon { transform: scale(1.2); }

.dept-name {
  font-size: 0.9rem;
  font-weight: 600;
  color: #fff;
  margin-bottom: 0.25rem;
}

.dept-count {
  font-size: 0.72rem;
  color: rgba(255,255,255,0.35);
}

/* ===== STEPS ===== */
.steps-track {
  position: relative;
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 2rem;
}

.steps-line {
  position: absolute;
  top: 1.5rem;
  left: calc(16.67% + 1rem);
  right: calc(16.67% + 1rem);
  height: 1px;
  background: linear-gradient(to right, var(--neon-cyan), var(--neon-mint));
  opacity: 0.3;
  z-index: 0;
}

.step-item {
  position: relative;
  z-index: 1;
}

.step-num {
  font-size: 0.7rem;
  font-weight: 800;
  letter-spacing: 2px;
  color: var(--neon-cyan);
  margin-bottom: 1rem;
  text-align: center;
  display: block;
  background: rgba(0,243,255,0.1);
  border: 1px solid rgba(0,243,255,0.2);
  width: 36px; height: 36px;
  border-radius: 50%;
  line-height: 34px;
  margin: 0 auto 1.2rem;
}

.step-body {
  border-radius: 20px;
  padding: 1.75rem;
  text-align: center;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.step-body:hover {
  transform: translateY(-4px);
  box-shadow: 0 20px 60px rgba(0,0,0,0.5), 0 0 30px rgba(0,243,255,0.06);
}

.step-icon { font-size: 1.8rem; display: block; margin-bottom: 1rem; }

.step-title {
  font-size: 1rem;
  font-weight: 700;
  color: #fff;
  margin-bottom: 0.5rem;
}

.step-desc {
  font-size: 0.85rem;
  color: rgba(255,255,255,0.45);
  line-height: 1.6;
}

/* ===== CTA BANNER ===== */
.cta-banner {
  position: relative;
  z-index: 1;
  text-align: center;
  padding: 6rem 2rem;
  overflow: hidden;
  border-top: 1px solid rgba(255,255,255,0.05);
  border-bottom: 1px solid rgba(255,255,255,0.05);
}

.cta-bg-glow {
  position: absolute;
  top: 50%; left: 50%;
  transform: translate(-50%, -50%);
  width: 800px; height: 400px;
  background: radial-gradient(ellipse, rgba(0,243,255,0.07), transparent 65%);
  pointer-events: none;
}

.cta-content { position: relative; z-index: 1; }

.cta-title {
  font-size: clamp(2.2rem, 5vw, 3.5rem);
  font-weight: 800;
  color: #fff;
  letter-spacing: -1.5px;
  line-height: 1.2;
  margin-bottom: 1rem;
}

.cta-sub {
  font-size: 1rem;
  color: rgba(255,255,255,0.45);
  margin-bottom: 2.5rem;
}

.cta-btns {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1.5rem;
  flex-wrap: wrap;
}

.cta-large { font-size: 1.05rem; padding: 0.9rem 2.5rem; }

.cta-ghost {
  color: rgba(255,255,255,0.5);
  text-decoration: none;
  font-size: 0.95rem;
  transition: color 0.2s ease;
}

.cta-ghost:hover { color: #fff; }

/* ===== FOOTER ===== */
.home-footer {
  position: relative;
  z-index: 1;
  padding: 2rem;
}

.footer-inner {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 1rem;
}

.footer-brand {
  display: flex;
  align-items: center;
  gap: 0.4rem;
}

.footer-copy {
  font-size: 0.8rem;
  color: rgba(255,255,255,0.3);
  margin: 0;
}

.footer-links {
  display: flex;
  gap: 1.5rem;
}

.footer-links a {
  font-size: 0.8rem;
  color: rgba(255,255,255,0.35);
  text-decoration: none;
  transition: color 0.2s ease;
}

.footer-links a:hover { color: var(--neon-cyan); }

/* ===== SCROLL REVEAL ===== */
.reveal {
  opacity: 0;
  transform: translateY(28px);
  transition: opacity 0.6s ease, transform 0.6s ease;
}

.reveal.visible {
  opacity: 1;
  transform: translateY(0);
}

/* stagger for grids */
.features-grid .feature-card:nth-child(1) { transition-delay: 0s; }
.features-grid .feature-card:nth-child(2) { transition-delay: 0.08s; }
.features-grid .feature-card:nth-child(3) { transition-delay: 0.16s; }
.features-grid .feature-card:nth-child(4) { transition-delay: 0.24s; }
.features-grid .feature-card:nth-child(5) { transition-delay: 0.32s; }
.features-grid .feature-card:nth-child(6) { transition-delay: 0.4s; }

.dept-grid .dept-card:nth-child(odd) { transition-delay: 0.05s; }
.dept-grid .dept-card:nth-child(even) { transition-delay: 0.1s; }

/* ===== RESPONSIVE ===== */
@media (max-width: 900px) {
  .hero-floating-cards { display: none; }
  .stats-inner { grid-template-columns: 1fr; gap: 2.5rem; }
  .steps-track { grid-template-columns: 1fr; }
  .steps-line { display: none; }
  .nav-links { display: none; }
}

@media (max-width: 600px) {
  .hero-section { padding: 7rem 1.5rem 4rem; }
  .features-grid { grid-template-columns: 1fr; }
  .stats-cards { grid-template-columns: 1fr 1fr; }
  .dept-grid { grid-template-columns: repeat(auto-fill, minmax(130px, 1fr)); }
  .footer-inner { flex-direction: column; text-align: center; }
}
</style>