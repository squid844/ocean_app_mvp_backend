import wikipediaapi
import textstat
import time
import evaluate_page as evaluate_page
import json

wiki = evaluate_page.wiki
max_jumps = 10

def spyder_wikipedia(seed_topic, max_articles=10):
    cards_library = []
    deja_vu = set()
    to_visit = [seed_topic]

    print(f"Start exploring at : {seed_topic}")

    while len(cards_library) < max_articles and to_visit:
        title = to_visit.pop(0)
        if title in deja_vu: continue

        page = wiki.page(title)
        if not page.exists(): continue

        card = evaluate_page.evaluate_page(page)

        cards_library.append(card)
        deja_vu.add(title)
        print(f"Added a new card : {title}")

        links = list(page.links.keys())
        to_visit.extend(links[:5])
        
        time.sleep(0.01) # not overwork wikipedia servers

    return cards_library

cards = spyder_wikipedia('Godot', max_jumps)
with open("cards.txt", "w", encoding="utf-8") as f:
    json.dump(cards, f, indent=4, ensure_ascii=False)