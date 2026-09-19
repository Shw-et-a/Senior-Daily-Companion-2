"""
Senior Daily Companion — Main Application
A Gen AI-powered, senior-first daily companion website.
"""

import os
import json
import re
from datetime import datetime
import pytz
from dotenv import load_dotenv
import streamlit as st
import streamlit.components.v1 as components
from google import genai
from google.genai import types

load_dotenv()


# ============================================================
# TRANSLATIONS
# ============================================================
TRANSLATIONS = {
    "en": {
        # App-level
        "app_title": "Senior Daily Companion",
        "app_tagline": "Your trusted helper — every single day",

        # Greetings
        "greeting_morning": "Good Morning! 🌅",
        "greeting_afternoon": "Good Afternoon! ☀️",
        "greeting_evening": "Good Evening! 🌙",
        "greeting_night": "Good Night! 🌛",
        "greeting_subtitle": "I'm here to help you with anything you need.",
        "todays_date": "Today is",

        # Dashboard cards
        "daily_tip_title": "💡 Helpful Tip For Today",
        "scam_alert_title": "⚠️ Today's Scam Warning",

        # Accessibility bar
        "language_label": "Language",
        "font_label": "Text Size",
        "font_normal": "A",
        "font_large": "A+",
        "font_xlarge": "A++",
        "contrast_label": "🌙 High Contrast",
        "sos_button": "🆘  SOS",

        # Quick help section
        "quick_help_title": "How Can I Help You Today?",
        "quick_help_subtitle": "Tap any tile below to get started",

        # Task categories
        "task_travel":    "✈️ Travel &\nBooking",
        "task_health":    "🏥 Health &\nMedicine",
        "task_tech":      "💻 Tech\nHelp",
        "task_finance":   "💰 Finance &\nBanking",
        "task_shopping":  "🛒 Shopping",
        "task_govt":      "🏛️ Government\nServices",
        "task_emergency": "📞 Emergency\n& Safety",
        "task_wellness":  "🧘 Wellness &\nDaily Life",

        # Chat panel
        "chat_title": "💬 Let's Talk",
        "chat_welcome": "Hello! I'm your Daily Companion 😊\n\nTap any tile above to get started, or type your question below. I'll guide you step by step — slowly and clearly.",
        "chat_placeholder": "Type your question here…",
        "ask_button": "🤖  Get Help",
        "voice_btn": "🎤  Speak",
        "thinking": "⏳ Finding the best answer for you…",
        "you_label": "You",
        "assistant_label": "Your Companion",

        # Response actions
        "read_aloud": "🔊  Read Aloud",
        "explain_simpler": "🔄  Explain More Simply",
        "next_step": "👉  Next Step",
        "suggestions_title": "You might also want to ask:",
        "step_prefix": "Step",
        "visual_cue_label": "👁️ Look for:",
        "encouragement_label": "💪",

        # Scam warning
        "scam_banner": "⛔  SCAM ALERT — This looks suspicious!",
        "scam_detail": "Do NOT share money, OTPs, passwords, or any personal information. Hang up or close the message immediately.",
        "scam_helpline": "Call the Cybercrime Helpline: 1930",

        # Emergency panel
        "emergency_title": "🆘 Emergency Help",
        "emergency_subtitle": "Tap a number to call immediately",
        "emergency_ambulance": "🚑  Ambulance — 108",
        "emergency_police": "🚔  Police — 100",
        "emergency_fire": "🚒  Fire — 101",
        "emergency_helpline": "📞  Senior Helpline — 14567",
        "emergency_cyber": "🛡️  Cyber Crime — 1930",
        "emergency_close": "Close",
        "emergency_note": "In any emergency, call 112 — it works everywhere in India.",

        # Category labels (for display)
        "cat_travel": "Travel & Booking",
        "cat_health": "Health & Medicine",
        "cat_tech": "Tech Help",
        "cat_finance": "Finance & Banking",
        "cat_shopping": "Shopping",
        "cat_govt": "Government Services",
        "cat_emergency": "Emergency & Safety",
        "cat_wellness": "Wellness & Daily Life",
        "cat_general": "General Help",

        # Footer
        "footer": "Senior Daily Companion • Powered by Google Gemini AI • Always here for you ❤️",
    },

    "hi": {
        # App-level
        "app_title": "वरिष्ठ दैनिक सहायक",
        "app_tagline": "आपका विश्वसनीय सहायक — हर दिन",

        # Greetings
        "greeting_morning": "सुप्रभात! 🌅",
        "greeting_afternoon": "शुभ दोपहर! ☀️",
        "greeting_evening": "शुभ संध्या! 🌙",
        "greeting_night": "शुभ रात्रि! 🌛",
        "greeting_subtitle": "मैं यहाँ आपकी हर जरूरत में मदद के लिए हूँ।",
        "todays_date": "आज की तारीख",

        # Dashboard cards
        "daily_tip_title": "💡 आज का उपयोगी सुझाव",
        "scam_alert_title": "⚠️ आज की धोखाधड़ी चेतावनी",

        # Accessibility bar
        "language_label": "भाषा",
        "font_label": "अक्षर का आकार",
        "font_normal": "अ",
        "font_large": "अ+",
        "font_xlarge": "अ++",
        "contrast_label": "🌙 हाई कंट्रास्ट",
        "sos_button": "🆘  आपातकाल",

        # Quick help section
        "quick_help_title": "आज मैं आपकी कैसे मदद करूँ?",
        "quick_help_subtitle": "शुरू करने के लिए नीचे कोई भी विकल्प चुनें",

        # Task categories
        "task_travel":    "✈️ यात्रा और\nबुकिंग",
        "task_health":    "🏥 स्वास्थ्य और\nदवाई",
        "task_tech":      "💻 तकनीकी\nसहायता",
        "task_finance":   "💰 वित्त और\nबैंकिंग",
        "task_shopping":  "🛒 खरीदारी",
        "task_govt":      "🏛️ सरकारी\nसेवाएं",
        "task_emergency": "📞 आपातकाल\nऔर सुरक्षा",
        "task_wellness":  "🧘 स्वास्थ्य\nदैनिक जीवन",

        # Chat panel
        "chat_title": "💬 बात करें",
        "chat_welcome": "नमस्ते! मैं आपका दैनिक सहायक हूँ 😊\n\nऊपर कोई भी विकल्प चुनें या नीचे अपना प्रश्न टाइप करें। मैं आपको धीरे-धीरे और साफ तरीके से हर कदम बताऊँगा।",
        "chat_placeholder": "यहाँ अपना प्रश्न लिखें…",
        "ask_button": "🤖  मदद लें",
        "voice_btn": "🎤  बोलें",
        "thinking": "⏳ आपके लिए सबसे अच्छा जवाब ढूंढ रहा हूँ…",
        "you_label": "आप",
        "assistant_label": "आपका सहायक",

        # Response actions
        "read_aloud": "🔊  जोर से पढ़ें",
        "explain_simpler": "🔄  और आसान भाषा में बताएं",
        "next_step": "👉  अगला कदम",
        "suggestions_title": "आप यह भी पूछ सकते हैं:",
        "step_prefix": "चरण",
        "visual_cue_label": "👁️ इसे देखें:",
        "encouragement_label": "💪",

        # Scam warning
        "scam_banner": "⛔  धोखाधड़ी की चेतावनी — यह संदिग्ध है!",
        "scam_detail": "पैसे, OTP, पासवर्ड या कोई भी व्यक्तिगत जानकारी साझा न करें। तुरंत फोन काटें या संदेश बंद करें।",
        "scam_helpline": "साइबर क्राइम हेल्पलाइन पर कॉल करें: 1930",

        # Emergency panel
        "emergency_title": "🆘 आपातकालीन सहायता",
        "emergency_subtitle": "तुरंत कॉल करने के लिए नंबर चुनें",
        "emergency_ambulance": "🚑  एम्बुलेंस — 108",
        "emergency_police": "🚔  पुलिस — 100",
        "emergency_fire": "🚒  दमकल — 101",
        "emergency_helpline": "📞  वरिष्ठ नागरिक हेल्पलाइन — 14567",
        "emergency_cyber": "🛡️  साइबर क्राइम — 1930",
        "emergency_close": "बंद करें",
        "emergency_note": "किसी भी आपातकाल में 112 पर कॉल करें — यह पूरे भारत में काम करता है।",

        # Category labels
        "cat_travel": "यात्रा और बुकिंग",
        "cat_health": "स्वास्थ्य और दवाई",
        "cat_tech": "तकनीकी सहायता",
        "cat_finance": "वित्त और बैंकिंग",
        "cat_shopping": "खरीदारी",
        "cat_govt": "सरकारी सेवाएं",
        "cat_emergency": "आपातकाल और सुरक्षा",
        "cat_wellness": "स्वास्थ्य और दैनिक जीवन",
        "cat_general": "सामान्य सहायता",

        # Footer
        "footer": "वरिष्ठ दैनिक सहायक • Google Gemini AI द्वारा संचालित • हमेशा आपके साथ ❤️",
    },
}

# ============================================================
# TASKS
# ============================================================
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

# ============================================================
# VOICE HELPERS
# ============================================================
# ─── Text-to-Speech ───────────────────────────────────────────────────────────
def render_read_aloud(text: str, language: str = "en", button_label: str = "🔊  Read Aloud"):
    """
    Render a 'Read Aloud' button that speaks the given text using the browser's
    Web Speech API at a senior-friendly pace.
    """
    lang_code = "hi-IN" if language == "hi" else "en-IN"

    # Sanitize text for JS string embedding
    safe = (
        text.replace("\\", "\\\\")
            .replace('"', '\\"')
            .replace("\n", " ")
            .replace("\r", "")
            .replace("'", "\\'")
    )

    components.html(
        f"""
        <button
            onclick="speakText()"
            style="
                font-family: 'Nunito', Arial, sans-serif;
                font-size: 18px;
                font-weight: 700;
                padding: 14px 22px;
                background-color: #1A5276;
                color: white;
                border: none;
                border-radius: 12px;
                cursor: pointer;
                width: 100%;
                transition: background 0.2s;
            "
            onmouseover="this.style.backgroundColor='#2E86AB'"
            onmouseout="this.style.backgroundColor='#1A5276'"
        >
            {button_label}
        </button>
        <script>
        function speakText() {{
            if (!window.speechSynthesis) {{
                alert('Your browser does not support text-to-speech. Please try Chrome or Edge.');
                return;
            }}
            window.speechSynthesis.cancel();
            var utterance = new SpeechSynthesisUtterance("{safe}");
            utterance.lang = "{lang_code}";
            utterance.rate = 0.82;
            utterance.pitch = 1.0;
            utterance.volume = 1.0;
            window.speechSynthesis.speak(utterance);
        }}
        </script>
        """,
        height=62,
    )


# ─── Speech-to-Text ───────────────────────────────────────────────────────────
def render_voice_input(language: str = "en"):
    """
    Render a voice input widget. Recognized text is passed back to Streamlit
    via URL query param '?voice_input=...' which triggers a page re-run.
    Works in Chrome / Edge (Web Speech API required).
    """
    lang_code = "hi-IN" if language == "hi" else "en-IN"

    listening_text = "सुन रहा हूँ… बोलें" if language == "hi" else "Listening… speak now"
    error_text     = "माफ करें, समझ नहीं आया। फिर कोशिश करें।" if language == "hi" else "Sorry, didn't catch that. Please try again."
    no_support     = "आपका ब्राउज़र वॉइस इनपुट को सपोर्ट नहीं करता।" if language == "hi" else "Your browser doesn't support voice input. Please use Chrome or Edge."
    use_text_label = "✓  इस्तेमाल करें" if language == "hi" else "✓  Use This"
    mic_label      = "🎤  बोलें" if language == "hi" else "🎤  Speak"

    components.html(
        f"""
        <div style="font-family:'Nunito',Arial,sans-serif;">
            <button id="micBtn"
                onclick="startVoice()"
                style="
                    font-size: 18px; font-weight: 700;
                    padding: 14px 22px;
                    background-color: #27AE60;
                    color: white; border: none;
                    border-radius: 12px; cursor: pointer;
                    width: 100%; transition: background 0.2s;
                "
                onmouseover="this.style.backgroundColor='#1E8449'"
                onmouseout="this.style.backgroundColor='#27AE60'"
            >{mic_label}</button>

            <p id="statusMsg" style="margin:8px 0 4px; font-size:16px; color:#7F8C8D;"></p>

            <div id="resultBox" style="display:none; margin-top:8px;">
                <p id="resultText"
                   style="font-size:18px; font-weight:700; color:#1A5276;
                          background:#D6EAF8; padding:12px 16px; border-radius:10px; margin:0 0 8px;">
                </p>
                <button id="useBtn"
                    onclick="useText()"
                    style="
                        font-size:16px; font-weight:700;
                        padding:12px 20px;
                        background-color:#1A5276; color:white;
                        border:none; border-radius:10px; cursor:pointer; width:100%;
                    "
                >{use_text_label}</button>
            </div>
        </div>
        <script>
        function startVoice() {{
            var SpeechRec = window.SpeechRecognition || window.webkitSpeechRecognition;
            if (!SpeechRec) {{
                document.getElementById('statusMsg').textContent = "{no_support}";
                return;
            }}
            var rec = new SpeechRec();
            rec.lang = "{lang_code}";
            rec.continuous = false;
            rec.interimResults = false;
            document.getElementById('statusMsg').textContent = "{listening_text}";
            document.getElementById('resultBox').style.display = 'none';
            document.getElementById('micBtn').style.backgroundColor = '#E74C3C';

            rec.onresult = function(e) {{
                var text = e.results[0][0].transcript;
                document.getElementById('resultText').textContent = text;
                document.getElementById('resultBox').style.display = 'block';
                document.getElementById('statusMsg').textContent = '';
                document.getElementById('micBtn').style.backgroundColor = '#27AE60';
            }};
            rec.onerror = function(e) {{
                document.getElementById('statusMsg').textContent = "{error_text}";
                document.getElementById('micBtn').style.backgroundColor = '#27AE60';
            }};
            rec.onend = function() {{
                document.getElementById('micBtn').style.backgroundColor = '#27AE60';
            }};
            rec.start();
        }}

        function useText() {{
            var text = document.getElementById('resultText').textContent;
            if (!text) return;
            var url = new URL(window.parent.location.href);
            url.searchParams.set('voice_input', encodeURIComponent(text));
            window.parent.location.href = url.toString();
        }}
        </script>
        """,
        height=180,
    )

# ============================================================
# AI ENGINE
# ============================================================
# ─── Load .env ────────────────────────────────────────────────────────────────


# ─── Gemini Client ────────────────────────────────────────────────────────────
_client = None

def _get_client():
    global _client
    if _client is None:
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            try:
                if hasattr(st, "secrets") and "GOOGLE_API_KEY" in st.secrets:
                    api_key = st.secrets["GOOGLE_API_KEY"]
            except Exception:
                pass
        if not api_key:
            raise EnvironmentError(
                "GOOGLE_API_KEY not found. Please add GOOGLE_API_KEY to your .env file or Streamlit Cloud Secrets."
            )
        _client = genai.Client(api_key=api_key)
    return _client


# ─── Language Helpers ─────────────────────────────────────────────────────────
_LANG_NAMES = {"en": "English", "hi": "Hindi (हिंदी)"}

def _lang_instruction(language: str) -> str:
    lang_name = _LANG_NAMES.get(language, "English")
    return (
        f"IMPORTANT: Respond ENTIRELY in {lang_name}. "
        f"Every word of your response — including step titles, instructions, visual cues, "
        f"encouragement, and follow-up suggestions — must be in {lang_name}. "
        f"Do not mix languages."
    )


# ─── JSON Extraction Helper ───────────────────────────────────────────────────
def _extract_json(text: str) -> dict:
    """Robustly extract JSON from model response (handles markdown code fences)."""
    # Try direct parse first
    try:
        return json.loads(text)
    except Exception:
        pass
    # Strip markdown fences
    cleaned = re.sub(r"```(?:json)?", "", text).strip().strip("`").strip()
    try:
        return json.loads(cleaned)
    except Exception:
        # Find first { ... } block
        match = re.search(r"\{.*\}", cleaned, re.DOTALL)
        if match:
            try:
                return json.loads(match.group())
            except Exception:
                pass
    # Fallback
    return {
        "step_title": "Here is your answer",
        "steps": [{"number": 1, "instruction": text[:1200], "visual_cue": ""}],
        "is_scam_warning": False,
        "scam_detail": "",
        "encouragement": "You're doing great!",
        "follow_up_suggestions": [],
        "simple_summary": text[:200],
    }


# ─── Greeting & Daily Tip ─────────────────────────────────────────────────────
_GREETING_SYSTEM = """
You are a warm, caring AI companion for senior citizens (65+).
Generate a friendly, personalized greeting along with a helpful daily tip and a scam warning.

Return STRICT JSON with exactly these keys:
{
  "greeting": "A warm personal greeting for the time of day (1-2 sentences)",
  "daily_tip": "One genuinely useful health/tech/life tip for seniors today (2-3 sentences)",
  "scam_alert": "One specific, real-sounding scam that seniors should watch for today (2-3 sentences, practical advice)",
  "encouragement": "A short motivating line (1 sentence)"
}
"""

def get_greeting_and_tip(language: str = "en", time_of_day: str = "morning") -> dict:
    """
    Generate a time-aware greeting, daily tip, and scam alert.
    Returns a dict with keys: greeting, daily_tip, scam_alert, encouragement.
    """
    client = _get_client()
    prompt = (
        f"The time of day is: {time_of_day}. "
        f"{_lang_instruction(language)} "
        f"Generate the greeting JSON now."
    )
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=_GREETING_SYSTEM,
                response_mime_type="application/json",
            ),
        )
        return _extract_json(response.text)
    except Exception as e:
        # Friendly fallback
        fallbacks = {
            "en": {
                "greeting": f"Good {time_of_day}! I'm so glad you're here. How can I help you today?",
                "daily_tip": "💧 Tip: Try to drink a glass of water first thing in the morning — it helps your body wake up gently.",
                "scam_alert": "⚠️ Watch out for calls claiming your Aadhaar is blocked. No real government official will ask for OTP or money on a phone call.",
                "encouragement": "You've got this — I'm right here with you! 😊",
            },
            "hi": {
                "greeting": f"शुभ {time_of_day}! मुझे खुशी है कि आप यहाँ हैं। आज मैं आपकी कैसे मदद करूँ?",
                "daily_tip": "💧 सुझाव: सुबह उठकर सबसे पहले एक गिलास पानी पियें — इससे शरीर को ऊर्जा मिलती है।",
                "scam_alert": "⚠️ सावधान: ऐसे फोन कॉल से बचें जो कहें कि आपका आधार बंद हो गया है। असली सरकारी अधिकारी कभी OTP या पैसे नहीं मांगते।",
                "encouragement": "आप बहुत अच्छा कर रहे हैं — मैं हमेशा आपके साथ हूँ! 😊",
            },
        }
        return fallbacks.get(language, fallbacks["en"])


# ─── Task Response ────────────────────────────────────────────────────────────
_TASK_SYSTEM_BASE = """
You are an empathetic, patient AI companion specifically designed for senior citizens (65+).

YOUR CORE RULES:
1. NEVER use technical jargon. Replace it with plain everyday words.
2. Break EVERY task into small, numbered micro-steps. Maximum 3-4 sentences per step.
3. For each step, describe EXACTLY what to look for (color, shape, location of buttons).
4. Be warm, encouraging, and never make the user feel stupid for asking.
5. SCAM DETECTION: If the query involves anyone asking for money, OTPs, gift cards, passwords,
   remote access, prize claims, or threats — set is_scam_warning=true IMMEDIATELY.
6. End with 2-3 simple follow-up suggestions the user might need next.

RESPONSE FORMAT — Return STRICT JSON with exactly these keys:
{
  "step_title": "Short friendly title of what you're helping with (max 8 words)",
  "simple_summary": "One plain sentence summarizing what you'll do (max 20 words)",
  "steps": [
    {
      "number": 1,
      "instruction": "The exact thing to do — very clear, very simple (2-4 sentences)",
      "visual_cue": "What to look for on screen or device (color, icon, text) — 1 sentence"
    }
  ],
  "is_scam_warning": false,
  "scam_detail": "If is_scam_warning is true, explain WHY this is a scam and what to do. Otherwise empty string.",
  "encouragement": "A warm, short motivating message for the user (1 sentence)",
  "follow_up_suggestions": ["Suggestion 1", "Suggestion 2", "Suggestion 3"]
}

Limit steps to maximum 5. If a task needs more, cover the first 5 and ask if they want to continue.
"""

def get_task_response(
    query: str,
    category: str = "general",
    language: str = "en",
    history: list = None,
    category_context: str = "",
) -> dict:
    """
    Get step-by-step AI guidance for a user query.

    Args:
        query: The user's question or request.
        category: Task category ID (travel, health, tech, etc.)
        language: 'en' or 'hi'
        history: List of {role: 'user'|'model', content: str} for multi-turn.
        category_context: Extra system context from tasks.py for this category.

    Returns:
        dict with keys: step_title, simple_summary, steps, is_scam_warning,
                        scam_detail, encouragement, follow_up_suggestions
    """
    client = _get_client()

    # Build system instruction
    system_instruction = _TASK_SYSTEM_BASE
    if category_context:
        system_instruction += f"\n\nCATEGORY CONTEXT:\n{category_context}"
    system_instruction += f"\n\n{_lang_instruction(language)}"

    # Build conversation contents
    contents = []
    if history:
        for msg in history[-10:]:  # Keep last 10 turns for context
            role = msg.get("role", "user")
            # Gemini uses 'model' for assistant role
            gemini_role = "model" if role in ("assistant", "model") else "user"
            contents.append(
                types.Content(
                    role=gemini_role,
                    parts=[types.Part(text=msg.get("content", ""))],
                )
            )

    # Add current query
    contents.append(
        types.Content(role="user", parts=[types.Part(text=query)])
    )

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=contents,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                response_mime_type="application/json",
            ),
        )
        return _extract_json(response.text)
    except Exception as e:
        lang = language
        if lang == "hi":
            return {
                "step_title": "एक छोटी सी समस्या आई",
                "simple_summary": "मुझे जवाब देने में थोड़ी दिक्कत हुई। कृपया दोबारा कोशिश करें।",
                "steps": [{"number": 1, "instruction": f"माफ करें, एक तकनीकी समस्या आई: {str(e)[:100]}। कृपया दोबारा पूछें।", "visual_cue": ""}],
                "is_scam_warning": False,
                "scam_detail": "",
                "encouragement": "चिंता न करें, दोबारा पूछें!",
                "follow_up_suggestions": [],
            }
        return {
            "step_title": "A small hiccup occurred",
            "simple_summary": "I had trouble getting your answer. Please try again.",
            "steps": [{"number": 1, "instruction": f"Sorry, a technical issue occurred: {str(e)[:100]}. Please try asking again.", "visual_cue": ""}],
            "is_scam_warning": False,
            "scam_detail": "",
            "encouragement": "Don't worry — just try again!",
            "follow_up_suggestions": [],
        }

# ============================================================
# MAIN STREAMLIT APP
# ============================================================
# ══════════════════════════════════════════════════════════════════════════════
# PAGE CONFIG
# ══════════════════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="Senior Daily Companion",
    page_icon="☀️",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ══════════════════════════════════════════════════════════════════════════════
# SESSION STATE
# ══════════════════════════════════════════════════════════════════════════════
def _init_state():
    defaults = {
        "lang": "en",
        "font_size": "large",       # "normal" | "large" | "xlarge"
        "high_contrast": False,
        "chat_history": [],          # [{role, content}]
        "selected_category": None,
        "greeting_data": None,
        "greeting_lang": None,
        "show_emergency": False,
        "last_ai_response": None,
        "pending_voice": "",
        "user_input": "",
        "ask_simplify": False,
        "ask_next": False,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

_init_state()


# ══════════════════════════════════════════════════════════════════════════════
# TRANSLATION HELPER
# ══════════════════════════════════════════════════════════════════════════════
def t(key: str) -> str:
    """Return translated string for the current language."""
    lang = st.session_state.lang
    return TRANSLATIONS.get(lang, TRANSLATIONS["en"]).get(key, key)


# ══════════════════════════════════════════════════════════════════════════════
# TIME HELPERS
# ══════════════════════════════════════════════════════════════════════════════
def _get_time_of_day() -> str:
    IST = pytz.timezone("Asia/Kolkata")
    hour = datetime.now(IST).hour
    if 5 <= hour < 12:
        return "morning"
    elif 12 <= hour < 17:
        return "afternoon"
    elif 17 <= hour < 21:
        return "evening"
    return "night"

def _greeting_key_for_time(time_of_day: str) -> str:
    return {
        "morning":   "greeting_morning",
        "afternoon": "greeting_afternoon",
        "evening":   "greeting_evening",
        "night":     "greeting_night",
    }.get(time_of_day, "greeting_morning")

def _formatted_date(lang: str) -> str:
    IST = pytz.timezone("Asia/Kolkata")
    now = datetime.now(IST)
    if lang == "hi":
        months_hi = ["जनवरी","फ़रवरी","मार्च","अप्रैल","मई","जून",
                     "जुलाई","अगस्त","सितंबर","अक्टूबर","नवंबर","दिसंबर"]
        days_hi = ["सोमवार","मंगलवार","बुधवार","गुरुवार","शुक्रवार","शनिवार","रविवार"]
        return f"{days_hi[now.weekday()]}, {now.day} {months_hi[now.month-1]} {now.year}"
    return now.strftime("%A, %d %B %Y")


# ══════════════════════════════════════════════════════════════════════════════
# DYNAMIC CSS
# ══════════════════════════════════════════════════════════════════════════════
def _inject_css():
    sizes = {
        "normal": {"body": "18px", "sub": "22px", "h3": "26px", "h2": "32px", "h1": "42px", "tile": "20px", "tile_icon": "44px"},
        "large":  {"body": "22px", "sub": "26px", "h3": "30px", "h2": "38px", "h1": "50px", "tile": "23px", "tile_icon": "52px"},
        "xlarge": {"body": "27px", "sub": "32px", "h3": "36px", "h2": "46px", "h1": "58px", "tile": "28px", "tile_icon": "60px"},
    }
    s = sizes.get(st.session_state.font_size, sizes["large"])

    if st.session_state.high_contrast:
        c = {
            "bg": "#0a0a0a", "text": "#f0f0f0", "card": "#1a1a1a",
            "primary": "#FFD700", "primary_text": "#000000",
            "accent": "#00BFFF", "border": "#888888",
            "user_bubble": "#001a33", "ai_bubble": "#001a00",
            "tip_bg": "#001a00", "tip_border": "#00FF00",
            "scam_bg": "#1a0000", "scam_border": "#FF4444",
            "input_bg": "#111111", "muted": "#aaaaaa",
            "tile_bg": "#1a1a1a", "tile_border": "#FFD700",
            "section_bg": "#111111",
        }
    else:
        c = {
            "bg": "#EEF2F7", "text": "#1B2631", "card": "#FFFFFF",
            "primary": "#1A5276", "primary_text": "#FFFFFF",
            "accent": "#2E86AB", "border": "#D5D8DC",
            "user_bubble": "#D6EAF8", "ai_bubble": "#EAFAF1",
            "tip_bg": "#EAFAF1", "tip_border": "#27AE60",
            "scam_bg": "#FDEDEC", "scam_border": "#E74C3C",
            "input_bg": "#FFFFFF", "muted": "#7F8C8D",
            "tile_bg": "#FFFFFF", "tile_border": "#2E86AB",
            "section_bg": "#F8F9FA",
        }

    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800;900&display=swap');

    *, *::before, *::after {{ box-sizing: border-box; margin: 0; }}

    html, body {{
        font-family: 'Nunito', Arial, sans-serif !important;
        font-size: {s["body"]} !important;
        background-color: {c["bg"]} !important;
        color: {c["text"]} !important;
        line-height: 1.75 !important;
    }}
    .stApp {{ background-color: {c["bg"]} !important; }}

    /* ── Typography ── */
    h1, .stMarkdown h1 {{
        font-size: {s["h1"]} !important; font-weight: 900 !important;
        color: {c["primary"]} !important; line-height: 1.2 !important;
    }}
    h2, .stMarkdown h2 {{
        font-size: {s["h2"]} !important; font-weight: 800 !important;
        color: {c["text"]} !important;
    }}
    h3, .stMarkdown h3 {{
        font-size: {s["h3"]} !important; font-weight: 700 !important;
        color: {c["primary"]} !important;
    }}
    p, span, div, label, li,
    .stMarkdown, .stText, .stCaption {{
        font-size: {s["body"]} !important;
        color: {c["text"]} !important;
        font-family: 'Nunito', Arial, sans-serif !important;
    }}

    /* ── Streamlit-specific overrides ── */
    .stApp > header {{ display: none !important; }}
    #MainMenu, footer, .stDeployButton {{ visibility: hidden !important; }}
    .block-container {{ padding: 1.5rem 2rem 3rem 2rem !important; max-width: 1200px !important; }}

    /* ── Inputs ── */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {{
        font-family: 'Nunito', Arial, sans-serif !important;
        font-size: {s["sub"]} !important;
        padding: 16px 20px !important;
        border-radius: 14px !important;
        border: 3px solid {c["accent"]} !important;
        background-color: {c["input_bg"]} !important;
        color: {c["text"]} !important;
        min-height: 62px !important;
        line-height: 1.5 !important;
    }}
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {{
        border-color: {c["primary"]} !important;
        box-shadow: 0 0 0 3px rgba(46,134,171,0.25) !important;
        outline: none !important;
    }}

    /* ── Buttons ── */
    .stButton > button {{
        font-family: 'Nunito', Arial, sans-serif !important;
        font-size: {s["sub"]} !important;
        font-weight: 800 !important;
        padding: 16px 24px !important;
        min-height: 66px !important;
        border-radius: 14px !important;
        background-color: {c["primary"]} !important;
        color: {c["primary_text"]} !important;
        border: none !important;
        width: 100% !important;
        cursor: pointer !important;
        transition: all 0.18s ease !important;
        letter-spacing: 0.3px !important;
        line-height: 1.3 !important;
        white-space: pre-line !important;
    }}
    .stButton > button:hover {{
        transform: translateY(-3px) !important;
        box-shadow: 0 8px 24px rgba(0,0,0,0.22) !important;
        filter: brightness(1.08) !important;
    }}
    .stButton > button:active {{ transform: translateY(0) !important; }}

    /* ── Selectbox / Radio ── */
    .stSelectbox > div > div,
    .stRadio > div,
    .stRadio label, .stCheckbox label {{
        font-family: 'Nunito', Arial, sans-serif !important;
        font-size: {s["body"]} !important;
        color: {c["text"]} !important;
    }}
    .stSelectbox select {{ min-height: 52px !important; font-size: {s["body"]} !important; }}

    /* ── Divider ── */
    hr {{ border: 2px solid {c["border"]}; margin: 28px 0; border-radius: 2px; }}

    /* ── Alert boxes ── */
    .stAlert {{
        font-family: 'Nunito', Arial, sans-serif !important;
        font-size: {s["body"]} !important;
        border-radius: 14px !important;
        padding: 18px 22px !important;
    }}
    .stInfo {{ background-color: {c["tip_bg"]} !important; border-left: 6px solid {c["tip_border"]} !important; }}
    .stError {{ background-color: {c["scam_bg"]} !important; border-left: 6px solid {c["scam_border"]} !important; font-weight: 700 !important; }}
    .stSuccess {{ background-color: {c["tip_bg"]} !important; }}

    /* ── Spinner ── */
    .stSpinner > div > div {{ font-size: {s["sub"]} !important; color: {c["primary"]} !important; }}

    /* ════════════════════════════════
       CUSTOM COMPONENTS
    ════════════════════════════════ */

    /* Accessibility top bar */
    .access-bar {{
        background: linear-gradient(90deg, {c["primary"]}, {c["accent"]});
        border-radius: 16px;
        padding: 14px 22px;
        margin-bottom: 22px;
        display: flex; align-items: center;
        box-shadow: 0 4px 16px rgba(0,0,0,0.15);
    }}

    /* App title in bar */
    .bar-title {{
        font-size: {s["h3"]} !important;
        font-weight: 900 !important;
        color: white !important;
        margin: 0 !important;
        white-space: nowrap;
    }}
    .bar-tagline {{
        font-size: {s["body"]} !important;
        color: rgba(255,255,255,0.88) !important;
        margin: 0 !important;
    }}

    /* SOS button */
    .stButton.sos-btn > button {{
        background-color: #E74C3C !important;
        font-size: {s["sub"]} !important;
        min-height: 56px !important;
        font-weight: 900 !important;
        letter-spacing: 0.5px !important;
        animation: pulse 2s infinite;
    }}
    @keyframes pulse {{
        0%, 100% {{ box-shadow: 0 0 0 0 rgba(231,76,60,0.4); }}
        50% {{ box-shadow: 0 0 0 10px rgba(231,76,60,0); }}
    }}

    /* Greeting card */
    .greeting-card {{
        background: linear-gradient(135deg, {c["primary"]} 0%, {c["accent"]} 100%);
        border-radius: 22px;
        padding: 32px 36px;
        margin-bottom: 22px;
        box-shadow: 0 6px 24px rgba(26,82,118,0.2);
    }}
    .greeting-time {{
        font-size: {s["h2"]} !important;
        font-weight: 900 !important;
        color: white !important;
        margin-bottom: 6px !important;
    }}
    .greeting-subtitle {{
        font-size: {s["sub"]} !important;
        color: rgba(255,255,255,0.92) !important;
        margin-bottom: 4px !important;
    }}
    .greeting-date {{
        font-size: {s["body"]} !important;
        color: rgba(255,255,255,0.78) !important;
    }}
    .greeting-ai-text {{
        font-size: {s["sub"]} !important;
        color: white !important;
        background: rgba(255,255,255,0.15);
        border-radius: 12px;
        padding: 14px 18px;
        margin-top: 14px !important;
        font-style: italic;
    }}

    /* Tip card */
    .tip-card {{
        background-color: {c["tip_bg"]};
        border: 2.5px solid {c["tip_border"]};
        border-radius: 18px;
        padding: 22px 26px;
        height: 100%;
        box-shadow: 0 2px 10px rgba(39,174,96,0.1);
    }}
    .tip-card-title {{
        font-size: {s["h3"]} !important;
        font-weight: 800 !important;
        color: #1D8348 !important;
        margin-bottom: 10px !important;
    }}
    .tip-card-body {{
        font-size: {s["body"]} !important;
        color: {c["text"]} !important;
        line-height: 1.8 !important;
    }}

    /* Scam card */
    .scam-card {{
        background-color: {c["scam_bg"]};
        border: 2.5px solid {c["scam_border"]};
        border-radius: 18px;
        padding: 22px 26px;
        height: 100%;
        box-shadow: 0 2px 10px rgba(231,76,60,0.1);
    }}
    .scam-card-title {{
        font-size: {s["h3"]} !important;
        font-weight: 800 !important;
        color: #C0392B !important;
        margin-bottom: 10px !important;
    }}
    .scam-card-body {{
        font-size: {s["body"]} !important;
        color: {c["text"]} !important;
        line-height: 1.8 !important;
    }}

    /* Section titles */
    .section-title {{
        font-size: {s["h2"]} !important;
        font-weight: 900 !important;
        color: {c["primary"]} !important;
        margin: 28px 0 6px !important;
        padding-bottom: 10px !important;
        border-bottom: 3px solid {c["accent"]};
    }}
    .section-sub {{
        font-size: {s["body"]} !important;
        color: {c["muted"]} !important;
        margin-bottom: 18px !important;
    }}

    /* Task tiles */
    .tile-active-badge {{
        background-color: {c["primary"]};
        color: {c["primary_text"]};
        border-radius: 8px;
        padding: 3px 10px;
        font-size: 13px !important;
        font-weight: 700 !important;
        display: inline-block;
        margin-bottom: 6px;
    }}

    /* Chat bubbles */
    .chat-container {{
        background-color: {c["card"]};
        border: 2px solid {c["border"]};
        border-radius: 20px;
        padding: 24px 28px;
        margin: 18px 0;
        max-height: 480px;
        overflow-y: auto;
        box-shadow: 0 2px 12px rgba(0,0,0,0.06);
    }}
    .user-bubble {{
        background-color: {c["user_bubble"]};
        border-radius: 18px 18px 5px 18px;
        padding: 16px 20px;
        margin: 12px 0 12px auto;
        max-width: 82%;
        font-size: {s["body"]} !important;
        box-shadow: 0 1px 4px rgba(0,0,0,0.08);
    }}
    .user-label {{
        font-size: 13px !important;
        font-weight: 800 !important;
        color: {c["primary"]} !important;
        text-align: right;
        margin-bottom: 4px;
    }}
    .ai-bubble {{
        background-color: {c["ai_bubble"]};
        border: 2px solid {c["border"]};
        border-radius: 18px 18px 18px 5px;
        padding: 20px 24px;
        margin: 12px auto 12px 0;
        max-width: 90%;
        font-size: {s["body"]} !important;
        box-shadow: 0 1px 4px rgba(0,0,0,0.06);
    }}
    .ai-label {{
        font-size: 13px !important;
        font-weight: 800 !important;
        color: #1D8348 !important;
        margin-bottom: 4px;
    }}

    /* AI Response cards */
    .response-card {{
        background-color: {c["card"]};
        border: 2.5px solid {c["accent"]};
        border-radius: 20px;
        padding: 26px 30px;
        margin: 16px 0;
        box-shadow: 0 3px 16px rgba(26,82,118,0.1);
    }}
    .response-title {{
        font-size: {s["h3"]} !important;
        font-weight: 900 !important;
        color: {c["primary"]} !important;
        margin-bottom: 6px !important;
    }}
    .response-summary {{
        font-size: {s["body"]} !important;
        color: {c["muted"]} !important;
        margin-bottom: 18px !important;
        font-style: italic;
    }}

    /* Step item */
    .step-item {{
        background-color: {c["section_bg"]};
        border-left: 5px solid {c["primary"]};
        border-radius: 0 12px 12px 0;
        padding: 14px 18px;
        margin: 10px 0;
        font-size: {s["body"]} !important;
    }}
    .step-num {{
        font-size: {s["sub"]} !important;
        font-weight: 900 !important;
        color: {c["primary"]} !important;
    }}
    .step-instruction {{
        font-size: {s["body"]} !important;
        color: {c["text"]} !important;
        line-height: 1.8 !important;
        margin: 4px 0 0 !important;
    }}
    .visual-cue {{
        background-color: {c["tip_bg"]};
        border: 1.5px solid {c["tip_border"]};
        border-radius: 8px;
        padding: 8px 14px;
        margin-top: 8px;
        font-size: {s["body"]} !important;
        color: #1D8348 !important;
    }}
    .encouragement {{
        font-size: {s["sub"]} !important;
        font-weight: 700 !important;
        color: {c["primary"]} !important;
        margin: 16px 0 8px !important;
        text-align: center;
    }}

    /* Scam warning banner */
    .scam-banner {{
        background: linear-gradient(135deg, #922B21, #E74C3C);
        color: white !important;
        border-radius: 16px;
        padding: 22px 26px;
        margin: 14px 0;
        box-shadow: 0 4px 16px rgba(231,76,60,0.35);
    }}
    .scam-banner * {{ color: white !important; }}
    .scam-banner-title {{
        font-size: {s["h3"]} !important;
        font-weight: 900 !important;
        margin-bottom: 10px !important;
    }}
    .scam-banner-body {{
        font-size: {s["body"]} !important;
        line-height: 1.8 !important;
    }}
    .scam-banner-helpline {{
        font-size: {s["sub"]} !important;
        font-weight: 800 !important;
        background: rgba(255,255,255,0.18);
        border-radius: 10px;
        padding: 10px 16px;
        margin-top: 12px;
        display: inline-block;
    }}

    /* Suggestions chips */
    .suggestions-label {{
        font-size: {s["body"]} !important;
        font-weight: 700 !important;
        color: {c["muted"]} !important;
        margin: 16px 0 8px !important;
    }}

    /* Emergency panel */
    .emergency-panel {{
        background: linear-gradient(135deg, #922B21, #C0392B);
        border-radius: 22px;
        padding: 30px 34px;
        color: white !important;
        box-shadow: 0 6px 28px rgba(192,57,43,0.4);
    }}
    .emergency-panel * {{ color: white !important; }}
    .emergency-title {{
        font-size: {s["h2"]} !important;
        font-weight: 900 !important;
        margin-bottom: 6px !important;
    }}
    .emergency-subtitle {{
        font-size: {s["body"]} !important;
        opacity: 0.9;
        margin-bottom: 20px !important;
    }}
    .emergency-number {{
        background: rgba(255,255,255,0.18);
        border-radius: 14px;
        padding: 16px 20px;
        margin: 10px 0;
        font-size: {s["sub"]} !important;
        font-weight: 800 !important;
        border: 2px solid rgba(255,255,255,0.3);
    }}
    .emergency-note {{
        font-size: {s["body"]} !important;
        margin-top: 18px !important;
        background: rgba(0,0,0,0.2);
        border-radius: 10px;
        padding: 12px 16px;
        font-weight: 700 !important;
    }}

    /* Category selected label */
    .cat-selected {{
        background-color: {c["primary"]};
        color: {c["primary_text"]} !important;
        border-radius: 10px;
        padding: 6px 14px;
        font-size: {s["body"]} !important;
        font-weight: 700 !important;
        display: inline-block;
        margin-bottom: 12px;
    }}

    /* Input area container */
    .input-area {{
        background-color: {c["card"]};
        border: 2.5px solid {c["border"]};
        border-radius: 18px;
        padding: 22px 26px;
        margin-top: 16px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    }}

    /* Footer */
    .app-footer {{
        text-align: center;
        padding: 20px 0 10px;
        font-size: {s["body"]} !important;
        color: {c["muted"]} !important;
        border-top: 2px solid {c["border"]};
        margin-top: 40px;
    }}
    </style>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# GREETING LOADER
# ══════════════════════════════════════════════════════════════════════════════
def _load_greeting():
    """Load greeting once per session (or when language changes)."""
    lang = st.session_state.lang
    if (
        st.session_state.greeting_data is None
        or st.session_state.greeting_lang != lang
    ):
        with st.spinner(t("thinking")):
            tod = _get_time_of_day()
            st.session_state.greeting_data = get_greeting_and_tip(lang, tod)
            st.session_state.greeting_lang = lang


# ══════════════════════════════════════════════════════════════════════════════
# COMPONENT RENDERERS
# ══════════════════════════════════════════════════════════════════════════════

def _render_access_bar():
    """Top accessibility bar: branding, language toggle, font size, contrast, SOS."""
    st.markdown(
        f"""
        <div class="access-bar">
            <div>
                <p class="bar-title">☀️ {t("app_title")}</p>
                <p class="bar-tagline">{t("app_tagline")}</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col_lang, col_font, col_contrast, col_sos = st.columns([2, 3, 2, 1.5])

    with col_lang:
        lang_choice = st.radio(
            t("language_label"),
            options=["🇬🇧 English", "🇮🇳 हिंदी"],
            index=0 if st.session_state.lang == "en" else 1,
            horizontal=True,
            key="_lang_radio",
            label_visibility="collapsed",
        )
        new_lang = "en" if "English" in lang_choice else "hi"
        if new_lang != st.session_state.lang:
            st.session_state.lang = new_lang
            st.session_state.greeting_data = None  # Force greeting reload
            st.rerun()

    with col_font:
        font_labels = [t("font_normal"), t("font_large"), t("font_xlarge")]
        size_map = {t("font_normal"): "normal", t("font_large"): "large", t("font_xlarge"): "xlarge"}
        cur_label = {v: k for k, v in size_map.items()}.get(st.session_state.font_size, font_labels[1])
        font_choice = st.radio(
            t("font_label"),
            options=font_labels,
            index=font_labels.index(cur_label),
            horizontal=True,
            key="_font_radio",
        )
        new_size = size_map[font_choice]
        if new_size != st.session_state.font_size:
            st.session_state.font_size = new_size
            st.rerun()

    with col_contrast:
        new_contrast = st.checkbox(
            t("contrast_label"),
            value=st.session_state.high_contrast,
            key="_contrast_chk",
        )
        if new_contrast != st.session_state.high_contrast:
            st.session_state.high_contrast = new_contrast
            st.rerun()

    with col_sos:
        if st.button(t("sos_button"), key="sos_btn", use_container_width=True):
            st.session_state.show_emergency = not st.session_state.show_emergency
            st.rerun()


def _render_greeting():
    """Time-aware greeting card + daily tip + scam alert cards."""
    tod = _get_time_of_day()
    greeting_key = _greeting_key_for_time(tod)
    greeting_time = t(greeting_key)
    date_str = _formatted_date(st.session_state.lang)

    data = st.session_state.greeting_data or {}
    ai_greeting = data.get("greeting", "")
    daily_tip = data.get("daily_tip", "")
    scam_alert = data.get("scam_alert", "")
    encouragement = data.get("encouragement", "")

    st.markdown(
        f"""
        <div class="greeting-card">
            <p class="greeting-time">{greeting_time}</p>
            <p class="greeting-subtitle">{t("greeting_subtitle")}</p>
            <p class="greeting-date">📅 {t("todays_date")}: {date_str}</p>
            {'<p class="greeting-ai-text">' + ai_greeting + '</p>' if ai_greeting else ''}
            {'<p class="greeting-ai-text">💪 ' + encouragement + '</p>' if encouragement else ''}
        </div>
        """,
        unsafe_allow_html=True,
    )

    if daily_tip or scam_alert:
        tip_col, scam_col = st.columns(2)
        with tip_col:
            st.markdown(
                f"""
                <div class="tip-card">
                    <p class="tip-card-title">{t("daily_tip_title")}</p>
                    <p class="tip-card-body">{daily_tip}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with scam_col:
            st.markdown(
                f"""
                <div class="scam-card">
                    <p class="scam-card-title">{t("scam_alert_title")}</p>
                    <p class="scam-card-body">{scam_alert}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )


def _render_task_tiles():
    """8 task category tiles in a 4×2 grid."""
    st.markdown(f'<p class="section-title">{t("quick_help_title")}</p>', unsafe_allow_html=True)
    st.markdown(f'<p class="section-sub">{t("quick_help_subtitle")}</p>', unsafe_allow_html=True)

    cols = st.columns(4)
    for i, task_id in enumerate(TASK_ORDER):
        task = TASKS[task_id]
        tile_label = t(task["tile_key"])
        is_selected = st.session_state.selected_category == task_id
        col = cols[i % 4]
        with col:
            if is_selected:
                st.markdown('<p class="tile-active-badge">✓ Selected</p>', unsafe_allow_html=True)
            btn_label = ("✅ " if is_selected else "") + tile_label
            if st.button(btn_label, key=f"tile_{task_id}", use_container_width=True):
                st.session_state.selected_category = task_id
                # Add a helpful prompt to get started
                cat_name = t(task["cat_key"])
                lang = st.session_state.lang
                examples = task["examples_hi"] if lang == "hi" else task["examples_en"]
                welcome_msg = (
                    f"{'मैं आपकी' if lang == 'hi' else 'I can help you with'} **{cat_name}** {'में मदद करूँगा' if lang == 'hi' else ''}. "
                    f"\n\n{'उदाहरण के लिए आप पूछ सकते हैं:' if lang == 'hi' else 'For example, you can ask:'}"
                    + "".join(f"\n• {ex}" for ex in examples[:3])
                )
                st.session_state.chat_history = [
                    {"role": "assistant", "content": welcome_msg}
                ]
                st.session_state.last_ai_response = None
                st.rerun()


def _render_chat():
    """Main AI conversation panel."""
    st.markdown(f'<p class="section-title">{t("chat_title")}</p>', unsafe_allow_html=True)

    # Show selected category badge
    if st.session_state.selected_category:
        cat_name = t(TASKS[st.session_state.selected_category]["cat_key"])
        st.markdown(
            f'<span class="cat-selected">{TASKS[st.session_state.selected_category]["icon"]} {cat_name}</span>',
            unsafe_allow_html=True,
        )

    # ── Chat history ──
    history = st.session_state.chat_history
    if not history:
        welcome = t("chat_welcome")
        st.markdown(
            f"""
            <div class="chat-container">
                <div class="ai-bubble">
                    <p class="ai-label">☀️ {t("assistant_label")}</p>
                    <p style="white-space: pre-line;">{welcome}</p>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        bubbles_html = '<div class="chat-container">'
        for msg in history:
            role = msg.get("role", "user")
            content = msg.get("content", "").replace("\n", "<br>")
            if role == "user":
                bubbles_html += f"""
                    <div style="text-align:right;">
                        <p class="user-label">🧑 {t("you_label")}</p>
                        <div class="user-bubble">{content}</div>
                    </div>
                """
            else:
                bubbles_html += f"""
                    <div style="text-align:left;">
                        <p class="ai-label">☀️ {t("assistant_label")}</p>
                        <div class="ai-bubble">{content}</div>
                    </div>
                """
        bubbles_html += "</div>"
        st.markdown(bubbles_html, unsafe_allow_html=True)

    # ── Last AI structured response ──
    if st.session_state.last_ai_response:
        _render_ai_response(st.session_state.last_ai_response)

    # ── Input area ──
    st.markdown('<div class="input-area">', unsafe_allow_html=True)

    # Check for voice input from URL
    voice_text = ""
    try:
        raw_voice = st.query_params.get("voice_input", "")
        if raw_voice:
            from urllib.parse import unquote
            voice_text = unquote(raw_voice)
            # Clear it after reading
            st.query_params.clear()
    except Exception:
        pass

    prefill = voice_text or st.session_state.get("pending_voice", "")

    input_col, voice_col = st.columns([4, 1])
    with input_col:
        user_text = st.text_input(
            label=t("chat_placeholder"),
            value=prefill,
            placeholder=t("chat_placeholder"),
            key="main_input",
            label_visibility="collapsed",
        )
    with voice_col:
        render_voice_input(st.session_state.lang)

    # Quick action buttons
    ask_col, simplify_col, next_col = st.columns([2, 2, 2])
    with ask_col:
        ask_clicked = st.button(t("ask_button"), key="ask_btn", use_container_width=True)
    with simplify_col:
        simplify_clicked = st.button(t("explain_simpler"), key="simplify_btn", use_container_width=True)
    with next_col:
        next_clicked = st.button(t("next_step"), key="next_btn", use_container_width=True)

    st.markdown("</div>", unsafe_allow_html=True)

    # ── Follow-up suggestion chips ──
    if st.session_state.last_ai_response:
        suggestions = st.session_state.last_ai_response.get("follow_up_suggestions", [])
        if suggestions:
            st.markdown(f'<p class="suggestions-label">{t("suggestions_title")}</p>', unsafe_allow_html=True)
            sug_cols = st.columns(min(len(suggestions), 3))
            for i, sug in enumerate(suggestions[:3]):
                with sug_cols[i]:
                    if st.button(f"💬 {sug}", key=f"sug_{i}", use_container_width=True):
                        _handle_query(sug)

    # ── Handle query submission ──
    query_to_send = None
    if ask_clicked and user_text.strip():
        query_to_send = user_text.strip()
    elif simplify_clicked:
        lang = st.session_state.lang
        query_to_send = "कृपया और आसान भाषा में समझाएं।" if lang == "hi" else "Please explain that more simply, like I've never done this before."
    elif next_clicked:
        lang = st.session_state.lang
        query_to_send = "अगला कदम क्या है?" if lang == "hi" else "What is the next step I should do?"

    if query_to_send:
        _handle_query(query_to_send)


def _handle_query(query: str):
    """Run AI query, update history, store structured response."""
    lang = st.session_state.lang
    category = st.session_state.selected_category or "general"
    category_context = TASKS.get(category, {}).get("system_context", "")

    # Add user message to history
    st.session_state.chat_history.append({"role": "user", "content": query})

    # Build history for AI (exclude structured-response messages)
    ai_history = [
        msg for msg in st.session_state.chat_history[:-1]
        if msg.get("role") in ("user", "assistant", "model")
    ]

    with st.spinner(t("thinking")):
        response = get_task_response(
            query=query,
            category=category,
            language=lang,
            history=ai_history,
            category_context=category_context,
        )

    st.session_state.last_ai_response = response

    # Add assistant reply to history (simple text for bubble display)
    summary = response.get("simple_summary", "")
    st.session_state.chat_history.append({
        "role": "assistant",
        "content": summary,
    })

    st.rerun()


def _render_ai_response(resp: dict):
    """Render a structured AI response card with steps, TTS, and actions."""
    lang = st.session_state.lang
    is_scam = resp.get("is_scam_warning", False)

    # Scam warning banner
    if is_scam:
        scam_detail = resp.get("scam_detail", "")
        st.markdown(
            f"""
            <div class="scam-banner">
                <p class="scam-banner-title">{t("scam_banner")}</p>
                <p class="scam-banner-body">{t("scam_detail")}</p>
                {'<p class="scam-banner-body">' + scam_detail + '</p>' if scam_detail else ''}
                <span class="scam-banner-helpline">{t("scam_helpline")}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Main response card
    step_title = resp.get("step_title", "")
    simple_summary = resp.get("simple_summary", "")
    steps = resp.get("steps", [])
    encouragement = resp.get("encouragement", "")

    st.markdown(
        f"""
        <div class="response-card">
            <p class="response-title">{'⚠️ ' if is_scam else '✅ '}{step_title}</p>
            <p class="response-summary">{simple_summary}</p>
        """,
        unsafe_allow_html=True,
    )

    # Step items
    step_prefix = t("step_prefix")
    visual_label = t("visual_cue_label")
    for step in steps:
        num = step.get("number", "")
        instruction = step.get("instruction", "")
        visual_cue = step.get("visual_cue", "")
        st.markdown(
            f"""
            <div class="step-item">
                <p class="step-num">📌 {step_prefix} {num}</p>
                <p class="step-instruction">{instruction}</p>
                {'<div class="visual-cue">' + visual_label + ' ' + visual_cue + '</div>' if visual_cue else ''}
            </div>
            """,
            unsafe_allow_html=True,
        )

    if encouragement:
        st.markdown(
            f'<p class="encouragement">{t("encouragement_label")} {encouragement}</p>',
            unsafe_allow_html=True,
        )

    st.markdown("</div>", unsafe_allow_html=True)

    # Read Aloud — compile full text
    tts_text = f"{step_title}. {simple_summary}. "
    for step in steps:
        tts_text += f"{t('step_prefix')} {step.get('number','')}: {step.get('instruction','')}. "
    if encouragement:
        tts_text += encouragement

    render_read_aloud(tts_text, lang, t("read_aloud"))


def _render_emergency():
    """Emergency contacts overlay."""
    st.markdown(
        f"""
        <div class="emergency-panel">
            <p class="emergency-title">{t("emergency_title")}</p>
            <p class="emergency-subtitle">{t("emergency_subtitle")}</p>
            <div class="emergency-number">🚑 {t("emergency_ambulance")}</div>
            <div class="emergency-number">🚔 {t("emergency_police")}</div>
            <div class="emergency-number">🚒 {t("emergency_fire")}</div>
            <div class="emergency-number">📞 {t("emergency_helpline")}</div>
            <div class="emergency-number">🛡️ {t("emergency_cyber")}</div>
            <p class="emergency-note">⚡ {t("emergency_note")}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if st.button(t("emergency_close"), key="close_emergency", use_container_width=True):
        st.session_state.show_emergency = False
        st.rerun()


# ══════════════════════════════════════════════════════════════════════════════
# MAIN APP
# ══════════════════════════════════════════════════════════════════════════════
def main():
    # 1. Inject CSS
    _inject_css()

    # 2. Accessibility bar (language, font, contrast, SOS)
    _render_access_bar()

    st.divider()

    # 3. Emergency panel (shown full-width if triggered)
    if st.session_state.show_emergency:
        _render_emergency()
        st.divider()

    # 4. Load and show greeting
    _load_greeting()
    _render_greeting()

    st.divider()

    # 5. Task tiles
    _render_task_tiles()

    st.divider()

    # 6. Chat panel
    _render_chat()

    # 7. Footer
    st.markdown(
        f'<p class="app-footer">{t("footer")}</p>',
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
