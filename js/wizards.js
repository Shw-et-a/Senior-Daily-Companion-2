/**
 * Senior Daily Companion - Interactive Task Wizards
 * Contains specialized interactive workflows:
 * 1. Wi-Fi & TV Troubleshooter (Interactive Router & 30s Countdown Timer)
 * 2. Senior Flight Booking Assistant (Discounts & Wheelchair Guide)
 * 3. Suspicious Message & Scam Analyzer (Risk Meter & Practical Advice)
 * 4. Medicine Tracker & Hydration (Daily Checklists & Sound Chimes)
 * 5. Confusing Bill Explainer
 */

// Sound chime synthesizer using Web Audio API (Zero external audio files needed)
function playTone(freq, type = "sine", duration = 0.25) {
  try {
    const ctx = new (window.AudioContext || window.webkitAudioContext)();
    const osc = ctx.createOscillator();
    const gain = ctx.createGain();
    osc.type = type;
    osc.frequency.value = freq;
    osc.connect(gain);
    gain.connect(ctx.destination);
    osc.start();
    gain.gain.exponentialRampToValueAtTime(0.0001, ctx.currentTime + duration);
    osc.stop(ctx.currentTime + duration);
  } catch (e) {
    // Audio context may be restricted before user gesture
  }
}

function playCelebrationChime() {
  playTone(523.25, "sine", 0.15); // C5
  setTimeout(() => playTone(659.25, "sine", 0.15), 120); // E5
  setTimeout(() => playTone(783.99, "sine", 0.3), 240); // G5
}

function playWarningBeep() {
  playTone(330, "triangle", 0.2);
  setTimeout(() => playTone(260, "triangle", 0.3), 150);
}

// ─────────────────────────────────────────────────────────────
// 1. Wi-Fi & TV Troubleshooter
// ─────────────────────────────────────────────────────────────
class WifiWizard {
  constructor() {
    this.timerInterval = null;
    this.secondsLeft = 30;
  }

  startRestartTimer(onTick, onComplete) {
    this.stopTimer();
    this.secondsLeft = 30;
    playTone(440, "sine", 0.1);

    this.timerInterval = setInterval(() => {
      this.secondsLeft--;
      playTone(587.33, "sine", 0.05); // Subtle tick
      if (onTick) onTick(this.secondsLeft);

      if (this.secondsLeft <= 0) {
        this.stopTimer();
        playCelebrationChime();
        if (onComplete) onComplete();
      }
    }, 1000);
  }

  stopTimer() {
    if (this.timerInterval) {
      clearInterval(this.timerInterval);
      this.timerInterval = null;
    }
  }
}

// ─────────────────────────────────────────────────────────────
// 2. Suspicious Message & Scam Analyzer
// ─────────────────────────────────────────────────────────────
class ScamAnalyzer {
  analyzeMessage(text, lang = "en") {
    const raw = (text || "").toLowerCase();
    
    // High danger keywords
    const redFlags = [
      "electricity", "power cut", "disconnected tonight", "anydesk", "teamviewer",
      "rustdesk", "apk", "lottery", "kbc", "digital arrest", "police warrant",
      "customs parcel", "send otp", "share otp", "aadhaar verification",
      "pan blocked", "sim blocked", "won cash", "urgent money", "card blocked",
      "बिजली", "कनेक्शन कटेगा", "लॉटरी", "ओटीपी", "अरेस्ट", "डिजिटल अरेस्ट",
      "सिम ब्लॉक", "खाता बंद", "पैन कार्ड"
    ];

    // Moderate caution keywords
    const yellowFlags = [
      "click link", "update kyc", "refund", "prize", "job offer", "work from home",
      "urgent", "free gift", "claim now", "केवाईसी", "उपहार", "रिफंड"
    ];

    let foundRed = redFlags.filter(word => raw.includes(word));
    let foundYellow = yellowFlags.filter(word => raw.includes(word));

    if (foundRed.length > 0) {
      playWarningBeep();
      return {
        level: "danger",
        score: 95,
        title: lang === "hi" ? "🔴 सावधान! यह 99% धोखाधड़ी (Scam) है" : "🔴 DANGER: This is Almost Certainly a SCAM!",
        reasons: lang === "hi" ? [
          `संदेश में खतरनाक शब्द मिले: "${foundRed.slice(0, 2).join(", ")}"`,
          "असली सरकारी विभाग या बिजली कंपनियां कभी भी व्हाट्सएप पर धमकी नहीं भेजते।",
          "वे कभी भी AnyDesk जैसी ऐप्स डाउनलोड करने को नहीं कहते।"
        ] : [
          `Found high-risk scam triggers: "${foundRed.slice(0, 2).join(", ")}"`,
          "Official utility companies and banks NEVER threaten sudden cutoff over SMS/WhatsApp.",
          "They NEVER ask you to install remote screen apps or pay to a private mobile number."
        ],
        action: lang === "hi"
          ? "तुरंत इस संदेश को डिलीट करें। किसी भी लिंक या फोन नंबर पर बिल्कुल टच न करें। अगर कोई फोन करे तो तुरंत काट दें और 1930 पर शिकायत करें।"
          : "Delete this message immediately. Do NOT click links or call the number provided. If someone calls, hang up and dial 1930."
      };
    } else if (foundYellow.length > 0 || raw.includes("http") || raw.includes("bit.ly")) {
      return {
        level: "caution",
        score: 65,
        title: lang === "hi" ? "🟡 सावधानी बरतें: अज्ञात संदेश" : "🟡 CAUTION: Treat With Great Suspicion",
        reasons: lang === "hi" ? [
          "संदेश में अज्ञात लिंक या जल्दीबाज़ी करने का दबाव है।",
          "अपरिचित नंबरों से आए ऑफर्स पर कभी भरोसा न करें।"
        ] : [
          "Message contains an unknown web link or artificial urgency.",
          "Legitimate organizations do not pressure you to act within minutes."
        ],
        action: lang === "hi"
          ? "अपने परिवार के किसी सदस्य या बैंक की आधिकारिक शाखा से खुद पुष्टि करें। अनजान लिंक न खोलें।"
          : "Verify with a trusted family member or contact the official company customer care directly. Do not open the link."
      };
    } else {
      return {
        level: "safe",
        score: 15,
        title: lang === "hi" ? "🟢 कोई स्पष्ट खतरा नहीं मिला" : "🟢 No Immediate Red Flags Detected",
        reasons: lang === "hi" ? [
          "संदेश में सामान्य बातचीत के शब्द हैं।",
          "कोई पासवर्ड, बैंक पिन या संदिग्ध ऐप डाउनलोड करने का दबाव नहीं है।"
        ] : [
          "No aggressive scam keywords, banking threats, or remote app requests detected.",
          "Always remember: never share your 4-digit or 6-digit OTP with anyone."
        ],
        action: lang === "hi"
          ? "यदि यह आपके किसी परिचित का संदेश है तो सुरक्षित लगता है। फिर भी कभी बैंक पिन या ओटीपी साझा न करें।"
          : "Looks safe for normal reading. As always, keep your personal banking passwords strictly confidential."
      };
    }
  }
}

// ─────────────────────────────────────────────────────────────
// 3. Medicine Checklist Manager
// ─────────────────────────────────────────────────────────────
class MedicineManager {
  constructor() {
    this.storageKey = "senior_companion_medicines";
    this.medicines = this.loadMedicines();
  }

  getDefaults(lang = "en") {
    return [
      { id: "m1", time: "morning", name: lang === "hi" ? "बीपी (रक्तचाप) की गोली" : "Blood Pressure Tablet (e.g., Telmisartan)", taken: false },
      { id: "m2", time: "morning", name: lang === "hi" ? "मल्टीविटामिन / कैल्शियम" : "Calcium & Vitamin D3", taken: false },
      { id: "m3", time: "afternoon", name: lang === "hi" ? "दोपहर का खाना बाद दवा" : "Post-Lunch Tablet", taken: false },
      { id: "m4", time: "night", name: lang === "hi" ? "रात की दवा (हार्ट / शुगर)" : "Bedtime Tablet (e.g., Diabetes/Heart)", taken: false }
    ];
  }

  loadMedicines() {
    try {
      const saved = localStorage.getItem(this.storageKey);
      if (saved) {
        return JSON.parse(saved);
      }
    } catch (e) {}
    return this.getDefaults("en");
  }

  saveMedicines() {
    try {
      localStorage.setItem(this.storageKey, JSON.stringify(this.medicines));
    } catch (e) {}
  }

  toggleTaken(id) {
    const med = this.medicines.find(m => m.id === id);
    if (med) {
      med.taken = !med.taken;
      if (med.taken) {
        playCelebrationChime();
      } else {
        playTone(350, "sine", 0.15);
      }
      this.saveMedicines();
    }
    return this.medicines;
  }

  addMedicine(name, time = "morning") {
    if (!name || !name.trim()) return;
    const newMed = {
      id: "med_" + Date.now(),
      name: name.trim(),
      time: time,
      taken: false
    };
    this.medicines.push(newMed);
    this.saveMedicines();
    playCelebrationChime();
    return this.medicines;
  }

  removeMedicine(id) {
    this.medicines = this.medicines.filter(m => m.id !== id);
    this.saveMedicines();
    return this.medicines;
  }

  resetDaily() {
    this.medicines.forEach(m => m.taken = false);
    this.saveMedicines();
    return this.medicines;
  }
}

// ─────────────────────────────────────────────────────────────
// 4. Hydration Tracker
// ─────────────────────────────────────────────────────────────
class HydrationTracker {
  constructor() {
    this.storageKey = "senior_companion_water";
    this.count = this.loadCount();
  }

  loadCount() {
    try {
      const today = new Date().toDateString();
      const saved = JSON.parse(localStorage.getItem(this.storageKey) || "{}");
      if (saved.date === today) {
        return saved.count || 0;
      }
    } catch (e) {}
    return 0;
  }

  addGlass() {
    this.count++;
    try {
      const today = new Date().toDateString();
      localStorage.setItem(this.storageKey, JSON.stringify({ date: today, count: this.count }));
    } catch (e) {}
    playCelebrationChime();
    return this.count;
  }
}

window.WifiWizard = new WifiWizard();
window.ScamAnalyzer = new ScamAnalyzer();
window.MedicineManager = new MedicineManager();
window.HydrationTracker = new HydrationTracker();
