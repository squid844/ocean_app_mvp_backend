import wikipediaapi
import textstat
import time
import evaluate_page as evaluate_page
import json

wiki = evaluate_page.wiki
max_depth = 10

def _strip_namespace(title: str) -> str:
    if not title:
        return title
    return title.split(":", 1)[1] if ":" in title else title

def spyder_tags_wikipedia(seed_topic, max_tags=10, max_depth=None):
    tags_library = []
    deja_vu = set()

    # Depth default
    if max_depth is None:
        max_depth = globals().get("max_depth", 10)

    # Try common localized category prefixes (fr/english), fall back to raw seed
    candidates = [f"Catégorie:{seed_topic}", f"Category:{seed_topic}", seed_topic]
    to_visit = []
    for cand in candidates:
        p = wiki.page(cand)
        if p.exists():
            # store tuples (title, depth)
            to_visit.append((p.title, 0))
            break
    if not to_visit:
        to_visit.append((seed_topic, 0))

    tag = {
        "category": seed_topic,
        "parent": None
    }
    tags_library.append(tag)
    print(f"Start exploring at : {seed_topic}")

    while len(tags_library) < max_tags and to_visit:
        title, depth = to_visit.pop(0)
        if title in deja_vu:
            continue

        try:
            page = wiki.page(title)
        except Exception as e:
            print(f"Warning: failed to fetch page {title}: {e}")
            deja_vu.add(title)
            continue

        if not page.exists():
            deja_vu.add(title)
            continue

        try:
            members = page.categorymembers
        except Exception as e:
            print(f"Warning: no category members for {title}: {e}")
            deja_vu.add(title)
            continue

        # collect up to 5 subcategories for this page
        subcats = []
        for m in members.values():
            # namespace for categories may vary by language; check namespace id
            try:
                is_category = (m.ns == wikipediaapi.Namespace.CATEGORY)
            except Exception:
                # fallback to checking prefix
                is_category = m.title.startswith("Catégorie:") or m.title.startswith("Category:")

            if is_category:
                tag = {
                    "category": _strip_namespace(m.title),
                    "parent": _strip_namespace(title)
                }
                tags_library.append(tag)
                subcats.append(m.title)
                print(f"Added a new tag : {_strip_namespace(m.title)} (parent: {_strip_namespace(title)})")
                if len(tags_library) >= max_tags:
                    break

        # mark processed and enqueue a few subcategories (respecting depth)
        deja_vu.add(title)
        if subcats and depth < max_depth:
            for sub in subcats[:5]:
                to_visit.append((sub, depth + 1))

        time.sleep(0.01) # not overwork wikipedia servers

    return tags_library

cards = spyder_tags_wikipedia('Cinéma', max_tags=100, max_depth=3)
with open("tags.txt", "w", encoding="utf-8") as f:
    json.dump(cards, f, indent=4, ensure_ascii=False)