# ⚡ EduAI Hub — Final Year Project

**An AI-Powered Learning & Career Assistant for Students & Employees**

Built with: Python Flask + Google Gemini AI

---

## 📁 Project Structure

```
EduAI-Hub/
├── app.py                  ← Main Python/Flask server (backend)
├── requirements.txt        ← Python libraries to install
└── templates/
    ├── index.html          ← Home page
    ├── tutor.html          ← AI Tutor module
    ├── quiz.html           ← Quiz Generator module
    ├── resume.html         ← Resume Analyzer module
    ├── interview.html      ← Interview Prep module
    └── news.html           ← Tech News module
```

---

## 🚀 STEP-BY-STEP SETUP (Beginner Level)

### STEP 1 — Install Python
- Download Python 3.10+ from https://python.org
- During installation, CHECK "Add Python to PATH"
- Verify: Open CMD/Terminal → type `python --version`

### STEP 2 — Install VS Code
- Download from https://code.visualstudio.com
- Install the "Python" extension from VS Code marketplace

### STEP 3 — Get FREE Gemini API Key
1. Go to https://aistudio.google.com
2. Sign in with your Google account
3. Click "Get API Key" → "Create API Key"
4. Copy the API key (keep it safe!)

### STEP 4 — Setup the Project
Open your terminal/CMD and run these commands one by one:

```bash
# Navigate to your project folder
cd EduAI-Hub

# Create a virtual environment (keeps your project clean)
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Install required libraries
pip install -r requirements.txt
```

### STEP 5 — Add Your API Key
1. Open `app.py` in VS Code
2. Find line: `GEMINI_API_KEY = "YOUR_GEMINI_API_KEY_HERE"`
3. Replace with your actual key: `GEMINI_API_KEY = "AIza...your-key-here"`
4. Save the file (Ctrl+S)

### STEP 6 — Run the Project
```bash
python app.py
```

You should see:
```
 * Running on http://127.0.0.1:5000
 * Debug mode: on
```

### STEP 7 — Open in Browser
Open your browser and go to: **http://localhost:5000**

🎉 Your EduAI Hub is now running!

---

## 🛠️ Features

| Module | Description |
|--------|-------------|
| 🎓 AI Tutor | Ask any tech question, get clear explanations |
| 📝 Quiz Generator | Auto-generate MCQ quizzes on any topic |
| 📄 Resume Analyzer | AI feedback on your resume |
| 💼 Interview Prep | Practice interview Q&A with model answers |
| 📡 Tech News | Latest technology trends & insights |

---

## ❓ Common Issues

**Issue:** `ModuleNotFoundError`
**Fix:** Run `pip install -r requirements.txt` again

**Issue:** `AI Error: Invalid API Key`
**Fix:** Check your API key in app.py. Make sure no spaces around it.

**Issue:** Port already in use
**Fix:** Change `port=5000` to `port=5001` in app.py

**Issue:** PDF not reading correctly
**Fix:** Make sure the PDF has selectable text (not scanned images)

---

## 📊 Technologies Used

- **Python 3.10+** — Backend programming language
- **Flask** — Lightweight web framework
- **Google Gemini 1.5 Flash** — AI model (free tier available)
- **PyPDF2** — PDF text extraction
- **HTML/CSS/JavaScript** — Frontend interface
- **SQLite** (optional) — Can be added for user data storage

---

## 🎯 Future Enhancements (for viva/presentation)

1. Add user login/signup system
2. Save quiz scores and progress history
3. Add speech-to-text for voice questions
4. Add roadmap generator (suggest learning path)
5. Deploy to cloud (Render.com — free hosting)

---

## 👨‍💻 Project Info

- **Project Type:** Final Year Project (IT Department)
- **Tech Stack:** Python, Flask, Google Gemini AI, HTML/CSS/JS
- **Unique Feature:** 5-in-1 AI platform for students AND employees
- **Cost:** FREE (Gemini free tier: 15 requests/min)
