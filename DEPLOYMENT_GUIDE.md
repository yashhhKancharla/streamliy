# Deployment Guide - Two Service Architecture

## Overview
This app uses a **two-service architecture** for reliability and scalability:
- **Service 1**: Flask Backend (Render) - API server
- **Service 2**: Streamlit Frontend (Streamlit Cloud) - UI

---

## Step 1: Deploy Backend to Render

### 1.1 Create Render Service
1. Go to https://render.com/dashboard
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repository `yashhhKancharla/streamliy`

### 1.2 Fill Render Configuration Form

| Field | Value |
|-------|-------|
| **Name** | `streamliy-backend` |
| **Language** | `Python 3` |
| **Branch** | `main` |
| **Root Directory** | (leave empty) |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `bash render_backend.sh` |
| **Region** | `Oregon (US West)` |

### 1.3 Add Environment Variables (in Render Dashboard)
Click **"Advanced"** and add:

```
OPENROUTER_API_KEY=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
OPENROUTER_MODEL=tngtech/tng-r1t-chimera:free
FLASK_ENV=production
FLASK_DEBUG=0
HOST=0.0.0.0
CHROMA_PERSIST_DIR=./data/chroma
CHROMA_COLLECTION=assignment_index
```

### 1.4 Deploy
- Click **"Create Web Service"**
- Wait for deployment to complete
- Copy your backend URL: `https://streamliy-backend.render.com`

---

## Step 2: Deploy Frontend to Streamlit Cloud

### 2.1 Push Code to GitHub
```bash
git add .
git commit -m "Deploy: Two-service architecture ready for production"
git push origin main
```

### 2.2 Deploy to Streamlit Cloud
1. Go to https://share.streamlit.io
2. Click **"New app"**
3. Connect GitHub repository: `yashhhKancharla/streamliy`
4. Fill form:
   - **Repository**: `yashhhKancharla/streamliy`
   - **Branch**: `main`
   - **Main file path**: `ui_app.py`

### 2.3 Add Secrets (Important!)
1. Click **"Advanced Settings"** ⚙️
2. Go to **"Secrets"** tab
3. Paste this (replace with your actual backend URL):

```toml
OPENROUTER_API_KEY = "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"
OPENROUTER_MODEL = "tngtech/tng-r1t-chimera:free"
API_BASE_URL = "https://streamliy-backend.render.com"
```

### 2.4 Set Python Version
1. In Advanced Settings → **"Python version"**: `3.11`
2. Click **"Save"**

### 2.5 Deploy
- Click **"Deploy"**
- Wait for deployment to complete
- Your app URL: `https://streamliy.streamlit.app`

---

## Step 3: Verify Deployment

### Check Backend Health
```bash
curl https://streamliy-backend.render.com/health
```

Expected response:
```json
{"status": "healthy", "services": {"flask": "ok", "chroma": "ok"}}
```

### Check Frontend
Open: https://streamliy.streamlit.app

Should show "✅ Healthy" in the sidebar if backend connection works.

---

## Environment Variables Summary

### Backend (Render)
```
OPENROUTER_API_KEY=your_key
OPENROUTER_MODEL=tngtech/tng-r1t-chimera:free
FLASK_ENV=production
FLASK_DEBUG=0
HOST=0.0.0.0
```

### Frontend (Streamlit Cloud)
```
OPENROUTER_API_KEY=your_key
OPENROUTER_MODEL=tngtech/tng-r1t-chimera:free
API_BASE_URL=https://streamliy-backend.render.com
```

---

## Troubleshooting

### Issue: Frontend shows "❌ Unhealthy"
**Solution**: Update `API_BASE_URL` in Streamlit Cloud secrets with correct backend URL

### Issue: Backend deployment fails
**Solution**: Check Render logs → ensure all dependencies in `requirements.txt` are compatible

### Issue: Port conflicts
**Solution**: Don't run combined services locally. Use separate scripts and ports:
- Backend: `python start_server.py` (port 8000)
- Frontend: `streamlit run ui_app.py --server.port 8501` (port 8501)

---

## Local Development (Optional)

### Terminal 1 - Backend
```bash
python start_server.py
# Backend runs on http://localhost:8000
```

### Terminal 2 - Frontend
```bash
API_BASE_URL=http://localhost:8000 streamlit run ui_app.py
# Frontend runs on http://localhost:8501
```

---

## Cost Breakdown

| Service | Cost | Notes |
|---------|------|-------|
| Render Backend | $7/month | Includes 750 hours/month |
| Streamlit Cloud | FREE | Unlimited apps |
| **Total** | **$7/month** | Very affordable! |

---

## File Structure

```
streamliy/
├── app/                      # Flask backend
│   ├── main.py              # Flask app entry point
│   ├── config.py            # Configuration
│   ├── api/                 # API endpoints
│   └── services/            # Business logic
├── ui_app.py                # Streamlit frontend
├── render_backend.sh        # Backend startup for Render
├── requirements.txt         # Python dependencies
├── .streamlit/
│   ├── config.toml          # Streamlit config
│   └── secrets.toml         # Secrets template
└── .env                     # Local development only
```

---

## Next Steps

1. ✅ Prepare GitHub repository
2. ✅ Deploy backend to Render
3. ✅ Deploy frontend to Streamlit Cloud
4. ✅ Update API_BASE_URL in Streamlit secrets
5. ✅ Test health check in sidebar
6. ✅ Share app URL with team!

**Happy Deploying! 🚀**
