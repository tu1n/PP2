import json
import os

SCORES_FILE= "leaderboard.json"
SETTINGS_FILE = "settings.json"

# что будет в settings если файл не нашли
DEFAULT_SETTINGS = {
    "sound":      True,
    "car_color":  "red",
    "difficulty": "normal"
}


def load_scores():
    if not os.path.exists(SCORES_FILE):
        return []
    with open(SCORES_FILE, "r") as f:
        return json.load(f)


def save_score(name, score, dist):
    data = load_scores()
    data.append({"name": name, "score": score, "dist": int(dist)})
    #тут сортируем по очкам, берём топ 10
    data.sort(key=lambda x: x["score"], reverse=True)
    with open(SCORES_FILE, "w") as f:
        json.dump(data[:10], f, indent=2)


def load_settings():
    if not os.path.exists(SETTINGS_FILE):
        return DEFAULT_SETTINGS.copy()
    with open(SETTINGS_FILE, "r") as f:
        return json.load(f)


def save_settings(s):
    with open(SETTINGS_FILE, "w") as f:
        json.dump(s, f, indent=2)
