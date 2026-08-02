import os
import whisper
import pandas as pd

model = whisper.load_model("base")

voice = pd.read_csv("dataset/voice_notes.csv")

lookup = {}

for _, row in voice.iterrows():
    lookup[row["voice_note_id"]] = row["file_path"]


def transcribe(media_id):

    if pd.isna(media_id):
        return ""

    if media_id not in lookup:
        return ""

    path = os.path.join("dataset", lookup[media_id])

    if not os.path.exists(path):
        return ""

    try:
        result = model.transcribe(path)
        return result["text"]

    except:
        return ""