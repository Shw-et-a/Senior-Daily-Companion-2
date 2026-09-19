"""
AI Engine — All Gemini API calls for Senior Daily Companion.
Functions:
  - get_greeting_and_tip(language, time_of_day) → dict
  - get_task_response(query, category, language, history) → dict
"""

import os
import json
import re
from dotenv import load_dotenv
from google import genai
from google.genai import types

# ─── Load .env ────────────────────────────────────────────────────────────────
load_dotenv()

# ─── Gemini Client ────────────────────────────────────────────────────────────
_client = None

def _get_client():
    global _client
    if _client is None:
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise EnvironmentError(
                "GOOGLE_API_KEY not found. Please create a .env file with your key. "
                "See .env.example for instructions."
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
