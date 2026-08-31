# 📊 Customer Feedback Analyzer

An end-to-end, production-grade AI platform built to analyze customer reviews in real time using structured sentiment analysis.
The project leverages **FastAPI** for backend service delivery, **Streamlit** for an interactive analytics dashboard, **SQLite** for feedback history storage, and **Google Gemini 2.5 Flash** for LLM-powered structured JSON outputs.

---

## 🌟 Key Features

* **LLM Sentiment & Theme Classification:** Uses Google's `gemini-2.5-flash` model with schema enforcement via Pydantic to deliver structured sentiment labels (`positive`, `negative`, `neutral`), numerical ratings (`1–5`), and core feedback topics (e.g., delivery, pricing, food quality).
* **Interactive Web Interface:** Streamlit-powered dashboard allowing batch text processing and real-time visualization of sentiment metrics.
* **Aggregated Insights:** Instant summary metrics for overall dataset sentiment, including average rating score and percentage of positive feedback.
* **Persistent Database Logging:** Local storage using SQLite (`feedback.db`) with full transactional execution.
* **Excel Export Support:** Export saved historical feedback directly to `.xlsx` spreadsheet files for offline data analysis.
* **FastAPI Backend Services:** High-performance RESTful API endpoints built using FastAPI and validated through Pydantic schemas.

---

## 🏗️ Architecture & Technology Stack

* **Frontend:** Streamlit, Pandas, Requests
* **Backend:** FastAPI, Uvicorn
* **AI Model:** Google Gemini API (`google-genai` SDK)
* **Data Validation:** Pydantic v2
* **Database:** SQLite3
* **Package & Environment Management:** `uv`

---

## 📂 Project Structure

```text
customer-feedback-analyzer/
├── api.py               # FastAPI backend with Gemini structured response schema
├── app.py               # Streamlit web dashboard interface
├── database.py          # SQLite helper for initialization, insertion, and query loading
├── pyproject.toml       # Environment configuration and project dependencies managed by uv
├── .env.example         # Template for environment configuration
├── .gitignore           # Excludes secrets (.env) and local database files from Git tracking
└── sample_reviews.txt   # Sample restaurant review dataset for quick execution testing

```

---

## 🚀 Getting Started

### Prerequisites

* Python `>=3.10` installed on your machine.
* `uv` package manager installed:
```powershell
powershell -ExecutionPolicy ByPass -c "irm [https://astral.sh/uv/install.ps1](https://astral.sh/uv/install.ps1) | iex"

```


* A Google Gemini API key from [Google AI Studio](https://aistudio.google.com/).

---

### Installation & Environment Setup

1. **Clone the Repository:**
```bash
git clone [https://github.com/sruthisswaminathan06/feedback-analyzer.git](https://github.com/sruthisswaminathan06/feedback-analyzer.git)
cd feedback-analyzer

```


2. **Sync Dependencies with `uv`:**
```powershell
uv sync

```


3. **Configure Environment Variables:**
Create a `.env` file in the root folder based on `.env.example`:
```env
GEMINI_API_KEY=your_actual_gemini_api_key_here

```



---

## 💻 Running the Application

### 1. Start the FastAPI Backend

In your terminal, launch the Uvicorn server:

```powershell
uv run uvicorn api:app --reload

```

The REST API will start at `http://127.0.0.1:8000`. You can test interactive API documentation by visiting `http://127.0.0.1:8000/docs`.

### 2. Start the Streamlit Frontend

Open a new terminal tab/window and launch the Streamlit app:

```powershell
uv run streamlit run app.py

```

Your browser will automatically open `http://localhost:8501`.

---

## 🧪 Usage Workflow

1. Paste individual customer reviews into the text input area (one review per line).
2. Click **Analyze** to submit reviews to the FastAPI endpoint for Gemini model processing.
3. Review aggregated rating metrics and categorized outputs in the interactive table.
4. Click **Save Results to Database** to log analyzed reviews into SQLite.
5. Click **Download History as Excel (.xlsx)** under the Saved History section to export recorded analytics.

---

## 🔐 Security Notice

This repository contains a `.gitignore` pre-configured to ensure local environment files (`.env`) and database instances (`feedback.db`) are excluded from version control, maintaining complete API key safety.

```
```
### Steps to Commit and Push:

1. Save `README.md` in VS Code.
2. In your terminal, commit and push the updated file:
   ```powershell
   git add README.md
   git commit -m "Add detailed README.md documentation"
   git push origin master

```
