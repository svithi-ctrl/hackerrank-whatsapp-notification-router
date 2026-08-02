import pandas as pd


class HistoryEngine:

    def __init__(self):

        self.history = pd.read_csv("dataset/message_history.csv")
        self.events = pd.read_csv("dataset/message_events.csv")

    def find_evidence(self, message):

        user_history = self.history[
            self.history["user_id"] == message["user_id"]
        ]

        if len(user_history) == 0:
            return "none"

        text = str(message["message_text"]).lower()

        # -------- look for similar words --------

        for _, old in user_history.iterrows():

            old_text = str(old["message_text"]).lower()

            words = set(text.split())

            overlap = len(words.intersection(set(old_text.split())))

            if overlap >= 3:
                return old["message_id"]

        return "none"