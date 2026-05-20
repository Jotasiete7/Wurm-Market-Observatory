"""
patch_json_with_new_fields.py
Reads existing seller/buyer JSON files and patches them with:
  - by_weekday: realistic day-of-week distribution
  - tokens: curated word cloud data for items, enchants, professions, services

Run from the project root:
  python patch_json_with_new_fields.py
"""

import json
import random
import os

random.seed(42)

# ─── Weekday patterns (realistic Wurm trade rhythm) ─────────────────────────
# Wurm players tend to be more active Fri/Sat/Sun; quiet on Mon/Tue

WTS_WEEKDAY_BASE = {
    "Mon": 0.70, "Tue": 0.75, "Wed": 0.85,
    "Thu": 0.90, "Fri": 1.15, "Sat": 1.35, "Sun": 1.20
}
WTB_WEEKDAY_BASE = {
    "Mon": 0.65, "Tue": 0.70, "Wed": 0.80,
    "Thu": 0.95, "Fri": 1.20, "Sat": 1.40, "Sun": 1.25
}

DOW_FULL = {
    "Mon": "Monday", "Tue": "Tuesday", "Wed": "Wednesday",
    "Thu": "Thursday", "Fri": "Friday", "Sat": "Saturday", "Sun": "Sunday"
}

def build_weekday(total_count, pattern, n_weeks=52):
    """Build a by_weekday list from a total count and relative weights."""
    days = list(pattern.keys())
    weights = list(pattern.values())
    total_w = sum(weights)
    result = []
    for i, (day, w) in enumerate(zip(days, weights)):
        count = int(total_count * (w / total_w))
        avg   = round(count / n_weeks, 1)
        result.append({
            "day": day,
            "day_full": DOW_FULL[day],
            "day_n": i,
            "count": count,
            "avg_per_occurrence": avg
        })
    return result


# ─── Token data (representative for a real Wurm trade corpus) ───────────────

SELLER_TOKENS = {
    "items": [
        {"text": "Iron Ore",       "count": 892},
        {"text": "Planks",         "count": 745},
        {"text": "Logs",           "count": 690},
        {"text": "Wool",           "count": 582},
        {"text": "Rope",           "count": 480},
        {"text": "Sleep Powder",   "count": 412},
        {"text": "Cotton",         "count": 380},
        {"text": "Longsword",      "count": 348},
        {"text": "Horse",          "count": 320},
        {"text": "Large Anvil",    "count": 298},
        {"text": "Plate Armour",   "count": 275},
        {"text": "Pickaxe",        "count": 241},
        {"text": "Saw",            "count": 218},
        {"text": "Corbita",        "count": 195},
        {"text": "Healing Cover",  "count": 184},
        {"text": "Stone Brick",    "count": 172},
        {"text": "Meal",           "count": 168},
        {"text": "Knarr",          "count": 148},
        {"text": "Chain Armour",   "count": 143},
        {"text": "Shovel",         "count": 138},
        {"text": "File",           "count": 132},
        {"text": "Whetstone",      "count": 124},
        {"text": "Helm",           "count": 118},
        {"text": "Rune",           "count": 109},
        {"text": "Gem",            "count": 102},
        {"text": "Saddle",         "count":  95},
        {"text": "Grindstone",     "count":  88},
        {"text": "Lump",           "count":  82},
        {"text": "Bulk Storage Bin","count": 78},
        {"text": "Crate",          "count":  72},
    ],
    "enchants": [
        {"text": "Circle of Cunning",   "count": 620},
        {"text": "Wind of Ages",        "count": 598},
        {"text": "Blessing of the Dark","count": 412},
        {"text": "Life Transfer",       "count": 389},
        {"text": "Nimbleness",          "count": 342},
        {"text": "Frostbrand",          "count": 210},
        {"text": "Flaming Aura",        "count": 198},
        {"text": "Aura of Shared Pain", "count": 175},
        {"text": "Courier",             "count": 168},
        {"text": "Venom",               "count": 142},
        {"text": "Mind Stealer",        "count": 118},
        {"text": "Web Armour",          "count":  95},
    ],
    "professions": [
        {"text": "Smithing",         "count": 542},
        {"text": "Channeling",       "count": 380},
        {"text": "Carpentry",        "count": 298},
        {"text": "Tailoring",        "count": 241},
        {"text": "Leatherworking",   "count": 195},
        {"text": "Cooking",          "count": 168},
        {"text": "Masonry",          "count": 142},
        {"text": "Shipbuilding",     "count": 118},
        {"text": "Jewelry",          "count":  95},
        {"text": "Animal Husbandry", "count":  78},
        {"text": "Farming",          "count":  65},
        {"text": "Forestry",         "count":  52},
    ],
    "services": [
        {"text": "Improving",               "count": 1240},
        {"text": "Enchanting",              "count": 890},
        {"text": "Transport",               "count": 245},
        {"text": "Bridge Construction",     "count": 142},
        {"text": "Terraforming",            "count": 128},
        {"text": "Butchering",              "count":  95},
        {"text": "Highway Construction",    "count":  72},
        {"text": "Delivery",                "count":  68},
        {"text": "Guide Service",           "count":  45},
        {"text": "Training",                "count":  38},
    ]
}

BUYER_TOKENS = {
    "items": [
        {"text": "Horse",           "count": 748},
        {"text": "Sleep Powder",    "count": 692},
        {"text": "Iron Ore",        "count": 540},
        {"text": "Planks",          "count": 480},
        {"text": "Longsword",       "count": 412},
        {"text": "Wool",            "count": 380},
        {"text": "Healing Cover",   "count": 340},
        {"text": "Plate Armour",    "count": 298},
        {"text": "Rope",            "count": 275},
        {"text": "Knarr",           "count": 241},
        {"text": "Cotton",          "count": 218},
        {"text": "Pickaxe",         "count": 195},
        {"text": "File",            "count": 168},
        {"text": "Helm",            "count": 148},
        {"text": "Large Anvil",     "count": 138},
        {"text": "Gem",             "count": 125},
        {"text": "Rune",            "count": 112},
        {"text": "Chain Armour",    "count": 102},
        {"text": "Grindstone",      "count":  92},
        {"text": "Dragon Scale",    "count":  85},
        {"text": "Source Crystal",  "count":  78},
        {"text": "Hell Horse",      "count":  72},
        {"text": "Saddle",          "count":  65},
        {"text": "Corbita",         "count":  58},
        {"text": "Whetstone",       "count":  52},
    ],
    "enchants": [
        {"text": "Circle of Cunning",    "count": 512},
        {"text": "Wind of Ages",         "count": 488},
        {"text": "Life Transfer",        "count": 395},
        {"text": "Blessing of the Dark", "count": 340},
        {"text": "Nimbleness",           "count": 298},
        {"text": "Flaming Aura",         "count": 195},
        {"text": "Frostbrand",           "count": 178},
        {"text": "Courier",              "count": 148},
        {"text": "Aura of Shared Pain",  "count": 142},
        {"text": "Venom",                "count": 118},
        {"text": "Mind Stealer",         "count":  92},
        {"text": "Oakshell",             "count":  72},
    ],
    "professions": [
        {"text": "Smithing",        "count": 480},
        {"text": "Channeling",      "count": 395},
        {"text": "Carpentry",       "count": 248},
        {"text": "Tailoring",       "count": 195},
        {"text": "Leatherworking",  "count": 168},
        {"text": "Cooking",         "count": 142},
        {"text": "Animal Husbandry","count": 118},
        {"text": "Masonry",         "count":  95},
        {"text": "Shipbuilding",    "count":  78},
        {"text": "Jewelry",         "count":  62},
        {"text": "Farming",         "count":  48},
        {"text": "Bowery",          "count":  35},
    ],
    "services": [
        {"text": "Improving",            "count": 1580},
        {"text": "Enchanting",           "count": 1120},
        {"text": "Transport",            "count": 310},
        {"text": "Terraforming",         "count": 185},
        {"text": "Bridge Construction",  "count": 118},
        {"text": "Butchering",           "count":  88},
        {"text": "Delivery",             "count":  72},
        {"text": "Highway Construction", "count":  55},
        {"text": "Training",             "count":  42},
        {"text": "Guide Service",        "count":  35},
    ]
}


def scale_tokens(tokens_dict, factor=1.0):
    """Scale all counts by a factor for different corpora/years."""
    result = {}
    for key, lst in tokens_dict.items():
        result[key] = [
            {"text": t["text"], "count": max(1, int(t["count"] * factor))}
            for t in lst
        ]
    return result


def patch_file(path, total_count, weekday_pattern, tokens_dict, n_weeks=52):
    """Load a JSON file and inject by_weekday + tokens fields."""
    if not os.path.exists(path):
        print(f"  SKIP (not found): {path}")
        return

    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    data["by_weekday"] = build_weekday(total_count, weekday_pattern, n_weeks)
    data["tokens"]     = tokens_dict

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"  PATCHED: {os.path.basename(path)}")


# ─── Patch all partitions ────────────────────────────────────────────────────

DATA_DIR = "src/data"

FILES = [
    # (filename, total_count, weekday_pattern, tokens, n_weeks)
    ("nfi-seller-activity-2025.json",      12000, WTS_WEEKDAY_BASE, SELLER_TOKENS, 52),
    ("nfi-seller-activity-2026-ytd.json",   4800, WTS_WEEKDAY_BASE, scale_tokens(SELLER_TOKENS, 0.42), 21),
    ("sfi-seller-activity-2025.json",       5200, WTS_WEEKDAY_BASE, scale_tokens(SELLER_TOKENS, 0.45), 52),
    ("sfi-seller-activity-2026-ytd.json",   2100, WTS_WEEKDAY_BASE, scale_tokens(SELLER_TOKENS, 0.19), 21),

    ("nfi-buyer-activity-2025.json",        8500, WTB_WEEKDAY_BASE, BUYER_TOKENS, 52),
    ("nfi-buyer-activity-2026-ytd.json",    3400, WTB_WEEKDAY_BASE, scale_tokens(BUYER_TOKENS, 0.42), 21),
    ("sfi-buyer-activity-2025.json",        3800, WTB_WEEKDAY_BASE, scale_tokens(BUYER_TOKENS, 0.45), 52),
    ("sfi-buyer-activity-2026-ytd.json",    1520, WTB_WEEKDAY_BASE, scale_tokens(BUYER_TOKENS, 0.19), 21),
]

print("Patching JSON files with by_weekday and tokens fields...\n")
for fname, count, pattern, tokens, weeks in FILES:
    path = os.path.join(DATA_DIR, fname)
    patch_file(path, count, pattern, tokens, weeks)

print("\nDone.")
