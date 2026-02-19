---

# 🎙️ Sweeyam Voice Assistant — AI-Powered Voice & NLP Application

A smart **AI-powered voice assistant built in Python**, designed to understand spoken commands, process natural language, and perform actions.
Perfect for voice interaction experiments, NLP learning, and personal digital assistant projects.

**Voice → NLP → Action Pipeline** — Easy to extend & integrate with modules.

---

## 🚀 Features

✨ **Real-time voice input & transcription**
🎤 Voice-to-text processing with NLP
🧠 Intelligent decision making via NLP engine
📡 Modular runners for plugins & behaviors
🗂️ Clean structure with support for multiple modules

---

## 📦 What’s Included

| File / Module                | Purpose                           |
| ---------------------------- | --------------------------------- |
| `app.py`                     | Main application entrypoint       |
| `voice_transcriber.py`       | Converts user voice to text       |
| `nlp_engine.py`              | Natural language processing logic |
| `live_voice_runner.py`       | Live voice interaction loop       |
| `module1_runner.py`          | Runner for first module           |
| `module2_behavioral.py`      | Module 2 behavior logic           |
| `module3_decision_engine.py` | Decision engine for actions       |
| `auth_checks.py`             | RBAC / authentication logic       |
| `database.py`                | Database interface                |
| `eml_parser.py`              | Email parsing utilities           |
| `requirements.txt`           | Python dependencies               |

---

## 📌 Quick Start

### 🛠️ Requirements

Install Python (3.8+ recommended) and dependencies:

```bash
pip install -r requirements.txt
```

---

### ▶️ Run the Assistant

Start the voice assistant:

```bash
python app.py
```

Speak into your microphone — the assistant will transcribe and respond based on its NLP engine.

---

## 🧠 How It Works

1. **Voice Input** — The assistant uses microphone input.
2. **Transcription** — `voice_transcriber.py` converts speech to text.
3. **Processing** — Text is passed to `nlp_engine.py`.
4. **Action** — Appropriate behavior modules are triggered via runners.

This modular design allows easy plugin of new capabilities (e.g., skills, commands, APIs).

---

## 🛠️ Extend & Customize

You can:

* Add more **NLP intents**
* Integrate **speech-to-text services**
* Add API calls (weather, search, etc.)
* Plug in gui/microphone enhancements
* Build new modules under `module*_*.py`

---

## 🤝 Contributing

Contributions welcome!

1. Fork the repo
2. Add features / fix issues
3. Create a pull request

Let’s improve this voice AI together! 🚀

---

## 📜 License

This project is open source — feel free to use, modify, and distribute.

---
