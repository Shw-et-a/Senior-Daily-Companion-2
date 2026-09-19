/**
 * Senior Daily Companion - Complete Bilingual Localization (EN & HI)
 */

const TRANSLATIONS = {
  en: {
    // App Header
    app_title: "Senior Daily Companion",
    app_tagline: "Your caring, patient guide for everyday tasks",
    font_size_label: "Text Size",
    contrast_label: "Contrast",
    contrast_warm: "Warm & Cozy",
    contrast_light: "High Contrast Light",
    contrast_dark: "High Contrast Dark",
    language_label: "Language",
    api_key_btn: "🔑 AI Setup",
    sos_btn: "🆘 Emergency SOS",

    // Time & Daily Greeting
    greeting_morning: "Good Morning! 🌅",
    greeting_afternoon: "Good Afternoon! ☀️",
    greeting_evening: "Good Evening! 🌆",
    greeting_night: "Good Night! 🌙",
    greeting_subtitle: "Take your time. I am right here beside you to help.",
    todays_date_prefix: "Today is",
    wellbeing_water_prompt: "Hydration check: Have you had a glass of fresh water recently?",
    wellbeing_water_btn: "💧 Drank a Glass!",
    wellbeing_water_count: "Glasses today:",

    // Daily Proactive Cards
    card_tip_title: "💡 Daily Comfort Tip",
    card_tip_text: "Rest your eyes for 20 seconds every 20 minutes. Look out the window at something green and far away.",
    card_scam_title: "⚠️ Today's Scam Warning",
    card_scam_text: "Beware of calls or messages saying 'Your electricity will be disconnected tonight'. Real utility companies never send personal WhatsApp threats or ask for remote access apps like AnyDesk.",
    card_scam_btn: "Check a Suspicious Message",

    // Navigation Tabs / Main Actions
    tab_companion: "💬 Ask Companion",
    tab_wifi: "📶 Fix Wi-Fi & TV",
    tab_flight: "✈️ Book Flights",
    tab_scam: "🛡️ Scam Checker",
    tab_medicine: "💊 Medicine Tracker",
    tab_bills: "📄 Explain a Bill",

    // Quick Action Tiles
    quick_tiles_title: "What would you like help with right now?",
    quick_tiles_subtitle: "Tap any large button below — no typing required!",
    tile_wifi: "📶 Fix My Wi-Fi",
    tile_wifi_desc: "Router lights & internet connection",
    tile_tv: "📺 Fix TV 'No Signal'",
    tile_tv_desc: "Remote control & HDMI inputs",
    tile_flight: "✈️ Book a Flight",
    tile_flight_desc: "Senior discount & wheelchair help",
    tile_scam: "🛡️ Check Suspicious SMS",
    tile_scam_desc: "Find out if a message is a scam",
    tile_meds: "💊 Medicine Reminders",
    tile_meds_desc: "Check off your daily tablets",
    tile_whatsapp: "📱 WhatsApp Video Call",
    tile_whatsapp_desc: "How to call children & grandchildren",
    tile_bills: "🧾 Understand My Bill",
    tile_bills_desc: "Simplify confusing numbers & dates",
    tile_pension: "📜 Life Certificate (Jeevan Pramaan)",
    tile_pension_desc: "Step-by-step digital submission",

    // Companion Chat
    chat_header: "Talk with your Companion",
    chat_sub: "Ask any question in simple words. You can type or tap the microphone to speak.",
    chat_placeholder: "e.g., How do I order medicines on PharmEasy? or Why is my phone sound low?",
    btn_send: "Send Question",
    btn_speak: "Speak",
    btn_listening: "Listening... Speak now",
    btn_read_aloud: "🔊 Read Out Loud",
    btn_pause_speech: "⏸️ Pause Voice",
    btn_stop_speech: "⏹️ Stop Voice",
    btn_simpler: "🔄 Explain More Simply",
    btn_step_done: "✅ Got it! Next Step",
    ai_thinking: "Thinking carefully for you... Please wait a moment ⏳",
    badge_visual_cue: "👁️ Look for this on your screen:",
    badge_safety_tip: "🔒 Safety Note:",

    // Wi-Fi & TV Wizard
    wifi_wizard_title: "Wi-Fi & Internet Troubleshooter",
    wifi_wizard_sub: "We will check your home internet together, one simple step at a time.",
    wifi_step1_title: "Step 1: Check your Wi-Fi Box (Router)",
    wifi_step1_desc: "Look at your Wi-Fi box. Do you see lights on it? Make sure the black power plug in the wall switch is turned ON.",
    wifi_step2_title: "Step 2: Check the Internet Light Color",
    wifi_step2_desc: "Find the light with a small globe or 'Internet' sign. Is it Green/Blue or Red/Orange?",
    wifi_step2_green: "🟢 It is Green or Blue",
    wifi_step2_red: "🔴 It is Red, Orange, or Off",
    wifi_step3_title: "Step 3: The 30-Second Refresh Trick",
    wifi_step3_desc: "Turn off the wall switch of the Wi-Fi box. Wait 30 seconds before turning it back on. Use our timer below!",
    wifi_timer_btn: "Start 30-Second Countdown",
    wifi_timer_running: "Waiting patiently... seconds left:",
    wifi_timer_done: "🎉 Done! Now turn the switch back ON. Wait 2 minutes for the green light.",
    wifi_phone_step: "Step 4: Check your Phone or Tablet",
    wifi_phone_desc: "Swipe down from the top of your phone screen. Tap the Wi-Fi icon off, wait 5 seconds, and tap it back on.",

    // TV Troubleshooter
    tv_wizard_title: "TV 'No Signal' Helper",
    tv_step1: "Grab your TV Remote (not the set-top box remote).",
    tv_step2: "Look for a button named 'Source', 'Input', or a square with an arrow pointing inside 🔲➡️.",
    tv_step3: "Press that button and select 'HDMI 1' or 'HDMI 2' where your cable box is plugged in.",

    // Flight Wizard
    flight_wizard_title: "Senior Flight Booking Guide",
    flight_wizard_sub: "Everything you need to book comfortably with zero stress.",
    flight_discount_title: "1. Senior Citizen Concession (Up to 6% - 10% Off Base Fare)",
    flight_discount_desc: "Air India, IndiGo, and SpiceJet offer senior discounts for travelers aged 60+. You must carry a government photo ID (Aadhaar, Senior Citizen Card, or Passport) at the airport.",
    flight_wheelchair_title: "2. Free Wheelchair Assistance",
    flight_wheelchair_desc: "You can request free wheelchair help right when booking online or by calling the airline. Select: 'Ramp Wheelchair' (if you can walk a few steps into the aircraft) or 'Step Wheelchair' (if you need help to your seat).",
    flight_seat_title: "3. Best Seat Selection",
    flight_seat_desc: "Always choose an Aisle Seat near the front of the aircraft (rows 2 to 7). It makes walking to the lavatory and boarding/deboarding much easier.",
    flight_baggage_title: "4. Cabin Baggage & Medications",
    flight_baggage_desc: "Keep all your daily medicines and doctor prescriptions in your small cabin handbag — NEVER put essential medications in check-in luggage!",

    // Scam Checker Tool
    scam_tool_title: "Suspicious Message & Scam Checker",
    scam_tool_sub: "Paste any SMS, WhatsApp message, or email you received. We will tell you if it is safe or a trap.",
    scam_placeholder: "Paste or type the suspicious message here... (e.g. 'Dear customer your electricity bill is unpaid, call 98765...')",
    scam_btn_check: "🔍 Analyze Message Safety",
    scam_result_safe: "🟢 LIKELY SAFE",
    scam_result_caution: "🟡 USE CAUTION",
    scam_result_danger: "🔴 DANGEROUS SCAM DETECTED",
    scam_helpline_text: "National Cybercrime Reporting Helpline: Call 1930 (Toll-Free)",

    // Medicine Tracker
    med_title: "Daily Medicine Checklist",
    med_sub: "Keep track of your morning, afternoon, and night tablets.",
    med_morning: "Morning (After Breakfast)",
    med_afternoon: "Afternoon (After Lunch)",
    med_evening: "Evening (With Tea / Snack)",
    med_night: "Night (Before Bed)",
    med_add_placeholder: "Add a new tablet or medicine name...",
    med_add_btn: "Add Medicine",
    med_empty: "No medicines added for this time yet.",

    // Bill Explainer
    bill_title: "Explain a Confusing Bill or Letter",
    bill_sub: "Paste the text of your electricity, water, credit card, or medical bill.",
    bill_placeholder: "Paste the bill text or numbers here...",
    bill_analyze_btn: "Simplify This Bill",

    // Emergency Modal
    sos_modal_title: "🆘 Emergency Assistance",
    sos_modal_sub: "Tap any number below to call immediately from your device.",
    sos_ambulance: "🚑 Ambulance: 108",
    sos_police: "🚔 Police: 100",
    sos_senior: "🧓 National Senior Citizen Helpline: 14567",
    sos_cyber: "🛡️ Cybercrime Helpline (Fraud/Scams): 1930",
    sos_general: "🚨 All-in-One National Emergency: 112",
    sos_close: "Close",

    // API Key Modal
    api_modal_title: "Google Gemini AI Settings",
    api_modal_sub: "Enter your free Gemini API key to activate full live AI responses.",
    api_key_placeholder: "Paste your Gemini API key (AIzaSy...)",
    api_key_save: "Save Key",
    api_key_clear: "Remove Key",
    api_key_note: "Your key stays safely stored in your own browser (localStorage). You can get a free key from Google AI Studio (aistudio.google.com).",
    api_key_active: "✅ Gemini AI is active and connected!",
    api_key_inactive: "ℹ️ Running in Offline Knowledge Mode (Add API key for live custom AI).",

    // Footer
    footer_text: "Built with love and care for Senior Citizens • 100% Free & Accessible • Works on Phones, Tablets & Computers"
  },

  hi: {
    // App Header
    app_title: "वरिष्ठ दैनिक सहायक",
    app_tagline: "रोज़मर्रा के कामों में आपका धैर्यवान और मददगार साथी",
    font_size_label: "अक्षर का आकार",
    contrast_label: "रंग और चमक",
    contrast_warm: "सुखद व गर्म",
    contrast_light: "अधिक स्पष्ट (उजाला)",
    contrast_dark: "डार्क मोड (रात)",
    language_label: "भाषा",
    api_key_btn: "🔑 AI सेटअप",
    sos_btn: "🆘 आपातकालीन SOS",

    // Time & Daily Greeting
    greeting_morning: "शुभ प्रभात! 🌅",
    greeting_afternoon: "शुभ दोपहर! ☀️",
    greeting_evening: "शुभ संध्या! 🌆",
    greeting_night: "शुभ रात्रि! 🌙",
    greeting_subtitle: "बिल्कुल चिंता न करें। मैं हर कदम पर आपकी मदद के लिए उपस्थित हूँ।",
    todays_date_prefix: "आज का दिन है",
    wellbeing_water_prompt: "स्वास्थ्य जांच: क्या आपने अभी ताज़ा पानी पिया है?",
    wellbeing_water_btn: "💧 एक गिलास पानी पिया!",
    wellbeing_water_count: "आज पिए गए गिलास:",

    // Daily Proactive Cards
    card_tip_title: "💡 आज का स्वास्थ्य सुझाव",
    card_tip_text: "हर 20 मिनट बाद 20 सेकंड के लिए अपनी आंखों को आराम दें। खिड़की से बाहर किसी दूर की हरी चीज़ को देखें।",
    card_scam_title: "⚠️ आज की ठगी (धोखाधड़ी) से सावधान",
    card_scam_text: "यदि कोई फोन या संदेश कहे कि 'आज रात आपकी बिजली काट दी जाएगी', तो घबराएं नहीं। बिजली विभाग कभी भी व्यक्तिगत व्हाट्सएप पर धमकी नहीं देता और न ही AnyDesk ऐप डाउनलोड करने को कहता है।",
    card_scam_btn: "संदेश की जांच करें",

    // Navigation Tabs / Main Actions
    tab_companion: "💬 सहायक से पूछें",
    tab_wifi: "📶 वाई-फाई व टीवी ठीक करें",
    tab_flight: "✈️ फ्लाइट टिकट बुक करें",
    tab_scam: "🛡️ ठगी जांच केंद्र",
    tab_medicine: "💊 दवाई डायरी",
    tab_bills: "📄 बिल समझें",

    // Quick Action Tiles
    quick_tiles_title: "आज मैं आपकी क्या सहायता कर सकता हूँ?",
    quick_tiles_subtitle: "नीचे दिए गए बड़े बटन दबाएं — लिखने की कोई जरूरत नहीं!",
    tile_wifi: "📶 वाई-फाई ठीक करें",
    tile_wifi_desc: "राउटर की लाइट और इंटरनेट कनेक्शन",
    tile_tv: "📺 टीवी 'No Signal' ठीक करें",
    tile_tv_desc: "रिमोट कंट्रोल व HDMI इनपुट",
    tile_flight: "✈️ फ्लाइट (हवाई) टिकट बुक करें",
    tile_flight_desc: "वरिष्ठ नागरिक छूट व व्हीलचेयर सुविधा",
    tile_scam: "🛡️ संदिग्ध संदेश (SMS) जांचें",
    tile_scam_desc: "पता करें कि कोई संदेश असली है या धोखा",
    tile_meds: "💊 दवाई अनुस्मारक (रिमाइंडर)",
    tile_meds_desc: "अपनी दैनिक गोलियों का हिसाब रखें",
    tile_whatsapp: "📱 व्हाट्सएप वीडियो कॉल करें",
    tile_whatsapp_desc: "बच्चों और पोते-पोतियों को कॉल करने का तरीका",
    tile_bills: "🧾 बिजली/फोन बिल समझें",
    tile_bills_desc: "उलझाने वाले अंकों और अंतिम तारीख को आसान बनाएं",
    tile_pension: "📜 जीवन प्रमाण पत्र (Jeevan Pramaan)",
    tile_pension_desc: "घर बैठे डिजिटल प्रमाण पत्र जमा करने के चरण",

    // Companion Chat
    chat_header: "अपने सहायक से बातचीत करें",
    chat_sub: "कोई भी प्रश्न सीधे सरल शब्दों में पूछें। आप बोल भी सकते हैं और लिख भी सकते हैं।",
    chat_placeholder: "उदा: फोन पर दवाई कैसे मंगाएं? या फोन की आवाज़ कैसे बढ़ाएं?",
    btn_send: "प्रश्न पूछें",
    btn_speak: "बोलें",
    btn_listening: "सुन रहा हूँ... अब बोलिए",
    btn_read_aloud: "🔊 बोलकर सुनाएं",
    btn_pause_speech: "⏸️ आवाज़ रोकें",
    btn_stop_speech: "⏹️ आवाज़ बंद करें",
    btn_simpler: "🔄 और आसान शब्दों में बताएं",
    btn_step_done: "✅ समझ गया! अगला कदम",
    ai_thinking: "आपके लिए सरल और सटीक उत्तर तैयार कर रहा हूँ... कृपया प्रतीक्षा करें ⏳",
    badge_visual_cue: "👁️ अपनी स्क्रीन पर यह देखें:",
    badge_safety_tip: "🔒 सुरक्षा नियम:",

    // Wi-Fi & TV Wizard
    wifi_wizard_title: "वाई-फाई व इंटरनेट समस्या निवारण",
    wifi_wizard_sub: "हम मिलकर आपके इंटरनेट को एक-एक सरल चरण में ठीक करेंगे।",
    wifi_step1_title: "चरण 1: अपने वाई-फाई बॉक्स (राउटर) को देखें",
    wifi_step1_desc: "अपने वाई-फाई बॉक्स को देखें। क्या उस पर लाइटें जल रही हैं? दीवार पर लगे काले प्लग का स्विच ऑन है या नहीं, यह सुनिश्चित करें।",
    wifi_step2_title: "चरण 2: इंटरनेट लाइट का रंग देखें",
    wifi_step2_desc: "उस लाइट को खोजें जिस पर छोटा ग्लोब (पृथ्वी) या 'Internet' लिखा हो। क्या यह हरी/नीली है या लाल/नारंगी?",
    wifi_step2_green: "🟢 हरी या नीली बत्ती जल रही है",
    wifi_step2_red: "🔴 लाल/नारंगी बत्ती है या बंद है",
    wifi_step3_title: "चरण 3: 30-सेकंड का रीस्टार्ट उपाय",
    wifi_step3_desc: "वाई-फाई बॉक्स का मुख्य स्विच बंद करें। फिर 30 सेकंड प्रतीक्षा करें और दोबारा चालू करें। नीचे टाइमर का उपयोग करें!",
    wifi_timer_btn: "30-सेकंड उल्टी गिनती शुरू करें",
    wifi_timer_running: "प्रतीक्षा करें... शेष सेकंड:",
    wifi_timer_done: "🎉 समय पूरा हुआ! अब स्विच चालू करें और 2 मिनट में हरी लाइट आने दें।",
    wifi_phone_step: "चरण 4: अपना फोन या टैबलेट देखें",
    wifi_phone_desc: "अपने फोन की स्क्रीन को ऊपर से नीचे स्वाइप करें। वाई-फाई का निशान 5 सेकंड बंद करें और फिर चालू करें।",

    // TV Troubleshooter
    tv_wizard_title: "टीवी 'No Signal' ठीक करें",
    tv_step1: "अपने मुख्य टीवी का रिमोट लें (सेट-टॉप बॉक्स वाला नहीं)।",
    tv_step2: "रिमोट पर 'Source', 'Input' या तीर वाले चौकोर निशान (🔲➡️) का बटन खोजें।",
    tv_step3: "उस बटन को दबाएं और 'HDMI 1' या 'HDMI 2' चुनें जहाँ आपकी केबल लगी है।",

    // Flight Wizard
    flight_wizard_title: "वरिष्ठ नागरिक हवाई यात्रा मार्गदर्शिका",
    flight_wizard_sub: "बिना किसी तनाव के आसानी से टिकट बुक करने के नियम।",
    flight_discount_title: "1. वरिष्ठ नागरिक छूट (किराये में 6% से 10% तक की छूट)",
    flight_discount_desc: "Air India, IndiGo और SpiceJet 60 वर्ष से अधिक आयु के वरिष्ठ नागरिकों को विशेष छूट देते हैं। हवाई अड्डे पर आधार कार्ड या पहचान पत्र साथ रखना अनिवार्य है।",
    flight_wheelchair_title: "2. मुफ्त व्हीलचेयर (Wheelchair) सुविधा",
    flight_wheelchair_desc: "आप टिकट बुक करते समय या एयरलाइन को फोन करके मुफ्त व्हीलचेयर मांग सकते हैं। 'रैंप व्हीलचेयर' (यदि आप कुछ कदम चल सकते हैं) या 'स्टेप व्हीलचेयर' का विकल्प चुनें।",
    flight_seat_title: "3. सबसे आरामदायक सीट का चयन",
    flight_seat_desc: "हमेशा विमान के आगे के हिस्से में गलियारे (Aisle) वाली सीट चुनें (पंक्ति 2 से 7)। इससे शौचालय जाना और चढ़ना-उतरना बहुत आसान रहता है।",
    flight_baggage_title: "4. दवाइयां और ज़रूरी सामान",
    flight_baggage_desc: "अपनी सभी ज़रूरी दैनिक दवाइयां और डॉक्टर का पर्चा अपने छोटे हैंडबैग में रखें — इसे कभी भी बड़े चेक-इन बैग में न डालें!",

    // Scam Checker Tool
    scam_tool_title: "संदिग्ध संदेश व ठगी पहचान केंद्र",
    scam_tool_sub: "आपको आया कोई भी SMS या व्हाट्सएप संदेश यहाँ डालें। हम बताएंगे कि यह सुरक्षित है या धोखा।",
    scam_placeholder: "संदेश यहाँ पेस्ट करें या लिखें... (जैसे: 'बिजली बिल नहीं भरा तो आज कनेक्शन कटेगा...')",
    scam_btn_check: "🔍 संदेश की सुरक्षा जांचें",
    scam_result_safe: "🟢 सुरक्षित लगता है",
    scam_result_caution: "🟡 सावधानी बरतें",
    scam_result_danger: "🔴 खतरनाक ठगी (Scam) का अंदेशा!",
    scam_helpline_text: "राष्ट्रीय साइबर अपराध हेल्पलाइन: 1930 (निःशुल्क टोल-फ्री)",

    // Medicine Tracker
    med_title: "दैनिक दवाई डायरी",
    med_sub: "सुबह, दोपहर और रात की दवाइयों का पूरा हिसाब रखें।",
    med_morning: "सुबह (नाश्ते के बाद)",
    med_afternoon: "दोपहर (दोपहर के खाने के बाद)",
    med_evening: "शाम (चाय/नाश्ते के साथ)",
    med_night: "रात (सोने से पहले)",
    med_add_placeholder: "दवाई का नाम लिखें...",
    med_add_btn: "दवाई जोड़ें",
    med_empty: "इस समय के लिए अभी कोई दवाई दर्ज नहीं है।",

    // Bill Explainer
    bill_title: "उलझाने वाला बिल या पत्र समझें",
    bill_sub: "बिजली, पानी, फोन या अस्पताल के बिल के मुख्य शब्द यहाँ डालें।",
    bill_placeholder: "बिल का विवरण या राशि यहाँ पेस्ट करें...",
    bill_analyze_btn: "बिल को सरल बनाएं",

    // Emergency Modal
    sos_modal_title: "🆘 आपातकालीन सहायता (Emergency)",
    sos_modal_sub: "तुरंत कॉल करने के लिए किसी भी नंबर पर टच करें।",
    sos_ambulance: "🚑 एम्बुलेंस (Ambulance): 108",
    sos_police: "🚔 पुलिस (Police): 100",
    sos_senior: "🧓 राष्ट्रीय वरिष्ठ नागरिक हेल्पलाइन: 14567",
    sos_cyber: "🛡️ साइबर अपराध / फ्रॉड हेल्पलाइन: 1930",
    sos_general: "🚨 राष्ट्रीय आपातकालीन सेवा: 112",
    sos_close: "बंद करें",

    // API Key Modal
    api_modal_title: "Google Gemini AI सेटिंग्स",
    api_modal_sub: "लाइव AI प्रतिक्रियाओं के लिए अपनी निःशुल्क Gemini API Key दर्ज करें।",
    api_key_placeholder: "अपनी Gemini API Key यहाँ पेस्ट करें (AIzaSy...)",
    api_key_save: "कुंजी सुरक्षित करें",
    api_key_clear: "कुंजी हटाएं",
    api_key_note: "आपकी कुंजी केवल आपके ब्राउज़र में सुरक्षित रहती है। आप Google AI Studio (aistudio.google.com) से मुफ्त कुंजी प्राप्त कर सकते हैं।",
    api_key_active: "✅ Gemini AI सक्रिय है और जुड़ा हुआ है!",
    api_key_inactive: "ℹ️ ऑफलाइन मोड में चल रहा है (लाइव AI के लिए अपनी API Key जोड़ें)।",

    // Footer
    footer_text: "वरिष्ठ नागरिकों के लिए प्रेम और देखभाल से निर्मित • 100% निःशुल्क और सुगम • फोन, टैबलेट और कंप्यूटर पर उपलब्ध"
  }
};

window.TRANSLATIONS = TRANSLATIONS;
