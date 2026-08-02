import os
import easyocr
import pandas as pd

reader = easyocr.Reader(['en'], gpu=False)

images = pd.read_csv("dataset/images.csv")

image_lookup = {}

for _, row in images.iterrows():
    image_lookup[row["image_id"]] = row["file_path"]


def read_image(media_id):

    if pd.isna(media_id):
        return ""

    if media_id not in image_lookup:
        return ""

    path = os.path.join("dataset", image_lookup[media_id])

    if not os.path.exists(path):
        return ""

    try:
        result = reader.readtext(path, detail=0)
        return " ".join(result)

    except:
        return ""