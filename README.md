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
