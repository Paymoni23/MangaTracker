import json
import os
from typing import List
from .models import Manga

DATA_FILE = "manga_data.json"

def save_manga_list(manga_list: List[Manga]):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump([manga.to_dict() for manga in manga_list], f, indent=4)

def load_manga_list() -> List[Manga]:
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return [Manga.from_dict(item) for item in data]
    except (json.JSONDecodeError, KeyError):
        return []
