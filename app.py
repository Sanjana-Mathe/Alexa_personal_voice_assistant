# assistant_server.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import pyttsx3, pywhatkit, wikipedia, pyjokes, datetime, os, webbrowser
import threading

app = Flask(__name__)
CORS(app)

# Initialize TTS engine
engine = pyttsx3.init()
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[1].id if len(voices) > 1 else voices[0].id)

# Lock to prevent concurrent TTS
tts_lock = threading.Lock()

def talk(text):
    """Speak and print text safely."""
    print("Alexa:", text)
    # Run TTS in a separate thread to prevent blocking
    def speak():
        with tts_lock:
            engine.say(text)
            engine.runAndWait()
    threading.Thread(target=speak).start()

def handle_command(cmd: str):
    cmd = cmd.lower().strip()
    if cmd.startswith("alexa"):
        cmd = cmd.replace("alexa", "", 1).strip()

    # 🎵 Play music on YouTube
    if cmd.startswith("play") or "play music" in cmd:
        song = cmd.replace("play music", "").replace("play", "").strip()
        talk("Playing " + song)
        pywhatkit.playonyt(song)
        return f"Playing {song}"

    # 🔍 Google search
    elif cmd.startswith("search"):
        query = cmd.replace("search", "", 1).strip()
        talk("Searching for " + query)
        webbrowser.open(f"https://www.google.com/search?q={query}")
        return f"Searching for {query}"

    # ⏰ Current time
    elif "time" in cmd:
        now = datetime.datetime.now().strftime("%H:%M")
        talk("Current time is " + now)
        return f"Current time is {now}"

    # 🌟 Wikipedia info
    elif "superstar" in cmd:
        person = cmd.replace("superstar", "", 1).strip()
        try:
            info = wikipedia.summary(person, sentences=2)
            talk(info)
            return info
        except Exception:
            return f"Could not find info about {person}"

    # 😂 Joke
    elif "joke" in cmd:
        joke = pyjokes.get_joke()
        talk(joke)
        return joke

    # 💻 System apps
    elif "vs code" in cmd:
        talk("Opening VS Code")
        os.system("code")
        return "Opening VS Code"
    elif "chrome" in cmd:
        talk("Opening Chrome")
        os.system('start "" "chrome"')
        return "Opening Chrome"
    elif "file manager" in cmd or "explorer" in cmd:
        talk("Opening File Manager")
        os.system("explorer")
        return "Opening File Manager"
    elif "calculator" in cmd:
        talk("Opening Calculator")
        os.system("calc")
        return "Opening Calculator"
    elif "notepad" in cmd:
        talk("Opening Notepad")
        os.system("notepad")
        return "Opening Notepad"

    # 🔌 Shutdown
    elif "shutdown" in cmd:
        talk("Shutting down in 5 seconds")
        os.system("shutdown /s /t 5")
        return "Shutting down in 5 seconds"

    # 🌐 Websites (OTT, Shopping, Education, Social)
    websites = {
        # OTT Platforms
        "netflix": "https://www.netflix.com/",
        "prime video": "https://www.primevideo.com/",
        "disney plus": "https://www.disneyplus.com/",
        "hotstar": "https://www.hotstar.com/",
        "zee5": "https://www.zee5.com/",
        # Shopping / E-commerce
        "blinkit": "https://blinkit.com/",
        "amazon": "https://www.amazon.in/",
        "flipkart": "https://www.flipkart.com/",
        "myntra": "https://www.myntra.com/",
        "snapdeal": "https://www.snapdeal.com/",
        # Electronics
        "electronics": "https://www.croma.com/",
        # Education
        "edx": "https://www.edx.org/",
        "coursera": "https://www.coursera.org/",
        "udemy": "https://www.udemy.com/",
        "khan academy": "https://www.khanacademy.org/",
        # Social / AI
        "instagram": "https://www.instagram.com/",
        "facebook": "https://www.facebook.com/",
        "chatgpt": "https://chat.openai.com/",
        "gemini": "https://gemini.google.com/"
    }

    for key, url in websites.items():
        if key in cmd:
            talk(f"Opening {key.title()}")
            webbrowser.open(url)
            return f"Opening {key.title()}"

    # ❌ Exit
    if cmd in ("exit", "quit"):
        talk("Goodbye!")
        return "Goodbye!"

    else:
        talk("Sorry, I didn't understand that.")
        return "Sorry, I didn't understand that."

# API Endpoint
@app.route("/command", methods=["POST"])
def command():
    data = request.get_json()
    cmd = data.get("command", "")
    reply = handle_command(cmd)
    return jsonify({"reply": reply})

if __name__ == "__main__":
    print("🚀 Alexa Server running at http://localhost:5005")
    app.run(port=5005)
