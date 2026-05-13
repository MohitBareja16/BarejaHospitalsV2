<template>
  <div id="app-wrapper">
    <main class="container-fluid py-4">
      <router-view />
    </main>
  </div>
</template>

<style>
:root {
  --neon-cyan: #00f3ff;
  --neon-mint: #00ff9d;
  --glass-bg: rgba(15, 20, 25, 0.7);
  --glass-border: rgba(255, 255, 255, 0.1);
}

body, html {
  height: 100%;
  margin: 0;
  font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
  background-color: #050505;
  color: #e0e0e0;
}

#app-wrapper {
  min-height: 100vh;
  background-image: linear-gradient(to bottom, rgba(5, 5, 5, 0.8), rgba(10, 15, 20, 0.9)), 
                    url('https://images.unsplash.com/photo-1579684385127-1ef15d508118?q=80&w=2000&auto=format&fit=crop');
  background-size: cover;
  background-position: center;
  background-attachment: fixed;
}

.glass-card {
  background: var(--glass-bg) !important;
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border: 1px solid var(--glass-border) !important;
  box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.5);
  color: white;
}

.form-control.glass-input {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid var(--glass-border);
  color: white;
}

.form-control.glass-input:focus {
  background: rgba(255, 255, 255, 0.1);
  border-color: var(--neon-cyan);
  box-shadow: 0 0 10px rgba(0, 243, 255, 0.3);
  color: white;
}

.btn-neon {
  background: transparent;
  color: var(--neon-cyan);
  border: 1px solid var(--neon-cyan);
  transition: all 0.3s ease;
}

.btn-neon:hover {
  background: var(--neon-cyan);
  color: #000;
  box-shadow: 0 0 15px var(--neon-cyan);
}
</style>