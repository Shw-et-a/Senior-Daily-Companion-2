# ☀️ Senior Daily Companion (वरिष्ठ दैनिक सहायक)

> **An intelligent, accessible, and trustworthy digital companion designed specifically for senior citizens.**  
> Helps elders navigate everyday challenges with ease, confidence, and independence — from fixing home Wi-Fi and booking flights with senior concessions to detecting online scams and tracking daily medications.

---

## 🌟 Key Senior-First Features

- 🔤 **Large, Legible Typography**: One-tap text resizing (`A`, `A+`, `A++` from 19px to 27px+).
- 🎨 **Aging-Eye Friendly Themes**:
  - **Warm & Cozy** (soft amber/cream to reduce blue light fatigue)
  - **High Contrast Light** (crisp black & white with bold borders)
  - **High Contrast Dark** (deep slate with vivid goldenrod highlights)
- 🌐 **Full Bilingual Support**: One-tap instant toggle between **English** and **हिन्दी (Hindi)** across all cards, buttons, tools, and speech engines.
- 🎤 **Voice First (Speak & Listen)**:
  - **Voice Input (Speech-to-Text)**: Speak naturally in English, Hindi, or Hinglish.
  - **Gentle Read Aloud (Text-to-Speech)**: Reads instructions out loud at a comfortable, patient pace (0.88x speed) with pause/stop controls.
- 📶 **Interactive Wi-Fi & TV Troubleshooter**:
  - Visual simulated router with LED light diagnostic indicators.
  - Interactive **30-second restart countdown timer** with audio ticks and completion chime.
  - TV "No Signal" remote control and HDMI input switch helper.
- ✈️ **Senior Flight Booking Guide**:
  - Step-by-step guidance on **Senior Citizen Concessions (6% to 10% off)**.
  - Free wheelchair assistance selection guide.
  - Front-aisle seat selection tips and cabin medicine checklist.
- 🛡️ **Suspicious Message & Scam Checker**:
  - Paste any SMS, WhatsApp forward, or email.
  - Instant **Risk Meter** (Safe 🟢 / Caution 🟡 / Dangerous Scam 🔴) with practical plain-language advice.
  - Direct 1-tap call to **National Cybercrime Helpline 1930**.
- 💊 **Daily Medicine & Hydration Checklist**:
  - Morning, afternoon, evening, and night pill tracking with audio chimes.
  - Interactive water glass counter.
- 🆘 **One-Tap Emergency SOS**:
  - Quick dial to Ambulance (108), Police (100), National Emergency (112), and Senior Citizen Helpline (14567).
- 🤖 **Google Gemini 2.5 AI Powered**:
  - Step-by-step micro-instructions, color-coded visual cues, and "Explain More Simply" button.
  - Works with a free Gemini API key, plus has an extensive offline knowledge base so it never leaves the user stranded!

---

## 🚀 How to Run Locally (Instant - No Setup Required!)

You do **not** need to install Python, Node.js, or any complex tools.

1. Simply double-click **`index.html`** in your file explorer.
2. It will open immediately in your web browser (Chrome, Edge, Safari, or Firefox)!

*(Optional: If you prefer a local web server, run `python -m http.server 8000` or `npx serve` and open `http://localhost:8000`)*

---

## 🌐 How to Deploy to GitHub Pages (Free & Automatic)

This website is 100% ready for **GitHub Pages** with zero configuration!

### Option A: 1-Click via GitHub Repository Settings
1. Push your repository to GitHub:
   ```bash
   git add .
   git commit -m "Deploy Senior Daily Companion"
   git push origin main
   ```
2. Go to your repository on **GitHub.com**.
3. Click on **Settings** (gear icon) ➔ **Pages** (in the left sidebar).
4. Under **Build and deployment** ➔ **Branch**:
   - Select **`main`** (or `master`).
   - Leave the folder as **`/ (root)`**.
   - Click **Save**.
5. In about 30 seconds, your site is live at:  
   `https://<your-github-username>.github.io/<repo-name>/`!

### Option B: Automatic via GitHub Actions
We have included `.github/workflows/deploy.yml`. In your repo settings:
- Go to **Settings** ➔ **Pages** ➔ under **Source**, select **GitHub Actions**.
- Every time you push a change, GitHub will automatically publish the website!

---

## 🔑 Setting up Google Gemini AI (Optional)

The website includes an extensive built-in knowledge base for common senior questions. To enable full conversational AI for custom questions:

1. Visit [Google AI Studio](https://aistudio.google.com/) and click **Get API Key** (it is free).
2. On the website, click the **🔑 AI Setup** button in the top navigation bar.
3. Paste your key and click **Save Key**.
4. Your key is stored securely in your own browser (`localStorage`) and is never sent to any third-party server.

---

## 📁 Project Structure

```
senior_companion/
├── .github/
│   └── workflows/
│       └── deploy.yml        # GitHub Actions automated deployment
├── css/
│   └── styles.css            # Accessible styles, contrast themes & animations
├── js/
│   ├── translations.js       # Complete English & Hindi localization
│   ├── speech.js             # Web Speech API (TTS & STT with senior tuning)
│   ├── gemini.js             # Google Gemini 2.5 Flash & offline knowledge base
│   ├── wizards.js            # Wi-Fi timer, scam analyzer, medicine tracker
│   └── app.js                # Core state & UI event orchestration
├── index.html                # Master responsive senior-first web app
├── README.md                 # Documentation & deployment guide
└── .gitignore
```

---

## ❤️ Dedicated to Senior Independence

Built with patience, clarity, and respect. Technology should empower everyone, regardless of age.
