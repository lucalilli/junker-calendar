import re
import requests
import json
from ics import Calendar, Event
from datetime import datetime

URL = "https://differenziata.junkerapp.it/fiano-romano/284099/calendario"

# Traduzione specifica come da richiesta
waste_map = {
    "Organic waste": "Organico",
    "General waste collection": "Residuo",
    "Glass/Cans": "Vetro/Latta",
    "Plastic": "Plastica",
    "Paper": "Carta"
}

def fetch_calendar():
    # Scarica la pagina
    r = requests.get(URL)
    html = r.text

    # Trova la variabile events = [...]
    match = re.search(r"var\s+events\s*=\s*(\[.*?\]);", html, re.DOTALL)
    if not match:
        raise RuntimeError("Impossibile trovare la variabile events nella pagina")

    events_json = match.group(1)
    events = json.loads(events_json)

    cal = Calendar()
    for e in events:
        date_str = e["date"]
        desc = e.get("vbin_desc", "Raccolta")

        # Traduci in italiano
        desc_it = waste_map.get(desc, desc)

        # Parsing data
        dt = datetime.strptime(date_str, "%Y-%m-%d")

        # Crea evento
        event = Event()
        event.name = f"Raccolta {desc_it}"
        event.begin = dt
        cal.events.add(event)

    return cal

if __name__ == "__main__":
    cal = fetch_calendar()
    with open("calendario.ics", "w", encoding="utf-8") as f:
        f.writelines(cal)
    print("✅ File calendario.ics generato con successo!")
