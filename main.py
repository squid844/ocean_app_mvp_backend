import json
from fastapi import FastAPI

app = FastAPI()

@app.get("/feed")
def get_cards_from_file():
    with open("cards.txt", "r", encoding="utf-8") as f:
        data = json.load(f)
    return {"cards" : data}