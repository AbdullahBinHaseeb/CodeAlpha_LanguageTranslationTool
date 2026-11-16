"""
Language Translation Tool — CodeAlpha AI Internship, Task 1.

A Flask web app that translates text between languages using the free
`deep-translator` package (GoogleTranslator). If the translation service
is unreachable, a small built-in phrase dictionary is used as a fallback
so the app still demonstrates end-to-end translation.

Author: Abdullah Bin Haseeb
Student ID: CA/DF1/321398
"""

from flask import Flask, jsonify, render_template, request

try:
    from deep_translator import GoogleTranslator
except ImportError:  # pragma: no cover - deep-translator not installed
    GoogleTranslator = None

app = Flask(__name__)

# Language code -> display name (shown in the dropdowns)
LANGUAGES = {
    "en": "English",
    "ur": "Urdu",
    "es": "Spanish",
    "fr": "French",
    "de": "German",
    "ar": "Arabic",
    "zh-CN": "Chinese (Simplified)",
    "hi": "Hindi",
    "ja": "Japanese",
    "ru": "Russian",
    "tr": "Turkish",
    "it": "Italian",
}

# Fallback phrase dictionary, used only when the translation API is
# unreachable. Keys are (source_lang, target_lang) -> {phrase: translation}.
# Phrases are matched case-insensitively on the stripped input text.
FALLBACK_PHRASES = {
    ("en", "ur"): {
        "hello": "ہیلو",
        "hello, how are you?": "ہیلو، آپ کیسے ہیں؟",
        "how are you?": "آپ کیسے ہیں؟",
        "thank you": "شکریہ",
        "thank you very much": "بہت شکریہ",
        "good morning": "صبح بخیر",
        "good night": "شب بخیر",
        "goodbye": "خدا حافظ",
        "yes": "ہاں",
        "no": "نہیں",
        "welcome": "خوش آمدید",
    },
    ("en", "es"): {
        "hello": "Hola",
        "hello, how are you?": "Hola, ¿cómo estás?",
        "how are you?": "¿Cómo estás?",
        "thank you": "Gracias",
        "thank you very much": "Muchas gracias",
        "good morning": "Buenos días",
        "good night": "Buenas noches",
        "goodbye": "Adiós",
        "yes": "Sí",
        "no": "No",
        "welcome": "Bienvenido",
    },
    ("en", "fr"): {
        "hello": "Bonjour",
        "hello, how are you?": "Bonjour, comment allez-vous ?",
        "how are you?": "Comment allez-vous ?",
        "thank you": "Merci",
        "thank you very much": "Merci beaucoup",
        "good morning": "Bonjour",
        "good night": "Bonne nuit",
        "goodbye": "Au revoir",
        "yes": "Oui",
        "no": "Non",
        "welcome": "Bienvenue",
    },
    ("en", "de"): {
        "hello": "Hallo",
        "hello, how are you?": "Hallo, wie geht es dir?",
        "how are you?": "Wie geht es dir?",
        "thank you": "Danke",
        "thank you very much": "Vielen Dank",
        "good morning": "Guten Morgen",
        "good night": "Gute Nacht",
        "goodbye": "Auf Wiedersehen",
        "yes": "Ja",
        "no": "Nein",
        "welcome": "Willkommen",
    },
    ("en", "ar"): {
        "hello": "مرحباً",
        "hello, how are you?": "مرحباً، كيف حالك؟",
        "how are you?": "كيف حالك؟",
        "thank you": "شكراً",
        "thank you very much": "شكراً جزيلاً",
        "good morning": "صباح الخير",
        "good night": "تصبح على خير",
        "goodbye": "وداعاً",
        "yes": "نعم",
        "no": "لا",
        "welcome": "أهلاً وسهلاً",
    },
    ("en", "hi"): {
        "hello": "नमस्ते",
        "hello, how are you?": "नमस्ते, आप कैसे हैं?",
        "how are you?": "आप कैसे हैं?",
        "thank you": "धन्यवाद",
        "thank you very much": "बहुत धन्यवाद",
        "good morning": "सुप्रभात",
        "good night": "शुभ रात्रि",
        "goodbye": "अलविदा",
        "yes": "हाँ",
        "no": "नहीं",
        "welcome": "स्वागत है",
    },
    ("en", "zh-CN"): {
        "hello": "你好",
        "hello, how are you?": "你好，你好吗？",
        "how are you?": "你好吗？",
        "thank you": "谢谢",
        "thank you very much": "非常感谢",
        "good morning": "早上好",
        "good night": "晚安",
        "goodbye": "再见",
        "yes": "是",
        "no": "不",
        "welcome": "欢迎",
    },
}


def fallback_translate(text, source, target):
    """Look up a phrase in the built-in dictionary. Returns None if absent."""
    table = FALLBACK_PHRASES.get((source, target))
    if not table:
        return None
    return table.get(text.strip().lower())


def translate_text(text, source, target):
    """Translate text. Returns (translated_text, used_fallback: bool).

    Raises ValueError on bad input and RuntimeError when neither the API
    nor the fallback dictionary can translate the text.
    """
    text = (text or "").strip()
    if not text:
        raise ValueError("Please enter some text to translate.")
    if source not in LANGUAGES:
        raise ValueError(f"Unsupported source language: {source}")
    if target not in LANGUAGES:
        raise ValueError(f"Unsupported target language: {target}")
    if source == target:
        return text, False

    # Primary route: free Google Translate via deep-translator.
    if GoogleTranslator is not None:
        try:
            result = GoogleTranslator(source=source, target=target).translate(text)
            if result and result.strip():
                return result, False
        except Exception:
            pass  # fall through to the offline dictionary

    # Offline fallback for common phrases.
    fallback = fallback_translate(text, source, target)
    if fallback:
        return fallback, True

    raise RuntimeError(
        "Translation service is unreachable and this phrase is not in the "
        "offline dictionary. Please check your internet connection and try again."
    )


@app.route("/", methods=["GET"])
def index():
    return render_template(
        "index.html", languages=LANGUAGES, default_source="en", default_target="ur"
    )


@app.route("/translate", methods=["POST"])
def translate():
    """Accepts form data or JSON: text, source, target. Returns JSON."""
    payload = request.get_json(silent=True) or request.form
    text = payload.get("text", "")
    source = payload.get("source", "en")
    target = payload.get("target", "ur")
    try:
        translated, used_fallback = translate_text(text, source, target)
    except (ValueError, RuntimeError) as exc:
        return jsonify({"ok": False, "error": str(exc)}), 400
    return jsonify(
        {
            "ok": True,
            "translated_text": translated,
            "source": source,
            "target": target,
            "source_language": LANGUAGES[source],
            "target_language": LANGUAGES[target],
            "fallback_used": used_fallback,
        }
    )


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"ok": True, "languages": len(LANGUAGES)})


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
