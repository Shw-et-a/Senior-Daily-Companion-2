"""
Voice components for Senior Daily Companion.
Provides:
  - render_read_aloud(text, language) — TTS button using Web Speech API
  - render_voice_input(language)      — STT mic button using Web Speech API
"""

import streamlit.components.v1 as components


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
