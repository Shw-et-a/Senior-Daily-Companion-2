/**
 * Senior Daily Companion - Main Application Logic
 * Coordinates UI states, translations, voice speech, interactive wizards, and Gemini AI.
 */

// Application State
const state = {
  lang: localStorage.getItem("senior_lang") || "en",
  theme: localStorage.getItem("senior_theme") || "warm",
  fontSize: localStorage.getItem("senior_font_size") || "font-normal",
  activeTab: "companion",
  isSpeaking: false,
  isSpeechPaused: false,
  lastAiResponse: ""
};

// Quick helper to get localized string
function t(key) {
  const langTable = window.TRANSLATIONS[state.lang] || window.TRANSLATIONS["en"];
  return langTable[key] || window.TRANSLATIONS["en"][key] || key;
}

// ─────────────────────────────────────────────────────────────
// UI Initialization & Localization
// ─────────────────────────────────────────────────────────────
document.addEventListener("DOMContentLoaded", () => {
  applyTheme(state.theme);
  applyFontSize(state.fontSize);
  updateLocalization();
  setupEventListeners();
  renderGreeting();
  renderMedicines();
  renderHydration();
  checkApiStatus();
});

function applyTheme(theme) {
  state.theme = theme;
  localStorage.setItem("senior_theme", theme);
  document.body.classList.remove("theme-light", "theme-dark");
  if (theme === "light") document.body.classList.add("theme-light");
  if (theme === "dark") document.body.classList.add("theme-dark");

  const select = document.getElementById("contrast-select");
  if (select) select.value = theme;
}

function applyFontSize(sizeClass) {
  state.fontSize = sizeClass;
  localStorage.setItem("senior_font_size", sizeClass);
  document.body.classList.remove("font-normal", "font-large", "font-xlarge");
  document.body.classList.add(sizeClass);

  // Update active state on font size buttons
  document.querySelectorAll("[data-font-size]").forEach(btn => {
    if (btn.dataset.fontSize === sizeClass) {
      btn.classList.add("border-amber-600", "bg-amber-100", "dark:bg-amber-900");
    } else {
      btn.classList.remove("border-amber-600", "bg-amber-100", "dark:bg-amber-900");
    }
  });
}

function toggleLanguage(newLang) {
  state.lang = newLang;
  localStorage.setItem("senior_lang", newLang);
  updateLocalization();
  renderGreeting();
  renderMedicines();
  renderHydration();

  // If there was an AI response, announce language switch
  if (window.SeniorSpeech.isSpeaking()) {
    window.SeniorSpeech.stop();
    updateSpeechButtons(false);
  }
}

function updateLocalization() {
  // Update all elements with data-i18n attribute
  document.querySelectorAll("[data-i18n]").forEach(el => {
    const key = el.getAttribute("data-i18n");
    const text = t(key);
    if (text) el.innerHTML = text;
  });

  // Update placeholders
  document.querySelectorAll("[data-i18n-placeholder]").forEach(el => {
    const key = el.getAttribute("data-i18n-placeholder");
    const text = t(key);
    if (text) el.placeholder = text;
  });

  // Update active language button styling
  const enBtn = document.getElementById("lang-en-btn");
  const hiBtn = document.getElementById("lang-hi-btn");
  if (enBtn && hiBtn) {
    if (state.lang === "en") {
      enBtn.className = "senior-btn senior-btn-primary px-3 py-1 font-bold";
      hiBtn.className = "senior-btn senior-btn-secondary px-3 py-1";
    } else {
      hiBtn.className = "senior-btn senior-btn-primary px-3 py-1 font-bold";
      enBtn.className = "senior-btn senior-btn-secondary px-3 py-1";
    }
  }
}

// ─────────────────────────────────────────────────────────────
// Greeting & Daily Well-being
// ─────────────────────────────────────────────────────────────
function renderGreeting() {
  const now = new Date();
  const hour = now.getHours();
  let greetingKey = "greeting_morning";
  if (hour >= 12 && hour < 17) greetingKey = "greeting_afternoon";
  else if (hour >= 17 && hour < 21) greetingKey = "greeting_evening";
  else if (hour >= 21 || hour < 5) greetingKey = "greeting_night";

  const greetingEl = document.getElementById("daily-greeting-text");
  if (greetingEl) greetingEl.textContent = t(greetingKey);

  const dateEl = document.getElementById("daily-date-text");
  if (dateEl) {
    const options = { weekday: "long", year: "numeric", month: "long", day: "numeric" };
    const dateStr = now.toLocaleDateString(state.lang === "hi" ? "hi-IN" : "en-US", options);
    dateEl.textContent = `${t("todays_date_prefix")} ${dateStr}`;
  }
}

function renderHydration() {
  const countEl = document.getElementById("water-count-number");
  if (countEl) {
    countEl.textContent = window.HydrationTracker.count;
  }
}

// ─────────────────────────────────────────────────────────────
// Event Listeners & Tab Navigation
// ─────────────────────────────────────────────────────────────
function setupEventListeners() {
  // Language Switch
  document.getElementById("lang-en-btn")?.addEventListener("click", () => toggleLanguage("en"));
  document.getElementById("lang-hi-btn")?.addEventListener("click", () => toggleLanguage("hi"));

  // Font Size Buttons
  document.querySelectorAll("[data-font-size]").forEach(btn => {
    btn.addEventListener("click", (e) => {
      applyFontSize(e.currentTarget.dataset.fontSize);
    });
  });

  // Contrast Selector
  document.getElementById("contrast-select")?.addEventListener("change", (e) => {
    applyTheme(e.target.value);
  });

  // Tab Switching
  document.querySelectorAll("[data-tab-target]").forEach(tabBtn => {
    tabBtn.addEventListener("click", (e) => {
      switchTab(e.currentTarget.dataset.tabTarget);
    });
  });

  // Quick Action Tiles
  document.querySelectorAll("[data-quick-action]").forEach(tile => {
    tile.addEventListener("click", (e) => {
      const action = e.currentTarget.dataset.quickAction;
      handleQuickAction(action);
    });
  });

  // Hydration Button
  document.getElementById("btn-drink-water")?.addEventListener("click", () => {
    window.HydrationTracker.addGlass();
    renderHydration();
  });

  // Emergency SOS Modal
  const sosModal = document.getElementById("emergency-modal");
  document.getElementById("btn-sos-trigger")?.addEventListener("click", () => {
    sosModal.classList.remove("hidden");
    playWarningBeep();
  });
  document.getElementById("btn-close-sos")?.addEventListener("click", () => {
    sosModal.classList.add("hidden");
  });

  // API Key Settings Modal
  const apiModal = document.getElementById("api-modal");
  document.getElementById("btn-api-modal-trigger")?.addEventListener("click", () => {
    document.getElementById("api-key-input").value = window.GeminiService.getApiKey();
    apiModal.classList.remove("hidden");
  });
  document.getElementById("btn-close-api")?.addEventListener("click", () => {
    apiModal.classList.add("hidden");
  });
  document.getElementById("btn-save-api-key")?.addEventListener("click", () => {
    const val = document.getElementById("api-key-input").value;
    window.GeminiService.setApiKey(val);
    checkApiStatus();
    apiModal.classList.add("hidden");
    playCelebrationChime();
  });
  document.getElementById("btn-clear-api-key")?.addEventListener("click", () => {
    window.GeminiService.setApiKey("");
    document.getElementById("api-key-input").value = "";
    checkApiStatus();
  });

  // Chat Send & Voice
  document.getElementById("btn-chat-send")?.addEventListener("click", submitChatQuery);
  document.getElementById("chat-user-input")?.addEventListener("keydown", (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      submitChatQuery();
    }
  });

  // Voice Input (Microphone)
  const micBtn = document.getElementById("btn-voice-input");
  micBtn?.addEventListener("click", () => {
    if (window.SeniorSpeech.isListening) {
      window.SeniorSpeech.stopListening();
      micBtn.classList.remove("mic-active");
      micBtn.querySelector(".btn-label").textContent = t("btn_speak");
    } else {
      micBtn.classList.add("mic-active");
      micBtn.querySelector(".btn-label").textContent = t("btn_listening");
      window.SeniorSpeech.startListening(
        state.lang,
        (transcript) => {
          const input = document.getElementById("chat-user-input");
          input.value = transcript;
          micBtn.classList.remove("mic-active");
          micBtn.querySelector(".btn-label").textContent = t("btn_speak");
          submitChatQuery();
        },
        () => {
          micBtn.classList.remove("mic-active");
          micBtn.querySelector(".btn-label").textContent = t("btn_speak");
        },
        () => {
          micBtn.classList.remove("mic-active");
          micBtn.querySelector(".btn-label").textContent = t("btn_speak");
        }
      );
    }
  });

  // Speech Readout Buttons
  document.getElementById("btn-read-aloud")?.addEventListener("click", () => {
    if (state.lastAiResponse) {
      window.SeniorSpeech.speak(
        state.lastAiResponse,
        state.lang,
        () => updateSpeechButtons(true),
        () => updateSpeechButtons(false)
      );
    }
  });

  document.getElementById("btn-pause-speech")?.addEventListener("click", () => {
    const isPaused = window.SeniorSpeech.pause();
    state.isSpeechPaused = isPaused;
    document.getElementById("btn-pause-speech").textContent = isPaused ? "▶️ Resume Voice" : t("btn_pause_speech");
  });

  document.getElementById("btn-stop-speech")?.addEventListener("click", () => {
    window.SeniorSpeech.stop();
    updateSpeechButtons(false);
  });

  document.getElementById("btn-explain-simpler")?.addEventListener("click", () => {
    const currentInput = document.getElementById("chat-user-input").value;
    const prompt = state.lang === "hi"
      ? `कृपया इसे और भी आसान शब्दों में एक-एक कदम करके समझाएं:`
      : `Please explain this in even simpler, easier words with tiny steps:`;
    document.getElementById("chat-user-input").value = `${prompt} ${currentInput || state.lastAiResponse.slice(0, 100)}`;
    submitChatQuery();
  });

  // ─────────────────────────────────────────────────────────
  // Wi-Fi Wizard Triggers
  // ─────────────────────────────────────────────────────────
  document.getElementById("btn-wifi-light-green")?.addEventListener("click", () => {
    document.getElementById("wifi-green-result").classList.remove("hidden");
    document.getElementById("wifi-red-result").classList.add("hidden");
    playCelebrationChime();
  });

  document.getElementById("btn-wifi-light-red")?.addEventListener("click", () => {
    document.getElementById("wifi-red-result").classList.remove("hidden");
    document.getElementById("wifi-green-result").classList.add("hidden");
    playWarningBeep();
  });

  document.getElementById("btn-start-wifi-timer")?.addEventListener("click", () => {
    const timerDisplay = document.getElementById("wifi-timer-display");
    const timerBtn = document.getElementById("btn-start-wifi-timer");
    timerBtn.disabled = true;
    timerBtn.classList.add("opacity-50");

    window.WifiWizard.startRestartTimer(
      (secondsLeft) => {
        timerDisplay.textContent = `${t("wifi_timer_running")} ${secondsLeft}s`;
        timerDisplay.classList.remove("hidden");
      },
      () => {
        timerDisplay.innerHTML = `<span class="text-green-600 font-bold">${t("wifi_timer_done")}</span>`;
        timerBtn.disabled = false;
        timerBtn.classList.remove("opacity-50");
      }
    );
  });

  // ─────────────────────────────────────────────────────────
  // Scam Analyzer Trigger
  // ─────────────────────────────────────────────────────────
  document.getElementById("btn-run-scam-check")?.addEventListener("click", () => {
    const text = document.getElementById("scam-message-input").value;
    if (!text.trim()) {
      alert(state.lang === "hi" ? "कृपया पहले संदेश यहाँ लिखें।" : "Please paste a message first.");
      return;
    }
    const result = window.ScamAnalyzer.analyzeMessage(text, state.lang);
    renderScamResult(result);
  });

  // ─────────────────────────────────────────────────────────
  // Bill Explainer Trigger
  // ─────────────────────────────────────────────────────────
  document.getElementById("btn-run-bill-check")?.addEventListener("click", () => {
    const text = document.getElementById("bill-text-input").value;
    if (!text.trim()) return;

    // Direct inquiry to companion
    switchTab("companion");
    const prompt = state.lang === "hi"
      ? `कृपया इस बिल/पत्र को 3 आसान बिंदुओं में समझाएं (किसे देना है, कितना देना है, और कब तक देना है):\n\n${text}`
      : `Please explain this bill or letter in 3 simple points (Who it is to, How much to pay, and Due date):\n\n${text}`;
    document.getElementById("chat-user-input").value = prompt;
    submitChatQuery();
  });

  // ─────────────────────────────────────────────────────────
  // Medicine Add Form
  // ─────────────────────────────────────────────────────────
  document.getElementById("btn-add-medicine")?.addEventListener("click", () => {
    const nameInput = document.getElementById("new-med-name");
    const timeSelect = document.getElementById("new-med-time");
    if (nameInput && nameInput.value.trim()) {
      window.MedicineManager.addMedicine(nameInput.value, timeSelect.value);
      nameInput.value = "";
      renderMedicines();
    }
  });
}

function switchTab(tabId) {
  state.activeTab = tabId;
  document.querySelectorAll(".tab-pane").forEach(pane => {
    pane.classList.add("hidden");
  });
  const targetPane = document.getElementById(`tab-pane-${tabId}`);
  if (targetPane) targetPane.classList.remove("hidden");

  // Update active tab buttons
  document.querySelectorAll("[data-tab-target]").forEach(btn => {
    if (btn.dataset.tabTarget === tabId) {
      btn.className = "senior-btn senior-btn-primary px-4 py-2 font-bold shadow-md";
    } else {
      btn.className = "senior-btn senior-btn-secondary px-4 py-2";
    }
  });

  window.scrollTo({ top: 0, behavior: "smooth" });
}

function handleQuickAction(action) {
  switch (action) {
    case "wifi":
      switchTab("wifi");
      break;
    case "flight":
      switchTab("flight");
      break;
    case "scam":
      switchTab("scam");
      break;
    case "meds":
      switchTab("medicine");
      break;
    case "bills":
      switchTab("bills");
      break;
    case "whatsapp":
      switchTab("companion");
      document.getElementById("chat-user-input").value = state.lang === "hi"
        ? "व्हाट्सएप पर बच्चों या पोते-पोतियों को वीडियो कॉल कैसे करें?"
        : "How do I make a video call on WhatsApp?";
      submitChatQuery();
      break;
    case "pension":
      switchTab("companion");
      document.getElementById("chat-user-input").value = state.lang === "hi"
        ? "जीवन प्रमाण पत्र (Jeevan Pramaan Digital Life Certificate) घर बैठे कैसे जमा करें?"
        : "How do I submit my Digital Life Certificate (Jeevan Pramaan) from home?";
      submitChatQuery();
      break;
    default:
      switchTab("companion");
  }
}

// ─────────────────────────────────────────────────────────────
// Chat Execution & Rendering
// ─────────────────────────────────────────────────────────────
async function submitChatQuery() {
  const input = document.getElementById("chat-user-input");
  const query = (input.value || "").trim();
  if (!query) return;

  const thinkingEl = document.getElementById("chat-thinking");
  const responseCard = document.getElementById("chat-response-card");
  const responseBody = document.getElementById("chat-response-body");
  const speechControls = document.getElementById("speech-action-bar");

  // Show thinking indicator
  if (thinkingEl) thinkingEl.classList.remove("hidden");
  if (responseCard) responseCard.classList.add("hidden");
  if (speechControls) speechControls.classList.add("hidden");

  try {
    const result = await window.GeminiService.askCompanion(query, state.lang);
    state.lastAiResponse = result.text;

    // Hide thinking indicator
    if (thinkingEl) thinkingEl.classList.add("hidden");

    // Format and render text
    if (responseBody) {
      responseBody.innerHTML = formatAiResponse(result.text);
    }
    if (responseCard) responseCard.classList.remove("hidden");
    if (speechControls) speechControls.classList.remove("hidden");

    // Automatically read out response gently
    window.SeniorSpeech.speak(
      result.text,
      state.lang,
      () => updateSpeechButtons(true),
      () => updateSpeechButtons(false)
    );

    // Scroll to response smoothly
    responseCard.scrollIntoView({ behavior: "smooth", block: "start" });
  } catch (err) {
    if (thinkingEl) thinkingEl.classList.add("hidden");
    alert("Error getting response: " + err.message);
  }
}

function formatAiResponse(text) {
  // Convert markdown-style bullet points, numbers, bolding into accessible senior cards
  let html = text
    .replace(/\*\*(.*?)\*\*/g, '<strong class="font-bold text-amber-700 dark:text-amber-400">$1</strong>')
    .replace(/\n\n/g, '</p><p class="my-3 leading-relaxed">')
    .replace(/^(\d+\.)\s*(.*)$/gm, '<div class="flex items-start gap-3 my-3 p-3 rounded-xl bg-amber-50 dark:bg-slate-800 border border-amber-200 dark:border-slate-700"><span class="w-8 h-8 rounded-full bg-amber-500 text-white font-bold flex items-center justify-center flex-shrink-0 text-lg">$1</span><div class="pt-0.5">$2</div></div>');

  return `<p class="leading-relaxed text-lg sm:text-xl">${html}</p>`;
}

function updateSpeechButtons(isPlaying) {
  state.isSpeaking = isPlaying;
  const readBtn = document.getElementById("btn-read-aloud");
  const pauseBtn = document.getElementById("btn-pause-speech");
  const stopBtn = document.getElementById("btn-stop-speech");

  if (isPlaying) {
    if (readBtn) readBtn.classList.add("hidden");
    if (pauseBtn) pauseBtn.classList.remove("hidden");
    if (stopBtn) stopBtn.classList.remove("hidden");
  } else {
    if (readBtn) readBtn.classList.remove("hidden");
    if (pauseBtn) pauseBtn.classList.add("hidden");
    if (stopBtn) stopBtn.classList.add("hidden");
  }
}

// ─────────────────────────────────────────────────────────────
// Scam Checker UI
// ─────────────────────────────────────────────────────────────
function renderScamResult(result) {
  const resultCard = document.getElementById("scam-result-card");
  const meterFill = document.getElementById("scam-meter-fill");
  const titleEl = document.getElementById("scam-result-title");
  const reasonsEl = document.getElementById("scam-result-reasons");
  const actionEl = document.getElementById("scam-result-action");

  if (!resultCard) return;

  resultCard.classList.remove("hidden");
  titleEl.textContent = result.title;

  meterFill.style.width = `${result.score}%`;
  if (result.level === "danger") {
    meterFill.className = "h-4 rounded-full bg-red-600 transition-all duration-500";
    resultCard.className = "senior-card p-6 mt-6 border-4 border-red-600 bg-red-50 dark:bg-red-950/40";
  } else if (result.level === "caution") {
    meterFill.className = "h-4 rounded-full bg-yellow-500 transition-all duration-500";
    resultCard.className = "senior-card p-6 mt-6 border-4 border-yellow-500 bg-yellow-50 dark:bg-yellow-950/40";
  } else {
    meterFill.className = "h-4 rounded-full bg-green-600 transition-all duration-500";
    resultCard.className = "senior-card p-6 mt-6 border-4 border-green-600 bg-green-50 dark:bg-green-950/40";
  }

  reasonsEl.innerHTML = result.reasons.map(r => `<li class="my-2">${r}</li>`).join("");
  actionEl.textContent = result.action;

  resultCard.scrollIntoView({ behavior: "smooth", block: "center" });

  // Read verdict out loud
  window.SeniorSpeech.speak(`${result.title}. ${result.action}`, state.lang);
}

// ─────────────────────────────────────────────────────────────
// Medicine Checklist UI
// ─────────────────────────────────────────────────────────────
function renderMedicines() {
  const container = document.getElementById("medicine-list-container");
  if (!container) return;

  const meds = window.MedicineManager.medicines;
  const timeLabels = {
    morning: t("med_morning"),
    afternoon: t("med_afternoon"),
    evening: t("med_evening"),
    night: t("med_night")
  };

  const times = ["morning", "afternoon", "evening", "night"];
  let html = "";

  times.forEach(time => {
    const timeMeds = meds.filter(m => m.time === time);
    html += `
      <div class="mb-6 p-4 rounded-2xl bg-amber-50/70 dark:bg-slate-800/80 border border-amber-200 dark:border-slate-700">
        <h4 class="font-bold text-xl mb-3 text-amber-900 dark:text-amber-200 flex items-center gap-2">
          ⏰ ${timeLabels[time]}
        </h4>
    `;

    if (timeMeds.length === 0) {
      html += `<p class="text-stone-500 dark:text-stone-400 italic text-base">${t("med_empty")}</p>`;
    } else {
      timeMeds.forEach(med => {
        html += `
          <div class="flex items-center justify-between p-3 my-2 rounded-xl bg-white dark:bg-slate-900 border ${med.taken ? 'border-green-500 bg-green-50/50 dark:bg-green-950/30' : 'border-stone-300 dark:border-slate-700'}">
            <label class="flex items-center gap-3 cursor-pointer flex-1">
              <input type="checkbox" class="med-checkbox" ${med.taken ? 'checked' : ''} onchange="toggleMed('${med.id}')">
              <span class="text-xl ${med.taken ? 'line-through text-stone-400 dark:text-stone-500' : 'font-medium'}">${med.name}</span>
            </label>
            <button onclick="removeMed('${med.id}')" class="text-stone-400 hover:text-red-500 p-2 text-xl" title="Delete">✕</button>
          </div>
        `;
      });
    }

    html += `</div>`;
  });

  container.innerHTML = html;
}

window.toggleMed = function(id) {
  window.MedicineManager.toggleTaken(id);
  renderMedicines();
};

window.removeMed = function(id) {
  window.MedicineManager.removeMedicine(id);
  renderMedicines();
};

function checkApiStatus() {
  const statusEl = document.getElementById("api-status-indicator");
  if (!statusEl) return;
  if (window.GeminiService.hasApiKey()) {
    statusEl.innerHTML = `<span class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-sm font-bold bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200">🟢 Gemini 2.5 Active</span>`;
  } else {
    statusEl.innerHTML = `<span class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-sm font-bold bg-amber-100 text-amber-800 dark:bg-amber-900 dark:text-amber-200">🟡 Offline Knowledge Active</span>`;
  }
}
