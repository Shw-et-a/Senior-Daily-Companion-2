/**
 * Senior Daily Companion - Speech Engine
 * Web Speech API for Text-to-Speech (reading aloud) and Speech-to-Text (voice typing)
 * Optimized for Senior Citizens: slower cadence, high intelligibility, bilingual (EN & HI)
 */

class SeniorSpeechEngine {
  constructor() {
    this.synth = window.speechSynthesis || null;
    this.currentUtterance = null;
    this.recognition = null;
    this.isListening = false;
    this.voices = [];

    if (this.synth) {
      this.loadVoices();
      if (speechSynthesis.onvoiceschanged !== undefined) {
        speechSynthesis.onvoiceschanged = () => this.loadVoices();
      }
    }

    this.initRecognition();
  }

  loadVoices() {
    if (!this.synth) return;
    this.voices = this.synth.getVoices();
  }

  initRecognition() {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) {
      console.warn("Speech recognition not supported in this browser.");
      return;
    }

    this.recognition = new SpeechRecognition();
    this.recognition.continuous = false;
    this.recognition.interimResults = false;
    this.recognition.maxAlternatives = 1;
  }

  /**
   * Speak text out loud with calm, patient pacing for seniors
   */
  speak(text, lang = 'en', onStart, onEnd, onError) {
    if (!this.synth) {
      alert("Text-to-speech is not supported on this browser.");
      return;
    }

    // Stop any currently playing audio
    this.stop();

    // Clean markdown symbols or asterisks before speaking
    const cleanText = text
      .replace(/[#*_`~>-]/g, ' ')
      .replace(/https?:\/\/\S+/g, 'link')
      .replace(/\s+/g, ' ')
      .trim();

    if (!cleanText) return;

    const utterance = new SpeechSynthesisUtterance(cleanText);
    
    // Senior-friendly voice parameters: slower rate (0.85x), natural pitch (1.0)
    utterance.rate = 0.88;
    utterance.pitch = 1.0;
    utterance.volume = 1.0;

    // Pick best matching voice
    const langCode = lang === 'hi' ? 'hi-IN' : 'en-IN';
    utterance.lang = langCode;

    if (this.voices.length > 0) {
      let voice = this.voices.find(v => v.lang === langCode || v.lang.startsWith(lang));
      if (!voice && lang === 'en') {
        voice = this.voices.find(v => v.lang.startsWith('en'));
      }
      if (voice) {
        utterance.voice = voice;
      }
    }

    utterance.onstart = () => {
      if (onStart) onStart();
    };

    utterance.onend = () => {
      this.currentUtterance = null;
      if (onEnd) onEnd();
    };

    utterance.onerror = (e) => {
      console.error("Speech error:", e);
      this.currentUtterance = null;
      if (onError) onError(e);
    };

    this.currentUtterance = utterance;
    this.synth.speak(utterance);
  }

  pause() {
    if (this.synth && this.synth.speaking) {
      if (this.synth.paused) {
        this.synth.resume();
        return false; // resumed
      } else {
        this.synth.pause();
        return true; // paused
      }
    }
    return false;
  }

  stop() {
    if (this.synth) {
      this.synth.cancel();
      this.currentUtterance = null;
    }
  }

  isSpeaking() {
    return this.synth ? this.synth.speaking : false;
  }

  /**
   * Listen for user speech (voice typing)
   */
  startListening(lang = 'en', onResult, onEnd, onError) {
    if (!this.recognition) {
      alert("Voice input is not supported in this browser. Please type your message.");
      return;
    }

    if (this.isListening) {
      this.stopListening();
      return;
    }

    this.recognition.lang = lang === 'hi' ? 'hi-IN' : 'en-IN';

    this.recognition.onstart = () => {
      this.isListening = true;
    };

    this.recognition.onresult = (event) => {
      const transcript = event.results[0][0].transcript;
      if (onResult) onResult(transcript);
    };

    this.recognition.onerror = (event) => {
      console.warn("Recognition error:", event.error);
      this.isListening = false;
      if (onError) onError(event.error);
    };

    this.recognition.onend = () => {
      this.isListening = false;
      if (onEnd) onEnd();
    };

    try {
      this.recognition.start();
    } catch (err) {
      console.error("Failed to start speech recognition", err);
    }
  }

  stopListening() {
    if (this.recognition && this.isListening) {
      this.recognition.stop();
      this.isListening = false;
    }
  }
}

window.SeniorSpeech = new SeniorSpeechEngine();
