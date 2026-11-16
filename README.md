# Language Translation Tool

A simple web app that translates text between 12 languages. Built as
**Task 1 of the CodeAlpha AI Internship**.

- **Author:** Abdullah Bin Haseeb
- **Student ID:** CA/DF1/321398
- **Internship:** CodeAlpha AI Internship

## Features

- Clean web UI: enter text, pick a source and a target language, get the
  translation instantly.
- 12 supported languages: English, Urdu, Spanish, French, German, Arabic,
  Chinese (Simplified), Hindi, Japanese, Russian, Turkish and Italian.
- Swap-languages button and a **Copy** button for the translated text.
- Translation uses the free `deep-translator` package (GoogleTranslator).
  If the translation service is unreachable, a small built-in phrase
  dictionary is used as an offline fallback so the app still works
  end-to-end for common phrases.
- No text-to-speech (not required for this task).

## Project structure

```text
CodeAlpha_LanguageTranslationTool/
├── app.py                 # Flask app (routes, translation logic, fallback)
├── requirements.txt       # flask, deep-translator
├── README.md
├── .gitignore
├── static/
│   └── style.css          # UI styling
└── templates/
    └── index.html         # Web UI (form, result area, copy button)
```

## Setup

```bash
# 1. Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the app
python app.py
```

Then open **http://127.0.0.1:5000** in your browser.

## API

| Method | Endpoint     | Body (JSON or form)                  | Response                          |
| ------ | ------------ | ------------------------------------ | --------------------------------- |
| GET    | `/`          | —                                    | HTML page with the translator UI  |
| GET    | `/health`    | —                                    | `{"ok": true, "languages": 12}`   |
| POST   | `/translate` | `text`, `source`, `target` (codes)   | `{"ok": true, "translated_text": "...", "fallback_used": false}` |

Example:

```bash
curl -X POST http://127.0.0.1:5000/translate \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello, how are you?", "source": "en", "target": "ur"}'
```

## Notes

- Translation needs internet access for the GoogleTranslator route.
  Without internet, only the common phrases in the offline dictionary
  translate; anything else returns a clear error message.
- Language codes follow ISO 639-1, except Chinese Simplified (`zh-CN`).
