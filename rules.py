# rules.py

import re


# -------------------------------
# Helper
# -------------------------------

def clean_text(text):
    """Normalize message text."""
    if text is None:
        return ""

    text = str(text).lower()

    # remove punctuation
    text = re.sub(r"[^a-z0-9\s]", " ", text)

    return text


# -------------------------------
# Scam Detection
# -------------------------------

def is_scam(text):

    text = clean_text(text)

    scam_keywords = [

        "otp",
        "verification code",
        "verify your account",
        "verify account",
        "bank account blocked",
        "click here",
        "claim prize",
        "winner",
        "gift card",
        "wallet suspended",
        "kyc expired",
        "pay immediately",
        "urgent payment",
        "bitcoin",
        "crypto giveaway"

    ]

    return any(word in text for word in scam_keywords)


# -------------------------------
# Prompt Injection Detection
# -------------------------------

def is_prompt_injection(text):

    text = clean_text(text)

    injection = [

        "ignore previous instructions",
        "ignore previous routing rules",
        "ignore system prompt",
        "you are chatgpt",
        "assistant",
        "developer message"

    ]

    return any(word in text for word in injection)


# -------------------------------
# Forward Detection
# -------------------------------

def is_forward(text, forwarded_count):

    text = clean_text(text)

    if forwarded_count >= 5:
        return True

    if "forward this" in text:
        return True

    if "share with everyone" in text:
        return True

    return False


# -------------------------------
# Greeting
# -------------------------------

def is_greeting(text):

    text = clean_text(text)

    greetings = [

        "happy birthday",
        "good morning",
        "good evening",
        "good night",
        "congratulations",
        "best wishes",
        "happy anniversary"

    ]

    return any(word in text for word in greetings)


# -------------------------------
# Promotion
# -------------------------------

def is_promotion(text):

    text = clean_text(text)

    promotions = [

        "sale",
        "offer",
        "discount",
        "coupon",
        "cashback",
        "limited time",
        "buy now",
        "shop now",
        "exclusive deal",
        "festival offer"

    ]

    return any(word in text for word in promotions)


# -------------------------------
# Payment
# -------------------------------

def is_payment(text):

    text = clean_text(text)

    payment = [

        "invoice",
        "bill",
        "payment",
        "maintenance fee",
        "rent",
        "due amount",
        "upi",
        "transaction"

    ]

    return any(word in text for word in payment)


# -------------------------------
# Event
# -------------------------------

def is_event(text):

    text = clean_text(text)

    event = [

        "meeting",
        "tomorrow",
        "today",
        "schedule",
        "event",
        "orientation",
        "seminar",
        "webinar",
        "maintenance",
        "exam",
        "deadline"

    ]

    return any(word in text for word in event)


# -------------------------------
# Urgent
# -------------------------------

def is_urgent(text):

    text = clean_text(text)

    urgent = [

        "urgent",
        "asap",
        "immediately",
        "emergency",
        "today only",
        "last chance",
        "deadline today",
        "expires today"

    ]

    return any(word in text for word in urgent)


# -------------------------------
# Business Update
# -------------------------------

def is_business_update(text):

    text = clean_text(text)

    updates = [

        "your order",
        "delivery",
        "booking",
        "shipment",
        "tracking",
        "ticket confirmed",
        "appointment confirmed",
        "dispatch",
        "arriving"

    ]

    return any(word in text for word in updates)


# -------------------------------
# Personal Request
# -------------------------------

def is_personal_request(text):

    text = clean_text(text)

    request = [

        "can you",
        "please reply",
        "call me",
        "let me know",
        "need your help",
        "are you free",
        "please send",
        "reply when possible"

    ]

    return any(word in text for word in request)


# -------------------------------
# Final Message Type
# -------------------------------

def detect_message_type(
    text,
    conversation_type,
    forwarded_count
):

    if is_prompt_injection(text):
        return "scam"

    if is_scam(text):
        return "scam"

    if is_forward(text, forwarded_count):
        return "forward"

    if is_payment(text):
        return "payment"

    if is_business_update(text):
        return "business_update"

    if is_promotion(text):
        return "promotion"

    if is_urgent(text):
        return "urgent"

    if is_event(text):
        return "event"

    if is_greeting(text):
        return "greeting"

    if conversation_type == "personal":
        return "personal"

    return "unknown"