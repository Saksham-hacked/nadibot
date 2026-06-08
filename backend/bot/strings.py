"""
Trilingual string table – English + Hindi + Marathi.
All user-facing text lives here. Never hardcode strings in handlers.
"""
from __future__ import annotations
from typing import Literal

Lang = Literal["en", "hi", "mr"]


STRINGS: dict[str, dict[Lang, str]] = {
    # ── Onboarding ──────────────────────────────────────────────────────────
    "welcome": {
        "en": (
            "🌊 *Welcome to NadiBot!*\n\n"
            "I help you report water problems in your area – broken pipes, "
            "dirty water, flooding, dry taps, and more.\n\n"
            "Your complaint goes directly to the right authority.\n\n"
            "Please choose your language:"
        ),
        "hi": (
            "🌊 *नदीबॉट में आपका स्वागत है!*\n\n"
            "मैं आपके क्षेत्र की पानी की समस्याएं दर्ज करने में मदद करता हूँ – "
            "टूटी पाइप, गंदा पानी, बाढ़, सूखे नल, और बहुत कुछ।\n\n"
            "आपकी शिकायत सीधे सही विभाग तक पहुंचेगी।\n\n"
            "कृपया अपनी भाषा चुनें:"
        ),
        "mr": (
            "🌊 *नदीबॉटमध्ये आपले स्वागत आहे!*\n\n"
            "मी तुमच्या परिसरातील पाण्याच्या समस्या नोंदवण्यास मदत करतो – "
            "तुटलेले पाईप, दूषित पाणी, पूर, कोरडे नळ, आणि बरेच काही.\n\n"
            "तुमची तक्रार थेट योग्य विभागाकडे जाईल.\n\n"
            "कृपया तुमची भाषा निवडा:"
        ),
    },
    "lang_set": {
        "en": "✅ Language set to *English*. Let's begin!",
        "hi": "✅ भाषा *हिंदी* सेट कर दी गई है। चलिए शुरू करते हैं!",
        "mr": "✅ भाषा *मराठी* सेट केली आहे. चला सुरू करूया!",
    },

    # ── Main menu ───────────────────────────────────────────────────────────
    "main_menu": {
        "en": (
            "What would you like to do?\n\n"
            "📋 *Report* – File a new water complaint\n"
            "📊 *My Reports* – See your past complaints\n"
            "🌐 *Language* – Change language"
        ),
        "hi": (
            "आप क्या करना चाहते हैं?\n\n"
            "📋 *शिकायत करें* – नई पानी की शिकायत दर्ज करें\n"
            "📊 *मेरी शिकायतें* – पिछली शिकायतें देखें\n"
            "🌐 *भाषा* – भाषा बदलें"
        ),
        "mr": (
            "तुम्हाला काय करायचे आहे?\n\n"
            "📋 *तक्रार करा* – नवीन पाण्याची तक्रार नोंदवा\n"
            "📊 *माझ्या तक्रारी* – मागील तक्रारी पाहा\n"
            "🌐 *भाषा* – भाषा बदला"
        ),
    },
    "btn_report": {
        "en": "📋 Report a Problem",
        "hi": "📋 समस्या दर्ज करें",
        "mr": "📋 समस्या नोंदवा",
    },
    "btn_my_reports": {
        "en": "📊 My Reports",
        "hi": "📊 मेरी शिकायतें",
        "mr": "📊 माझ्या तक्रारी",
    },
    "btn_language": {
        "en": "🌐 Change Language",
        "hi": "🌐 भाषा बदलें",
        "mr": "🌐 भाषा बदला",
    },

    # ── Complaint flow ───────────────────────────────────────────────────────
    "step_text": {
        "en": (
            "📝 *Step 1 of 4 – Describe the problem*\n\n"
            "Type what is wrong with the water in your area.\n"
            "_(You can skip this if you are sending a photo or voice note)_"
        ),
        "hi": (
            "📝 *चरण 1 / 4 – समस्या बताएं*\n\n"
            "अपने क्षेत्र में पानी की समस्या टाइप करें।\n"
            "_(अगर आप फोटो या आवाज भेज रहे हैं तो यह छोड़ सकते हैं)_"
        ),
        "mr": (
            "📝 *पायरी 1 / 4 – समस्या सांगा*\n\n"
            "तुमच्या परिसरातील पाण्याची समस्या टाइप करा.\n"
            "_(फोटो किंवा आवाज पाठवत असाल तर हे वगळू शकता)_"
        ),
    },
    "step_photo": {
        "en": (
            "📷 *Step 2 of 4 – Send a photo*\n\n"
            "Take a photo of the water problem and send it here.\n"
            "_(Skip if you don't have one)_"
        ),
        "hi": (
            "📷 *चरण 2 / 4 – फोटो भेजें*\n\n"
            "पानी की समस्या की फोटो लें और यहाँ भेजें।\n"
            "_(अगर नहीं है तो छोड़ दें)_"
        ),
        "mr": (
            "📷 *पायरी 2 / 4 – फोटो पाठवा*\n\n"
            "पाण्याच्या समस्येचा फोटो काढा आणि इथे पाठवा.\n"
            "_(नसल्यास वगळा)_"
        ),
    },
    "step_voice": {
        "en": (
            "🎙️ *Step 3 of 4 – Send a voice note*\n\n"
            "Hold the microphone button in Telegram and describe the problem in your own words.\n"
            "_(Skip if you prefer not to)_"
        ),
        "hi": (
            "🎙️ *चरण 3 / 4 – आवाज़ भेजें*\n\n"
            "Telegram में माइक्रोफोन बटन दबाकर अपनी बात कहें।\n"
            "_(अगर नहीं चाहते तो छोड़ दें)_"
        ),
        "mr": (
            "🎙️ *पायरी 3 / 4 – आवाज पाठवा*\n\n"
            "Telegram मध्ये मायक्रोफोन बटण दाबून तुमची समस्या सांगा.\n"
            "_(नको असल्यास वगळा)_"
        ),
    },
    "step_location": {
        "en": (
            "📍 *Step 4 of 4 – Share your location*\n\n"
            "Tap the button below ↓ to share your exact location.\n"
            "This helps route your complaint to the right office."
        ),
        "hi": (
            "📍 *चरण 4 / 4 – अपनी जगह शेयर करें*\n\n"
            "नीचे बटन दबाकर अपनी सटीक लोकेशन शेयर करें।\n"
            "इससे शिकायत सही दफ्तर तक पहुंचेगी।"
        ),
        "mr": (
            "📍 *पायरी 4 / 4 – तुमचे ठिकाण शेअर करा*\n\n"
            "खाली ↓ बटण दाबून तुमचे अचूक ठिकाण शेअर करा.\n"
            "यामुळे तक्रार योग्य कार्यालयाकडे जाईल."
        ),
    },
    "btn_skip": {
        "en": "⏭ Skip",
        "hi": "⏭ छोड़ें",
        "mr": "⏭ वगळा",
    },
    "btn_share_location": {
        "en": "📍 Share My Location",
        "hi": "📍 मेरी जगह शेयर करें",
        "mr": "📍 माझे ठिकाण शेअर करा",
    },

    # ── Review & submit ──────────────────────────────────────────────────────
    "review_header": {
        "en": "✅ *Review your complaint before submitting:*\n\n",
        "hi": "✅ *जमा करने से पहले अपनी शिकायत देखें:*\n\n",
        "mr": "✅ *सबमिट करण्यापूर्वी तुमची तक्रार तपासा:*\n\n",
    },
    "review_text": {
        "en": "📝 Description: ",
        "hi": "📝 विवरण: ",
        "mr": "📝 वर्णन: ",
    },
    "review_photo": {
        "en": "📷 Photo: ✓ added",
        "hi": "📷 फोटो: ✓ जोड़ी गई",
        "mr": "📷 फोटो: ✓ जोडला",
    },
    "review_voice": {
        "en": "🎙️ Voice note: ✓ added",
        "hi": "🎙️ आवाज़: ✓ जोड़ी गई",
        "mr": "🎙️ आवाज: ✓ जोडली",
    },
    "review_location": {
        "en": "📍 Location: ✓ captured",
        "hi": "📍 लोकेशन: ✓ मिल गई",
        "mr": "📍 ठिकाण: ✓ मिळाले",
    },
    "review_nothing": {
        "en": "_(nothing added)_",
        "hi": "_(कुछ नहीं जोड़ा)_",
        "mr": "_(काहीही जोडले नाही)_",
    },
    "btn_submit": {
        "en": "✅ Submit Complaint",
        "hi": "✅ शिकायत जमा करें",
        "mr": "✅ तक्रार सबमिट करा",
    },
    "btn_cancel": {
        "en": "❌ Cancel",
        "hi": "❌ रद्द करें",
        "mr": "❌ रद्द करा",
    },

    # ── Submission states ────────────────────────────────────────────────────
    "submitting": {
        "en": "⏳ Submitting your complaint… please wait.",
        "hi": "⏳ शिकायत जमा हो रही है… कृपया प्रतीक्षा करें।",
        "mr": "⏳ तक्रार सबमिट होत आहे… कृपया थांबा.",
    },
    "submit_success": {
        "en": (
            "🎉 *Complaint submitted successfully!*\n\n"
            "🆔 Complaint ID: `{complaint_id}`\n"
            "📂 Category: {category}\n"
            "⚠️ Severity: {severity}\n"
            "🏛 Assigned to: {authority}\n"
            "📊 Status: {status}\n\n"
            "We will keep track of your complaint. "
            "Use /mystatus to check updates anytime."
        ),
        "hi": (
            "🎉 *शिकायत सफलतापूर्वक दर्ज हो गई!*\n\n"
            "🆔 शिकायत ID: `{complaint_id}`\n"
            "📂 श्रेणी: {category}\n"
            "⚠️ गंभीरता: {severity}\n"
            "🏛 जिम्मेदार विभाग: {authority}\n"
            "📊 स्थिति: {status}\n\n"
            "हम आपकी शिकायत का ध्यान रखेंगे। "
            "कभी भी /mystatus टाइप करें।"
        ),
        "mr": (
            "🎉 *तक्रार यशस्वीरित्या नोंदवली गेली!*\n\n"
            "🆔 तक्रार ID: `{complaint_id}`\n"
            "📂 श्रेणी: {category}\n"
            "⚠️ तीव्रता: {severity}\n"
            "🏛 जबाबदार विभाग: {authority}\n"
            "📊 स्थिती: {status}\n\n"
            "आम्ही तुमच्या तक्रारीचा मागोवा घेऊ. "
            "कधीही /mystatus टाइप करा."
        ),
    },
    "submit_error": {
        "en": (
            "❌ *Could not submit your complaint.*\n\n"
            "Please try again in a few minutes. "
            "If the problem continues, contact your local water board."
        ),
        "hi": (
            "❌ *शिकायत जमा नहीं हो सकी।*\n\n"
            "कुछ मिनट बाद फिर कोशिश करें। "
            "समस्या बनी रहे तो स्थानीय जल विभाग से संपर्क करें।"
        ),
        "mr": (
            "❌ *तक्रार सबमिट होऊ शकली नाही.*\n\n"
            "काही मिनिटांनी पुन्हा प्रयत्न करा. "
            "समस्या कायम राहिल्यास स्थानिक जल विभागाशी संपर्क करा."
        ),
    },
    "cancelled": {
        "en": "🚫 Complaint cancelled. Type /start to begin again.",
        "hi": "🚫 शिकायत रद्द कर दी गई। दोबारा शुरू करने के लिए /start टाइप करें।",
        "mr": "🚫 तक्रार रद्द केली. पुन्हा सुरू करण्यासाठी /start टाइप करा.",
    },

    # ── Validation errors ────────────────────────────────────────────────────
    "nothing_added": {
        "en": (
            "⚠️ You must add at least one of: a description, a photo, or a voice note.\n"
            "Please go back and add something."
        ),
        "hi": (
            "⚠️ कम से कम एक जरूरी है: विवरण, फोटो, या आवाज़।\n"
            "कृपया वापस जाकर कुछ जोड़ें।"
        ),
        "mr": (
            "⚠️ किमान एक आवश्यक आहे: वर्णन, फोटो, किंवा आवाज.\n"
            "कृपया परत जाऊन काहीतरी जोडा."
        ),
    },
    "need_location": {
        "en": "📍 Please share your location using the button below.",
        "hi": "📍 कृपया नीचे दिए बटन से अपनी जगह शेयर करें।",
        "mr": "📍 कृपया खालील बटण वापरून तुमचे ठिकाण शेअर करा.",
    },

    # ── My Reports ───────────────────────────────────────────────────────────
    "my_reports_header": {
        "en": "📊 *Your last {count} complaint(s):*\n\n",
        "hi": "📊 *आपकी पिछली {count} शिकायत(ें):*\n\n",
        "mr": "📊 *तुमच्या शेवटच्या {count} तक्रारी:*\n\n",
    },
    "my_reports_empty": {
        "en": "You haven't filed any complaints yet. Type /start to report a problem.",
        "hi": "आपने अभी तक कोई शिकायत दर्ज नहीं की। शिकायत करने के लिए /start टाइप करें।",
        "mr": "तुम्ही अद्याप कोणतीही तक्रार नोंदवलेली नाही. समस्या नोंदवण्यासाठी /start टाइप करा.",
    },
    "report_item": {
        "en": (
            "🆔 `{id_short}`\n"
            "📂 {category} – {subcategory}\n"
            "⚠️ {severity}  |  📊 {status}\n"
            "📅 {date}\n"
        ),
        "hi": (
            "🆔 `{id_short}`\n"
            "📂 {category} – {subcategory}\n"
            "⚠️ {severity}  |  📊 {status}\n"
            "📅 {date}\n"
        ),
        "mr": (
            "🆔 `{id_short}`\n"
            "📂 {category} – {subcategory}\n"
            "⚠️ {severity}  |  📊 {status}\n"
            "📅 {date}\n"
        ),
    },

    # ── Misc ─────────────────────────────────────────────────────────────────
    "unexpected": {
        "en": "🤔 I didn't understand that. Please use the buttons or type /start.",
        "hi": "🤔 मैं समझ नहीं पाया। बटन का उपयोग करें या /start टाइप करें।",
        "mr": "🤔 मला ते समजले नाही. बटणे वापरा किंवा /start टाइप करा.",
    },
    "language_prompt": {
        "en": "🌐 Choose your language / भाषा चुनें / भाषा निवडा:",
        "hi": "🌐 Choose your language / भाषा चुनें / भाषा निवडा:",
        "mr": "🌐 Choose your language / भाषा चुनें / भाषा निवडा:",
    },
}


def t(key: str, lang: Lang, **kwargs) -> str:
    """Return translated string, optionally with .format(**kwargs)."""
    entry = STRINGS.get(key, {})
    # Fall back: mr -> hi -> en
    text = entry.get(lang) or entry.get("hi") or entry.get("en") or key
    if kwargs:
        text = text.format(**kwargs)
    return text
