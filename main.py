import json
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permet à n'importe quelle application de l'appeler
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/feed")
def get_cards_from_file():
    # L'indentation doit être à l'intérieur de la fonction
    try:
        with open("cards.txt", "r", encoding="utf-8") as f:
            data = json.load(f)
        return {"cards": data}
    except FileNotFoundError:
        return {"error": "Le fichier cards.txt est introuvable sur le serveur"}
    except json.JSONDecodeError:
        return {"error": "Le fichier cards.txt contient du JSON invalide"}