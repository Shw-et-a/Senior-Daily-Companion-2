"""
Task category definitions for Senior Daily Companion.
Each task defines its icon, labels (EN/HI), examples, and AI system context.
"""

TASKS = {
    "travel": {
        "id": "travel",
        "icon": "✈️",
        "tile_key": "task_travel",
        "cat_key": "cat_travel",
        "examples_en": [
            "How do I book a flight online?",
            "Book a train ticket on IRCTC",
            "Find a hotel near me",
            "How to book an Ola or Uber cab?",
        ],
        "examples_hi": [
            "ऑनलाइन उड़ान कैसे बुक करें?",
            "IRCTC पर ट्रेन टिकट बुक करें",
            "नजदीकी होटल खोजें",
            "Ola या Uber कैब कैसे बुक करें?",
        ],
        "system_context": (
            "You are helping a senior citizen (65+) with travel bookings. "
            "Break every task into tiny, numbered steps. Describe every button by its color and position. "
            "Mention which app to use and how to open it. Be patient and warm."
        ),
    },
    "health": {
        "id": "health",
        "icon": "🏥",
        "tile_key": "task_health",
        "cat_key": "cat_health",
        "examples_en": [
            "How do I order medicines online?",
            "Find a doctor near me",
            "Set a medicine reminder on my phone",
            "What does my prescription say?",
        ],
        "examples_hi": [
            "दवाई ऑनलाइन कैसे मंगाएं?",
            "नजदीकी डॉक्टर खोजें",
            "फोन पर दवाई का अनुस्मारक सेट करें",
            "मेरे पर्चे पर क्या लिखा है?",
        ],
        "system_context": (
            "You are helping a senior citizen with health and medicine questions. "
            "ALWAYS add that for medical emergencies they should call 112 immediately. "
            "Do NOT give medical diagnoses or replace professional medical advice. "
            "Be reassuring and calm. Help with apps like Practo, PharmEasy, 1mg."
        ),
    },
    "tech": {
        "id": "tech",
        "icon": "💻",
        "tile_key": "task_tech",
        "cat_key": "cat_tech",
        "examples_en": [
            "My WiFi is not working",
            "TV shows No Signal",
            "How do I video call on WhatsApp?",
            "My phone is running slow",
            "How to take a screenshot?",
        ],
        "examples_hi": [
            "मेरा वाईफाई काम नहीं कर रहा",
            "टीवी पर 'No Signal' आ रहा है",
            "WhatsApp पर वीडियो कॉल कैसे करें?",
            "मेरा फोन धीमा चल रहा है",
            "स्क्रीनशॉट कैसे लें?",
        ],
        "system_context": (
            "You are helping a senior citizen fix a technology problem. "
            "Use EXTREMELY simple language — no technical jargon at all. "
            "Describe buttons, ports, and switches by their color, shape, and exact location on the device. "
            "Go one step at a time. Ask clarifying questions if needed (e.g., 'What brand is your TV?')."
        ),
    },
    "finance": {
        "id": "finance",
        "icon": "💰",
        "tile_key": "task_finance",
        "cat_key": "cat_finance",
        "examples_en": [
            "How do I pay my electricity bill online?",
            "How to check my bank balance?",
            "What is UPI and how do I use it?",
            "How to recharge my phone?",
        ],
        "examples_hi": [
            "बिजली बिल ऑनलाइन कैसे भरें?",
            "अपना बैंक बैलेंस कैसे जांचें?",
            "UPI क्या है और कैसे उपयोग करें?",
            "फोन रिचार्ज कैसे करें?",
        ],
        "system_context": (
            "You are helping a senior citizen with banking and finance tasks. "
            "ALWAYS remind them: never share OTP, PIN, password, or Aadhaar number with anyone — "
            "even if they claim to be from a bank or government. Flag any suspicious request immediately. "
            "Explain UPI, net banking, and bill payments step by step."
        ),
    },
    "shopping": {
        "id": "shopping",
        "icon": "🛒",
        "tile_key": "task_shopping",
        "cat_key": "cat_shopping",
        "examples_en": [
            "How do I order something on Amazon?",
            "How to track my Flipkart order?",
            "How to return a product?",
            "Is this website safe to shop from?",
        ],
        "examples_hi": [
            "Amazon पर ऑर्डर कैसे करें?",
            "Flipkart ऑर्डर कैसे ट्रैक करें?",
            "सामान वापस कैसे करें?",
            "क्या यह वेबसाइट सुरक्षित है?",
        ],
        "system_context": (
            "You are helping a senior citizen with online shopping. "
            "Walk through each step with visuals described clearly. "
            "WARN them about fake shopping websites — only use Amazon, Flipkart, Myntra, Meesho, BigBasket. "
            "Tell them how to spot fake vs. real sites."
        ),
    },
    "govt": {
        "id": "govt",
        "icon": "🏛️",
        "tile_key": "task_govt",
        "cat_key": "cat_govt",
        "examples_en": [
            "How to update my Aadhaar card?",
            "Check my pension status",
            "Apply for a ration card",
            "How to get PF withdrawal?",
            "Apply for senior citizen ID card",
        ],
        "examples_hi": [
            "आधार कार्ड कैसे अपडेट करें?",
            "पेंशन स्थिति कैसे जांचें?",
            "राशन कार्ड के लिए आवेदन करें",
            "PF निकासी कैसे करें?",
            "वरिष्ठ नागरिक पहचान पत्र के लिए आवेदन करें",
        ],
        "system_context": (
            "You are helping a senior citizen navigate Indian government services. "
            "Only mention OFFICIAL websites: uidai.gov.in, epfindia.gov.in, pensioners.gov.in, etc. "
            "Warn them that government officials NEVER ask for OTP or money over phone. "
            "Be patient with complex bureaucratic processes — simplify everything."
        ),
    },
    "emergency": {
        "id": "emergency",
        "icon": "📞",
        "tile_key": "task_emergency",
        "cat_key": "cat_emergency",
        "examples_en": [
            "I think I'm being scammed",
            "Someone is asking me for OTP",
            "Is this a real call from my bank?",
            "I need help right now",
        ],
        "examples_hi": [
            "मुझे लगता है मेरे साथ धोखा हो रहा है",
            "कोई मुझसे OTP मांग रहा है",
            "क्या यह मेरे बैंक का असली कॉल है?",
            "मुझे अभी मदद चाहिए",
        ],
        "system_context": (
            "You are a safety advisor for a senior citizen. "
            "If there is ANY sign of a scam (requests for OTP, money, gift cards, remote access, "
            "urgency, threats), IMMEDIATELY output is_scam_warning=true and tell them to STOP and call 1930. "
            "For health emergencies: call 112. For police: call 100. Be calm but very clear and urgent."
        ),
    },
    "wellness": {
        "id": "wellness",
        "icon": "🧘",
        "tile_key": "task_wellness",
        "cat_key": "cat_wellness",
        "examples_en": [
            "Suggest a healthy breakfast for seniors",
            "Easy exercises I can do at home",
            "How to video call my grandchildren?",
            "Suggest a hobby for my free time",
            "I feel lonely — what can I do?",
        ],
        "examples_hi": [
            "बुजुर्गों के लिए स्वस्थ नाश्ते का सुझाव दें",
            "घर पर आसान व्यायाम बताएं",
            "अपने पोते-पोतियों को वीडियो कॉल कैसे करें?",
            "खाली समय में कोई शौक बताएं",
            "मुझे अकेलापन लगता है — क्या करूँ?",
        ],
        "system_context": (
            "You are a warm wellness companion for a senior citizen. "
            "Be genuinely empathetic, warm, and encouraging. "
            "Suggest activities that are safe and appropriate for 65+ age group. "
            "If they express loneliness or sadness, respond with great compassion and practical suggestions."
        ),
    },
}

TASK_ORDER = ["travel", "health", "tech", "finance", "shopping", "govt", "emergency", "wellness"]
