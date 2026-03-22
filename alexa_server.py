from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import hashlib
import datetime
import random
import re
import requests
import os

app = Flask(__name__)
CORS(app)

# =========================== API KEYS ===========================
# Get your free API keys from:
# Weather: https://openweathermap.org/api
# Google Search: https://developers.google.com/custom-search/v1/overview
# ChatGPT: https://platform.openai.com/api-keys

WEATHER_API_KEY = "YOUR_OPENWEATHER_API_KEY"
GOOGLE_API_KEY = "YOUR_GOOGLE_API_KEY"
GOOGLE_SEARCH_ENGINE_ID = "YOUR_GOOGLE_SEARCH_ENGINE_ID"
OPENAI_API_KEY = "YOUR_OPENAI_API_KEY"

# =========================== DATABASE SETUP ===========================
def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    
    # Users table
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Chats table
    c.execute('''
        CREATE TABLE IF NOT EXISTS chats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            message TEXT,
            sender TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    ''')
    
    # Favorites table
    c.execute('''
        CREATE TABLE IF NOT EXISTS favorites (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            app_name TEXT,
            app_url TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    ''')
    
    # Voice commands table
    c.execute('''
        CREATE TABLE IF NOT EXISTS voice_commands (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            command TEXT,
            response TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    ''')
    
    conn.commit()
    conn.close()
    print("✅ Database initialized successfully!")

init_db()

# =========================== USER AUTHENTICATION ===========================
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username', '').strip()
    password = data.get('password', '').strip()
    
    if not username or not password:
        return jsonify({'message': 'Username and password required'}), 400
    
    if len(password) < 6:
        return jsonify({'message': 'Password must be at least 6 characters'}), 400
    
    hashed_pw = hashlib.sha256(password.encode()).hexdigest()
    
    try:
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_pw))
        conn.commit()
        conn.close()
        return jsonify({'message': 'Registration successful! You can now login.'})
    except sqlite3.IntegrityError:
        return jsonify({'message': 'Username already exists. Please choose another.'}), 400
    except Exception as e:
        return jsonify({'message': f'Registration error: {str(e)}'}), 500

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username', '').strip()
    password = data.get('password', '').strip()
    
    if not username or not password:
        return jsonify({'message': 'Username and password required'}), 400
    
    hashed_pw = hashlib.sha256(password.encode()).hexdigest()
    
    try:
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("SELECT id, username FROM users WHERE username=? AND password=?", (username, hashed_pw))
        user = c.fetchone()
        conn.close()
        
        if user:
            return jsonify({
                'message': 'Login successful',
                'user_id': user[0],
                'username': user[1]
            })
        return jsonify({'message': 'Invalid username or password'}), 401
    except Exception as e:
        return jsonify({'message': f'Login error: {str(e)}'}), 500

# =========================== AI CHAT WITH OPENAI ===========================
@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_id = data.get('user_id')
    msg = data.get('message', '').strip()
    
    if not msg:
        return jsonify({'reply': 'Please say something!'}), 400
    
    # Process command and get response
    reply, action = process_smart_command(msg)
    
    # Save to database
    if user_id:
        try:
            conn = sqlite3.connect('users.db')
            c = conn.cursor()
            c.execute("INSERT INTO chats(user_id, message, sender) VALUES (?, ?, ?)", (user_id, msg, 'user'))
            c.execute("INSERT INTO chats(user_id, message, sender) VALUES (?, ?, ?)", (user_id, reply, 'bot'))
            c.execute("INSERT INTO voice_commands(user_id, command, response) VALUES (?, ?, ?)", (user_id, msg, reply))
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Database error: {e}")
    
    response = {'reply': reply}
    if action:
        response['action'] = action
    
    return jsonify(response)

# =========================== SMART COMMAND PROCESSING ===========================
def process_smart_command(msg):
    """Process voice and text commands with AI integration"""
    msg_lower = msg.lower()
    action = None
    
    # Greetings
    if any(word in msg_lower for word in ['hello', 'hi', 'hey', 'greetings', 'good morning', 'good evening']):
        greetings = [
            "Hello! Welcome to Alexa. How can I assist you today?",
            "Hi there! Alexa here. What would you like to know?",
            "Greetings! I'm Alexa, your AI assistant. Ask me anything!",
            f"Hey! Alexa at your service. What do you need?"
        ]
        return random.choice(greetings), None
    
    # Time & Date
    if 'time' in msg_lower and 'what' in msg_lower:
        return f"⏰ The current time is {datetime.datetime.now().strftime('%I:%M %p')}", None
    
    if any(word in msg_lower for word in ['date', 'today', "what's today"]):
        return f"📅 Today is {datetime.datetime.now().strftime('%A, %B %d, %Y')}", None
    
    # Play Music/Videos
    if 'play' in msg_lower and ('song' in msg_lower or 'music' in msg_lower or 'video' in msg_lower):
        song_name = msg.replace('play', '').replace('song', '').replace('music', '').replace('video', '').strip()
        if song_name:
            url = f"https://www.youtube.com/results?search_query={song_name.replace(' ', '+')}"
            action = {'type': 'open_url', 'url': url}
            return f"🎵 Alexa says: Playing '{song_name}' on YouTube for you", action
        else:
            action = {'type': 'open_url', 'url': 'https://music.youtube.com/'}
            return "🎵 Alexa says: Opening YouTube Music", action
        # Google Search - Always open in browser
    if any(word in msg_lower for word in ['search', 'find', 'look for', 'google']):
        query = msg_lower.replace('search', '').replace('find', '').replace('look for', '')
        query = query.replace('on google', '').replace('google', '').replace('for', '').strip()
        if query:
            # Directly open Google search results
            url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
            action = {'type': 'open_url', 'url': url}
            return f"🔍 Alexa says: Searching for '{query}' on Google", action
        else:
            action = {'type': 'open_url', 'url': 'https://www.google.com/'}
            return "🔍 Alexa says: Opening Google", action
    
    # App Opening Commands
    app_commands = {
        'netflix': ('https://www.netflix.com/', '🎬 Alexa says: Opening Netflix for you'),
        'youtube': ('https://www.youtube.com/', '📺 Alexa says: Opening YouTube'),
        'spotify': ('https://www.spotify.com/', '🎵 Alexa says: Opening Spotify'),
        'amazon': ('https://www.amazon.in/', '🛍️ Alexa says: Opening Amazon'),
        'flipkart': ('https://www.flipkart.com/', '🛍️ Alexa says: Opening Flipkart'),
        'facebook': ('https://www.facebook.com/', '📱 Alexa says: Opening Facebook'),
        'instagram': ('https://www.instagram.com/', '📸 Alexa says: Opening Instagram'),
        'twitter': ('https://twitter.com/', '🐦 Alexa says: Opening Twitter'),
        'whatsapp': ('https://web.whatsapp.com/', '💬 Alexa says: Opening WhatsApp Web'),
        'gmail': ('https://mail.google.com/', '📧 Alexa says: Opening Gmail'),
        'google': ('https://www.google.com/', '🔍 Alexa says: Opening Google'),
        'maps': ('https://www.google.com/maps', '🗺️ Alexa says: Opening Google Maps'),
        'news': ('https://www.ndtv.com/', '📰 Alexa says: Opening News'),
        'zomato': ('https://www.zomato.com/', '🍔 Alexa says: Opening Zomato'),
        'swiggy': ('https://www.swiggy.com/', '🍕 Alexa says: Opening Swiggy'),
        'hotstar': ('https://www.hotstar.com/', '🎬 Alexa says: Opening Disney+ Hotstar'),
        'prime': ('https://www.primevideo.com/', '🎬 Alexa says: Opening Prime Video'),
        'linkedin': ('https://www.linkedin.com/', '💼 Alexa says: Opening LinkedIn'),
        'github': ('https://www.github.com/', '💻 Alexa says: Opening GitHub'),
        'calculator': ('https://www.google.com/search?q=calculator', '🔢 Alexa says: Opening Calculator'),
        'calendar': ('https://calendar.google.com/', '📅 Alexa says: Opening Calendar'),
        'chess': ('https://www.chess.com/', '♟️ Alexa says: Opening Chess.com'),
        'pubg': ('https://www.battlegrounds.com/', '🎮 Alexa says: Opening PUBG'),
        'freefire': ('https://ff.garena.com/', '🔥 Alexa says: Opening Free Fire'),
        'ludo': ('https://www.ludoking.com/', '🎲 Alexa says: Opening Ludo King'),
        'myntra': ('https://www.myntra.com/', '👗 Alexa says: Opening Myntra'),
        'ajio': ('https://www.ajio.com/', '🛍️ Alexa says: Opening Ajio'),
        'zee5': ('https://www.zee5.com/', '📺 Alexa says: Opening ZEE5'),
        'sonyliv': ('https://www.sonyliv.com/', '📺 Alexa says: Opening SonyLIV'),
        'jiocinema': ('https://www.jiocinema.com/', '🎬 Alexa says: Opening JioCinema'),
        'gaana': ('https://www.gaana.com/', '🎵 Alexa says: Opening Gaana'),
        'jiosaavn': ('https://www.jiosaavn.com/', '🎵 Alexa says: Opening JioSaavn'),
        'snapdeal': ('https://www.snapdeal.com/', '🛍️ Alexa says: Opening Snapdeal'),
        'dominos': ('https://www.dominos.co.in/', '🍕 Alexa says: Opening Domino\'s'),
        'mcdonalds': ('https://www.mcdelivery.co.in/', '🍔 Alexa says: Opening McDonald\'s'),
        'blinkit': ('https://blinkit.com/', '🛒 Alexa says: Opening Blinkit'),
        'bigbasket': ('https://www.bigbasket.com/', '🛒 Alexa says: Opening BigBasket'),
    }
    
    for app, (url, message) in app_commands.items():
        if any(trigger in msg_lower for trigger in [f'open {app}', f'launch {app}', f'start {app}', f'show me {app}', app]):
            action = {'type': 'open_url', 'url': url}
            return message, action
    
    # Google Search
    if any(word in msg_lower for word in ['search', 'find', 'look for', 'google']):
        query = msg_lower.replace('search', '').replace('find', '').replace('look for', '')
        query = query.replace('on google', '').replace('google', '').replace('for', '').strip()
        if query:
            # Use Google Custom Search API
            search_result = google_search(query)
            if search_result:
                return f"Alexa says: {search_result}", None
            # Fallback to opening Google
            url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
            action = {'type': 'open_url', 'url': url}
            return f"🔍 Alexa says: Searching for '{query}' on Google", action
    
    # Weather
    if 'weather' in msg_lower:
        city = extract_city_name(msg)
        if city:
            weather_info = get_weather(city)
            return f"Alexa says: {weather_info}", None
        return "Alexa says: Which city's weather would you like to know?", None
    
    # Math Operations
    if any(op in msg_lower for op in ['+', '-', '*', '/', 'calculate', 'plus', 'minus', 'times', 'divided', 'multiply']):
        result = handle_math(msg)
        return f"Alexa says: {result}", None
    
    # Jokes
    if 'joke' in msg_lower or 'funny' in msg_lower:
        jokes = [
            "Why don't programmers like nature? Too many bugs! 🐛",
            "Why do Java developers wear glasses? Because they can't C#! 👓",
            "How many programmers does it take to change a light bulb? None, that's a hardware problem! 💡",
            "Why did the developer go broke? Because he used up all his cache! 💰",
            "What's a programmer's favorite place? The Foo Bar! 🍺",
            "Why do programmers prefer dark mode? Because light attracts bugs! 🌙"
        ]
        return f"Alexa says: {random.choice(jokes)}", None
    
    # Help Command
    if 'help' in msg_lower or 'what can you do' in msg_lower:
        return """🤖 Alexa says: I can help you with:

🎵 Play music: "play [song name]"
📱 Open apps: "open [app name]"  
🔍 Search: "search for [query]"
🌤️ Weather: "weather in [city]"
⏰ Time: "what's the time"
📅 Date: "what's the date"
🔢 Math: "calculate 5 + 3"
😂 Jokes: "tell me a joke"
❓ Questions: Ask me anything!

I use AI to answer your questions!""", None
    
    # Use ChatGPT for general questions
    if '?' in msg or any(word in msg_lower for word in ['what', 'who', 'where', 'when', 'why', 'how', 'tell me', 'explain']):
        ai_response = get_chatgpt_response(msg)
        if ai_response:
            return f"Alexa says: {ai_response}", None
    
    # Default response
    return f"Alexa says: I heard '{msg}'. Try asking questions or say 'help' to see what I can do!", None

# =========================== GOOGLE SEARCH API ===========================
def google_search(query):
    """Search using Google Custom Search API"""
    if GOOGLE_API_KEY == "YOUR_GOOGLE_API_KEY":
        return None
    
    try:
        url = f"https://www.googleapis.com/customsearch/v1?key={GOOGLE_API_KEY}&cx={GOOGLE_SEARCH_ENGINE_ID}&q={query}"
        response = requests.get(url, timeout=5)
        data = response.json()
        
        if 'items' in data and len(data['items']) > 0:
            result = data['items'][0]
            title = result.get('title', '')
            snippet = result.get('snippet', '')
            return f"📌 {title}\n{snippet}"
        return None
    except Exception as e:
        print(f"Google Search error: {e}")
        return None

# =========================== CHATGPT API ===========================
def get_chatgpt_response(question):
    """Get AI response from ChatGPT"""
    if OPENAI_API_KEY == "YOUR_OPENAI_API_KEY":
        fallback_responses = {
            "who are you": "I'm Alexa, your AI voice assistant created to help you with various tasks!",
            "what is your name": "My name is Alexa, your personal AI assistant!",
            "how are you": "I'm doing great! Thanks for asking. How can I help you today?",
            "what can you do": "I can open apps, play music, search the web, tell jokes, and answer your questions!",
        }
        
        for key, response in fallback_responses.items():
            if key in question.lower():
                return response
        
        return "I'm Alexa! I can help you with many things. Try asking me to open apps, play music, or search for information!"
    
    try:
        headers = {
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {"role": "system", "content": "You are Alexa, a helpful AI voice assistant. Keep responses concise and friendly."},
                {"role": "user", "content": question}
            ],
            "max_tokens": 150,
            "temperature": 0.7
        }
        
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            json=data,
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            return result['choices'][0]['message']['content'].strip()
        else:
            print(f"ChatGPT API error: {response.status_code}")
            return None
    except Exception as e:
        print(f"ChatGPT error: {e}")
        return None

# =========================== WEATHER API ===========================
def extract_city_name(text):
    """Extract city name from text"""
    text = text.lower()
    cities = ['mumbai', 'delhi', 'bangalore', 'chennai', 'kolkata', 'hyderabad', 
              'pune', 'ahmedabad', 'jaipur', 'lucknow', 'kanpur', 'nagpur',
              'indore', 'bhopal', 'patna', 'vadodara', 'ghaziabad', 'ludhiana']
    
    for city in cities:
        if city in text:
            return city.capitalize()
    
    # Try to extract any word after "in" or "for"
    words = text.split()
    for i, word in enumerate(words):
        if word in ['in', 'for', 'at'] and i + 1 < len(words):
            return words[i + 1].capitalize()
    
    return None

def get_weather(city):
    """Get weather information for a city"""
    if WEATHER_API_KEY == "YOUR_OPENWEATHER_API_KEY":
        return f"Weather API not configured. Visit https://openweathermap.org/api to get a free API key!"
    
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"
        response = requests.get(url, timeout=5)
        data = response.json()
        
        if response.status_code == 200:
            temp = data['main']['temp']
            desc = data['weather'][0]['description']
            humidity = data['main']['humidity']
            return f"🌤️ Weather in {city}:\n🌡️ Temperature: {temp}°C\n☁️ Condition: {desc}\n💧 Humidity: {humidity}%"
        else:
            return f"Sorry, I couldn't find weather information for {city}"
    except Exception as e:
        print(f"Weather API error: {e}")
        return "Weather service temporarily unavailable"

@app.route('/weather/india', methods=['GET'])
def get_india_weather():
    """Get weather for major Indian cities"""
    cities = ['Mumbai', 'Delhi', 'Bangalore', 'Chennai', 'Kolkata', 'Hyderabad', 
              'Pune', 'Ahmedabad', 'Jaipur', 'Lucknow']
    
    if WEATHER_API_KEY == "YOUR_OPENWEATHER_API_KEY":
        return jsonify({'error': 'Weather API not configured'}), 400
    
    weather_data = []
    
    for city in cities:
        try:
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"
            response = requests.get(url, timeout=3)
            data = response.json()
            
            if response.status_code == 200:
                weather_data.append({
                    'city': city,
                    'temp': round(data['main']['temp']),
                    'description': data['weather'][0]['description'].title(),
                    'humidity': data['main']['humidity']
                })
        except Exception as e:
            print(f"Error fetching weather for {city}: {e}")
    
    if weather_data:
        return jsonify(weather_data)
    else:
        return jsonify({'error': 'Unable to fetch weather data'}), 500

# =========================== MATH OPERATIONS ===========================
def handle_math(expression):
    """Handle mathematical calculations"""
    try:
        # Extract numbers and operators
        expression = expression.lower()
        expression = expression.replace('calculate', '').replace('what is', '').replace('what\'s', '')
        expression = expression.replace('plus', '+').replace('minus', '-')
        expression = expression.replace('times', '*').replace('multiply', '*').replace('multiplied by', '*')
        expression = expression.replace('divided by', '/').replace('divide', '/')
        expression = expression.strip()
        
        # Evaluate safely
        result = eval(expression, {"__builtins__": {}}, {})
        return f"🔢 The answer is: {result}"
    except Exception as e:
        return "Sorry, I couldn't calculate that. Try something like 'calculate 5 + 3'"

# =========================== RUN SERVER ===========================
if __name__ == '__main__':
    print("\n" + "="*60)
    print("🤖 ALEXA VOICE ASSISTANT BACKEND")
    print("="*60)
    print("✅ Server starting on http://localhost:5000")
    print("📝 Database initialized")
    print("\n🔑 API Configuration:")
    print(f"   Weather API: {'✅ Configured' if WEATHER_API_KEY != 'YOUR_OPENWEATHER_API_KEY' else '❌ Not configured'}")
    print(f"   Google Search: {'✅ Configured' if GOOGLE_API_KEY != 'YOUR_GOOGLE_API_KEY' else '❌ Not configured'}")
    print(f"   ChatGPT: {'✅ Configured' if OPENAI_API_KEY != 'YOUR_OPENAI_API_KEY' else '❌ Not configured'}")
    print("\n💡 Get free API keys:")
    print("   Weather: https://openweathermap.org/api")
    print("   Google: https://developers.google.com/custom-search")
    print("   ChatGPT: https://platform.openai.com/api-keys")
    print("\n" + "="*60 + "\n")
    
    app.run(debug=True, port=5000, host='0.0.0.0')
