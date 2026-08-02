# 🧠 Smart Notification Router for WhatsApp

An AI-powered notification routing system built for the HackerRank AI Hackathon.

## 🚀 Overview

Modern messaging apps generate hundreds of notifications every day. Many are important, while others are promotional, repetitive, or even malicious.

This project intelligently analyzes every incoming message using contextual information, user preferences, historical interactions, and message content to determine the most appropriate notification strategy.

Instead of notifying users for every message, the system decides whether to:

- 🔔 Notify immediately
- 📥 Add to a notification digest
- 🔕 Mute the notification

The entire routing process is explainable, personalized, and context-aware.

---

# ✨ Features

## 🛡️ Intelligent Scam Detection

Detects phishing and scam attempts using keyword analysis, suspicious forwarding patterns, and prompt-injection detection.

Examples:

- OTP scams
- Fake banking alerts
- Cryptocurrency giveaways
- Gift card scams
- Prompt injection attacks

---

## 👤 Personalized Notification Routing

Uses user behaviour such as:

- Do Not Disturb preferences
- Previous interactions
- Business relationships
- Notification history

to intelligently prioritize notifications.

---

## 👥 Group-aware Decisions

Different routing strategies are applied for:

- Family Groups
- Work Groups
- College Groups
- Society Groups

Muted groups are also respected while still allowing urgent messages through.

---

## 🏢 Business Intelligence

Recognizes:

- Verified businesses
- Existing customer relationships
- Promotional messages
- Delivery updates
- Payment reminders

to reduce notification fatigue.

---

## 🖼️ Media Understanding

Supports:

- OCR for image messages
- Voice note transcription pipeline
- Text enrichment before classification

---

## 📚 Historical Evidence Retrieval

For every prediction, the system retrieves a similar historical message to provide explainable AI reasoning.

---

## ⚙️ Technologies Used

- Python
- Pandas
- EasyOCR
- PyTorch
- Rule-based AI
- Context-aware Decision Engine

---

# 📂 Project Structure

```
hackerrank_whatsappnotif/
│
├── dataset/
│
├── main.py
├── classifier.py
├── context.py
├── rules.py
├── history.py
├── image_reader.py
├── voice_reader.py
│
├── output.csv
├── README.md
└── requirements.txt
```

---

# ▶️ Installation

Install dependencies

```bash
pip install -r requirements.txt
```

---

# ▶️ Run

```bash
python3 main.py
```

The program generates:

```
output.csv
```

containing:

- message_id
- action
- message_type
- reason
- confidence
- evidence_message_ids

---

# 🧩 Decision Pipeline

Incoming Message

↓

Media Processing (OCR / Voice)

↓

Context Building

↓

Message Classification

↓

Confidence Scoring

↓

Notification Decision

↓

Historical Evidence Retrieval

↓

Output Generation

---

# 🌟 Key Highlights

✅ Context-aware routing

✅ Personalized notification prioritization

✅ Explainable AI decisions

✅ Scam and phishing detection

✅ Business relationship modelling

✅ OCR-enabled media understanding

✅ Historical evidence support

---

Built for the **HackerRank AI Hackathon**.