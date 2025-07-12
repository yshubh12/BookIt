# 🧵 BookIt - AI Appointment Booking Assistant

**BookIt** is an AI-powered appointment booking assistant built using **LangGraph**, **LangChain**, and **Streamlit**, integrated with **Google Calendar API**. Users can interact naturally, like “Book a meeting tomorrow at 3 PM”, and BookIt will understand the intent, parse the time, check for availability, and book appointments for them.

---

## 🚀 Features

- ✅ **Natural language booking**
- ✅ **Google Calendar integration**
- ✅ **Live slot checking**
- ✅ **Readable confirmations**
- ✅ **Streamlit chatbot UI**
- ✅ **Graceful fallback if parsing fails**
- ✅ **Intent routing via LangGraph**

---

## 🛠️ Tech Stack

| Component     | Tech Used                      |
|---------------|--------------------------------|
| UI            | Streamlit                      |
| Backend       | FastAPI                        |
| AI Model      | OpenAI (via LangChain)         |
| Scheduling    | Google Calendar API            |
| Time Parsing  | `dateparser`                   |
| State Management | LangGraph (`StateGraph`)    |

---

## 📦 Installation

### 1. Clone the repository


git clone https://github.com/yourusername/BookIt.git
cd bookit

### 2. Set up a virtual environment

python -m venv agent
source agent/bin/activate  # on Windows: agent\Scripts\activate

### 3. Install dependencies

pip install -r requirements.txt

### 4. Set up OpenAI and Google credentials

OPENAI_API_KEY=your_openai_api_key

Add your Google credentials.json to the project root.

On first run, the app will generate token.json after you authorize it in a browser.

🧠 How It Works
LangGraph Agent Flow
1. User Message → "Book a meeting tomorrow at 3 PM"

2. Router Node determines intent → check_time

3. Time Parser extracts time from natural text

4. Slot Checker verifies availability in Google Calendar

5. If close match found → ✅ books appointment automatically

6. Else → 🕒 fallback: ask user to select slot manually

▶️ Running the Project
1. Start the backend (FastAPI)

uvicorn main:app --reload

2. Start the frontend (Streamlit)

streamlit run streamlit_app.py


📅 Google Calendar Integration
Ensure you’ve:

Enabled Google Calendar API from Google Cloud Console

Added credentials.json from OAuth 2.0 Client ID

Set Test Users in OAuth Consent Screen

Authorized on first run → token.json will be created