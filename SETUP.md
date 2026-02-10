# SentraAI Setup & Run Guide

This guide walks through setting up and running both the backend (FastAPI) and frontend (Next.js) locally with ticket classification functionality.

## Prerequisites

- Python 3.9+
- Node.js 18+
- npm or yarn

## Backend Setup (FastAPI Ticket Classifier)

1. **Create and activate Python environment:**

   ```bash
   cd c:\Users\Asus\Desktop\repos\sentra_ai
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1   # PowerShell on Windows
   ```

2. **Install backend dependencies:**

   ```bash
   pip install -r backend/requirements.txt
   ```

3. **Run FastAPI server:**

   ```bash
   uvicorn backend.app.main:app --reload --host 127.0.0.1 --port 8000
   ```

   The server will:
   - Load or train the TF-IDF + Logistic Regression model on startup
   - Expose `/predict` endpoint at `http://127.0.0.1:8000/predict`
   - Expose `/train` endpoint for retraining with new examples
   - Expose `/labels` endpoint to list supported categories

   **Test backend endpoint with curl:**

   ```bash
   curl -X POST http://127.0.0.1:8000/predict `
     -H "Content-Type: application/json" `
     -d '{"text":"I want a refund for my last order"}'
   ```

## Frontend Setup (Next.js)

1. **Install frontend dependencies:**

   ```bash
   cd frontend
   npm install
   ```

2. **Create `.env.local` file in the frontend folder:**

   ```
   NEXT_PUBLIC_API_URL=http://127.0.0.1:8000
   ```

   This tells the frontend where to reach the backend. Default fallback is `http://127.0.0.1:8000` if not set.

3. **Run Next.js dev server:**

   ```bash
   npm run dev
   ```

   Frontend will be available at `http://localhost:3000`

## Full Stack Testing

1. **Open http://localhost:3000** in your browser
2. **Paste a support ticket** in the input field (e.g., "I want a refund for my last purchase")
3. **Click "Analyze Ticket"**
4. **Result page will display:**
   - The ticket category classification from the TF-IDF + Logistic Regression model
   - Simulated sentiment and churn predictions (to be replaced with real models)

## Supported Ticket Categories

- **Billing** — Invoicing and payment issues
- **Technical** — App errors, server issues
- **Account** — Login, password, profile management
- **Feature** — Feature requests
- **Refund Request** — Refund demands
- **Service Complaint** — Poor service experience

## Troubleshooting

### Backend not starting?

- Ensure venv is activated: `.\.venv\Scripts\Activate.ps1`
- Check requirements installed: `pip list | grep -i scikit`
- Verify port 8000 is free: `netstat -ano | findstr :8000`

### Frontend stuck on loading?

- Check if backend is running at `http://127.0.0.1:8000`
- Check browser console (F12) for CORS or fetch errors
- Ensure `.env.local` has correct `NEXT_PUBLIC_API_URL`

### No classification shown?

- Open browser Dev Tools (F12) → Console tab
- Check for "Prediction error" message
- Verify backend is responding: `curl http://127.0.0.1:8000/labels`

## Production Deployment

See [backend/DEPLOYMENT.md](backend/DEPLOYMENT.md) for production build and hosting guidelines.
