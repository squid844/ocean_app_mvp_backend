
import wikipediaapi
import textstat
import re
import math
from textstat.textstat import textstat
# accès à wikipédia
wiki = wikipediaapi.Wikipedia(
    user_agent="OceanDuSavoir/1.0 (noelacanal29@gmail.com)",
    language='fr',
    extract_format = wikipediaapi.ExtractFormat.WIKI
)

def search_page(page_title):
    page = wiki.page(page_title)
    
    if not page.exists():
        return "Article non trouvé pour : " + page_title
    return page

def evaluate_page(page):
    complete_text = page.text
    clean_text = re.sub(r'\[d+\]','', complete_text) # delete references

    nb_of_words = len(clean_text.split())
    reading_time = math.ceil(nb_of_words / 220) # 220 wpm seems to be the mean
    readability_score = textstat.flesch_reading_ease(clean_text)

    if readability_score > 80 : difficulty = 1
    elif readability_score > 60 : difficulty = 2
    elif readability_score > 40 : difficulty = 3
    elif readability_score > 20 : difficulty = 4
    else : difficulty = 5
    tags = [cat.replace("Catégorie:","") for cat in page.categories.keys()
            if "Article" not in cat and "Portail" not in cat and "Bon" not in cat and "Page" not in cat][:5]
    url_mobile = page.fullurl.replace("fr.wikipedia.org", "fr.m.wikipedia.org")
    return {
        "title" : page.title,
        "url" : url_mobile,
        "intro" : re.sub(r'(\n)', '', page.summary[:300]) + "...",
        "estimated_duration" : f"{reading_time} min",
        "estimated_difficulty" : difficulty,
        "tags" : tags
    }
