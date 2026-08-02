import pandas as pd

from context import ContextManager
from classifier import decide_action
from history import HistoryEngine
from image_reader import read_image
from voice_reader import transcribe


# ----------------------------------------
# Load messages
# ----------------------------------------

messages = pd.read_csv("dataset/messages.csv")

context_manager = ContextManager()
history_engine = HistoryEngine()

predictions = []


# ----------------------------------------
# Process each message
# ----------------------------------------

for _, row in messages.iterrows():

    # Build user/group/business context
    context = context_manager.build(row)

    # Original message text
    text = str(row["message_text"])

    # Extract text from image or voice
    try:
        if row["media_type"] == "image":
            text += " " + read_image(row["media_id"])

        elif row["media_type"] == "voice":
            text += " " + transcribe(row["media_id"])

    except Exception:
        pass

    # Replace message text with enriched text
    row["message_text"] = text

    # AI decision
    action, message_type, reason, confidence = decide_action(
        row,
        context
    )

    # Retrieve similar historical message
    evidence = history_engine.find_evidence(row)

    predictions.append({

        "message_id": row["message_id"],
        "action": action,
        "message_type": message_type,
        "reason": reason,
        "confidence": round(confidence, 2),
        "evidence_message_ids": evidence

    })


# ----------------------------------------
# Save output
# ----------------------------------------

output = pd.DataFrame(predictions)

output.to_csv("output.csv", index=False)

print("\n✅ output.csv created successfully!")
print(f"Processed {len(output)} messages.")
print(output.head())