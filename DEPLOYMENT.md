# Frontend Deployment Guide

## Setup Instructions

### 1. Local Development
```bash
cd frontend
npm install
npm run dev
```

The app will use `http://127.0.0.1:5000` as the API base URL (from `.env`)

### 2. Environment Configuration

**Development** (`.env`):
```
VITE_API_BASE_URL=http://127.0.0.1:5000
```

**Production** (`.env.production`):
```
VITE_API_BASE_URL=https://your-backend-api.com
```

### 3. Building for Production
```bash
npm run build
```

This generates optimized files in the `dist/` folder

### 4. Deploying to Vercel

1. Connect your GitHub repository to Vercel
2. Set environment variable in Vercel dashboard:
   - Key: `VITE_API_BASE_URL`
   - Value: Your backend API URL (e.g., `https://your-backend.herokuapp.com`)
3. Vercel will automatically:
   - Detect `package.json`
   - Run `npm install`
   - Run `npm run build`
   - Deploy the `dist/` folder

### 5. API Configuration

All API calls now use a centralized config file (`src/config.js`):
- Environment variable: `VITE_API_BASE_URL`
- Default fallback: `http://127.0.0.1:5000`

The config exposes all API endpoints as constants for easy maintenance.

### 6. Files Structure

✅ **Frontend Ready Files:**
- `src/config.js` - Centralized API configuration
- `.env` - Development environment
- `.env.production` - Production environment
- `.env.example` - Template for team

✅ **All views updated:**
- `LoginView.vue` - Uses `apiConfig.login`
- `RegisterView.vue` - Uses `apiConfig.register`
- `AdminDashboard.vue` - All endpoints use `apiConfig`
- `DoctorDashboard.vue` - All endpoints use `apiConfig`
- `PatientDashboard.vue` - All endpoints use `apiConfig`

### 7. Before Pushing to GitHub

⚠️ **DO NOT** commit `.env` file
✅ **DO** commit `.env.example` (without actual values)
✅ **DO** commit `.env.production` (with your production URL)

## Notes for Backend Deployment

Your backend needs to be deployed separately (not supported by Vercel).
Options:
- **Railway**: Simple Flask deployment, comes with PostgreSQL
- **Render**: Free tier available for Python apps
- **Heroku**: Popular but now requires payment
- **AWS**: Lambda functions or EC2 instances

Set `VITE_API_BASE_URL` in Vercel to your backend URL.
