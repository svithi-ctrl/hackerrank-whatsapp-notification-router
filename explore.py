import pandas as pd

files = [
    "messages.csv",
    "users.csv",
    "groups.csv",
    "group_members.csv",
    "business_accounts.csv",
    "user_business_history.csv",
    "message_history.csv",
    "message_events.csv",
    "images.csv",
    "voice_notes.csv",
    "daily_notification_summary.csv"
]

for file in files:
    print("\n" + "=" * 60)
    print(file)

    try:
        df = pd.read_csv(f"dataset/{file}")

        print("Shape:", df.shape)
        print("\nColumns:")
        print(df.columns.tolist())

        print("\nFirst 2 rows:")
        print(df.head(2))

    except Exception as e:
        print("Error:", e)