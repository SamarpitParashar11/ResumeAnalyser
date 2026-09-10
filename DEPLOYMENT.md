# Deployment Guide — Streamlit Community Cloud

This project is a **stateful Streamlit application** with in-memory session tracking and active WebSocket connections. 

> [!IMPORTANT]
> **Why Not Vercel?**  
> Vercel is designed for stateless serverless HTTP functions (Next.js, static sites, APIs). Streamlit requires continuous, persistent WebSockets (`/_stcore/stream`) to sync UI clicks, file uploads, and session states. Running Streamlit on Vercel causes broken WebSocket connections and session dropouts.
> 
> **Streamlit Community Cloud** is the official, 100% free hosting platform designed natively for Streamlit applications.

---

## 🚀 1-Click Deployment (Recommended)

### Step 1: Commit and Push Code to GitHub

Ensure all your latest changes are pushed to your GitHub repository:

```bash
git add .
git commit -m "Prepare repository for Streamlit Cloud deployment"
git push origin main
```

---

### Step 2: Connect to Streamlit Community Cloud

1. Visit **[share.streamlit.io](https://share.streamlit.io/)**.
2. Click **Sign in with GitHub**.
3. Once logged in, click the **"New app"** button.

---

### Step 3: Configure Your App

Fill in the deployment form:

| Field | Value |
| :--- | :--- |
| **Repository** | Your GitHub repository (e.g. `username/ai-resume-interview-agent`) |
| **Branch** | `main` (or your primary branch) |
| **Main file path** | `app.py` |
| **App URL** | Choose a custom subdomain (e.g., `my-resume-analyzer.streamlit.app`) |

---

### Step 4: Configure Secrets (Gemini API Key)

1. Click **Advanced settings...** at the bottom of the form (or go to **App Settings ➔ Secrets** after creation).
2. Under the **Secrets** text area, paste your configuration in TOML format:

```toml
GEMINI_API_KEY = "AIzaSy..."
GEMINI_MODEL = "gemini-flash-latest"
```

> [!TIP]
> If you don't configure secrets beforehand, the app will gracefully prompt the user in the sidebar for their Gemini API key at runtime.

---

### Step 5: Deploy

Click **"Deploy!"**. 

Streamlit Community Cloud will:
1. Provision a dedicated container.
2. Install dependencies automatically from [`requirements.txt`](requirements.txt).
3. Apply settings from [`.streamlit/config.toml`](.streamlit/config.toml).
4. Launch your app with automated HTTPS and active WebSocket streaming.

---

## 🔄 Updating Your Live App

Whenever you push new code to your GitHub `main` branch, Streamlit Community Cloud automatically rebuilds and redeploys your app in seconds with zero manual intervention.

---

## 🛠️ Alternative Hosting Options (Container / Docker)

If you need containerized deployments with custom infrastructure:

| Platform | Deployment Type | WebSocket Support | Notes |
| :--- | :--- | :--- | :--- |
| **Streamlit Cloud** | Git Native | ✅ Native | **Recommended**: Free, instant setup |
| **Render** | Web Service (Python/Docker) | ✅ Yes | Set start command to `streamlit run app.py --server.port $PORT` |
| **Hugging Face Spaces** | Streamlit Space | ✅ Yes | Select "Streamlit" as SDK when creating Space |
| **Railway** | Nixpacks / Docker | ✅ Yes | Auto-detects Streamlit from `requirements.txt` |
