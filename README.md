# Nest Navigate - Full Stack Developer Assignment

## Live Demo
- **Frontend**: https://nest-navigate-nine.vercel.app
- **Backend**: https://nestnavigate.onrender.com

---

## Architecture Overview

This is a full-stack web application consisting of:

### Frontend
- **Framework**: React (Vite) + TypeScript
- **Styling**: TailwindCSS
- **State Management**: React hooks (`useState`, `useEffect`)
- **API Calls**: Axios with `withCredentials` enabled for secure cookie-based authentication
- **Deployment**: Vercel

### Backend
- **Framework**: FastAPI (Python)
- **Database**: SQLite (local) / PostgreSQL (production-ready)
- **ORM**: SQLAlchemy
- **Auth**: JWT tokens stored in HTTP-only cookies
- **CORS**: Configured for Vercel frontend + local dev
- **Deployment**: Render

---

## Technology Stack
- **Frontend**: React, Vite, TypeScript, TailwindCSS, Axios
- **Backend**: FastAPI, SQLAlchemy, Passlib (password hashing), Python-Jose (JWT)
- **Database**: SQLite (development), PostgreSQL-compatible
- **Hosting**: Vercel (frontend), Render (backend)

---

## Environment Variables

### Backend `.env`
SECRET_KEY=your_secret_key_here
ACCESS_TOKEN_EXPIRE_MINUTES=60
DATABASE_URL=sqlite:///./app.db

### Frontend `.env`
VITE_API_BASE_URL=https://nestnavigate.onrender.com

## Setup Instructions

### Backend
# Clone repository
git clone https://github.com/CoderCruz/nestNavigate
cd backend

# Create virtual environment
python -m venv env
source env/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run backend
uvicorn app.main:app --reload

# Run frontend
cd frontend

# Install dependencies
npm install

# Run frontend
npm run dev

Time Spent
Total Time: ~28 hours over 3 days
Backend Setup & API Development: ~5 hours
Setting up FastAPI, database models, authentication routes, and progress tracking.
Frontend Development & Integration: ~6 hours
Building UI components, handling authentication state, and integrating APIs.
Deployment & Debugging: ~4 hours
Configuring CORS, resolving cookie/auth issues, and ensuring production readiness.

Challenges Faced
CORS & Cookie Authentication in Production
Safari’s Intelligent Tracking Prevention blocked cross-site cookies, requiring testing across browsers and careful configuration with secure=True and samesite="none".
State Synchronization After Login
Ensuring the frontend correctly updated state after authentication, and handling isLoggedIn checks consistently across routes.
Cross-Origin Cookie Persistence Between Vercel and Render
Debugging why cookies were not being stored in certain environments and ensuring that credentials were passed correctly in Axios requests.
Error Handling & Unauthorized Requests
Updating backend routes to gracefully handle None from get_current_user instead of raising server errors, which improved stability in production.
