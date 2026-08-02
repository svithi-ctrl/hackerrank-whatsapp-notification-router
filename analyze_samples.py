import pandas as pd

pd.set_option("display.max_columns", None)
pd.set_option("display.max_colwidth", None)

df = pd.read_csv("dataset/sample_messages.csv")

print(df)