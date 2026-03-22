# 🤖 AI Voice Assistant (Alexa Clone)

👩‍💻 Developed by: **Sanjana Mathe**

A full-stack AI-powered voice assistant that can understand user commands, respond intelligently, and perform real-world actions like opening apps, searching the web, playing music, and more.

---

## 🚀 Features

* 🎤 Voice command recognition (frontend UI + backend processing)
* 🔊 Text-to-speech response using Python
* 🌐 Open websites like YouTube, Google, Netflix, etc.
* 🔍 Smart search functionality
* ⏰ Real-time time & date responses
* 🌦️ Weather information (API-based)
* 🤖 AI-based chat responses (ChatGPT integration ready)
* 🔐 User authentication (Login/Register system)
* 💬 Chat history stored using SQLite database
* 🎮 Interactive UI with categories:

  * Games, OTT, Music, Shopping, Social Media, Education

---

## 🛠️ Tech Stack

### 🔹 Frontend

* HTML, CSS, JavaScript 
* Advanced UI animations & responsive design

### 🔹 Backend

* Python (Flask) 
* REST API for communication

### 🔹 Database

* SQLite (user data + chat history) 

### 🔹 Libraries & Tools

* SpeechRecognition
* pyttsx3 (Text-to-Speech)
* requests (API calls)
* Flask-CORS

---

## 📂 Project Structure

```id="projstr1"
ai-voice-assistant/
 ├── app.py                 # Main backend server
 ├── alexa_server_ai.py     # Voice command processing
 ├── alexa.html             # Frontend UI
 ├── users.db               # Database
 ├── README.md
```

---

## ▶️ How to Run

### 1️⃣ Install Python

Make sure Python 3.10+ is installed

---

### 2️⃣ Install Required Libraries

```id="cmd1"
pip install flask flask-cors pyttsx3 speechrecognition requests
```

---

### 3️⃣ Run Backend Server

```id="cmd2"
python app.py
```

👉 Server runs on:

```
http://localhost:5000
```

---

### 4️⃣ Open Frontend

* Open `alexa.html` in browser
* OR use Live Server in VS Code

---

### 5️⃣ Start Using Assistant 🎤

* Click microphone button
* Speak commands like:

  * “Open YouTube”
  * “Play music”
  * “What is time?”
  * “Search for AI”

---

## 🔑 API Setup (Optional but Powerful)

To enable full features:

* 🌦️ Weather API → OpenWeather
* 🔍 Google Search API
* 🤖 OpenAI API

👉 Add keys inside `app.py`:

```id="api1"
WEATHER_API_KEY = "your_key"
GOOGLE_API_KEY = "your_key"
OPENAI_API_KEY = "your_key"
```

---

## 📸 Demo

👉 Add your screenshot or video here

Example:

```id="img1"
![Demo](demo.png)
```

---

## 💡 Future Improvements

* 🖥️ GUI Desktop App version
* 📱 Mobile app integration
* 🤖 Full AI chatbot integration
* 🌍 Multi-language voice support
* ☁️ Deploy on cloud (Render / Vercel)

---

## 🎯 Project Highlights

* Full-stack project (Frontend + Backend + Database)
* Real-world application (Voice Assistant)
* AI + Automation based system
* Interactive modern UI

---

## ⭐ Conclusion

This project demonstrates how voice-based AI systems can be built using Python and web technologies to create smart, interactive assistants similar to Alexa.

---

👉 If you like this project, give it a ⭐ on GitHub!
