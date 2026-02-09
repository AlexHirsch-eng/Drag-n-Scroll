# 🚀 Deployment Guide

## Quick Deploy (Recommended)

### Option A: PowerShell (Windows)

```powershell
cd frontend
.\deploy-vercel.ps1
```

### Option B: Bash (Linux/Mac)

```bash
cd frontend
chmod +x deploy-vercel.sh
./deploy-vercel.sh
```

### Option C: Manual Vercel CLI

```bash
cd frontend
npx vercel login
npx vercel --prod --yes
```

---

## 📋 What This Does

The script will:
1. ✓ Check if Vercel CLI is installed
2. ✓ Login to Vercel (opens browser)
3. ✓ Build the frontend with Vite
4. ✓ Deploy to https://drag-n-scroll.vercel.app
5. ✓ Set environment variables automatically

---

## 🔧 Environment Variables

The following variables are set automatically:
- `VITE_API_BASE_URL` = `https://drag-n-scroll.onrender.com/api`

---

## ✅ After Deployment

1. **Open browser in INCOGNITO mode** (Ctrl+Shift+N)
2. Go to: https://drag-n-scroll.vercel.app
3. **Hard refresh** (Ctrl+Shift+R)
4. Test:
   - Click "Open App" button
   - Register new account
   - Login
   - Should see learning screen without 404 errors

---

## 🐛 Troubleshooting

### Q: Still seeing old build (index-BVZ62spy.js)?
A: Clear browser cache or use incognito mode

### Q: Getting 404 on /api/learning/main-screen/?
A: Make sure VITE_API_BASE_URL is set in Vercel:
- Go to https://vercel.com/dashboard
- Your project → Settings → Environment Variables
- Add: `VITE_API_BASE_URL` = `https://drag-n-scroll.onrender.com/api`
- Redeploy

### Q: Vercel login not working?
A: Try: `npx vercel login --github`

---

## 📊 Current Status

Backend (Render): ✅ Working
- https://drag-n-scroll.onrender.com/api/health/ → 200 OK
- https://drag-n-scroll.onrender.com/api/learning/main-screen/ → 401 (auth required)

Frontend (Vercel): ⏳ Needs deployment
- Current build: index-BVZ62spy.js (OLD)
- Expected: New build with correct API URL

---

## 🎯 Expected URLs After Fix

```
Frontend: https://drag-n-scroll.vercel.app
Backend:  https://drag-n-scroll.onrender.com/api
API Call: https://drag-n-scroll.onrender.com/api/learning/main-screen/
```
