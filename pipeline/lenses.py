"""
lenses.py — Lens Processors for the Corpus Workbench
Each function takes a ParseResult + config and returns a JSON-ready dict.
"""

import re
from datetime import date
from collections import defaultdict
from core import ParseResult, CoverageResult
import parser_utils


# ─── Seller Activity Lens ────────────────────────────────────────────────────

def process_seller_lens(result: ParseResult, cov: CoverageResult, config: dict) -> dict:
    """
    Seller Activity Lens.
    Counts WTS mentions per player, per day, per category.
    Coverage per seller = % of covered days they appeared in.
    """
    lens_cfg  = config.get("lenses", {}).get("seller_activity", {})
    cleaning  = config.get("cleaning", {})
    categories = config.get("categories", {})

    wts_kw    = [k.lower() for k in cleaning.get("wts_keywords", ["wts", "selling", "for sale"])]
    top_n     = lens_cfg.get("top_sellers_count", 10)
    min_mentions = lens_cfg.get("min_mentions", 3)

    # Filter: only WTS lines
    wts_lines = [l for l in result.lines if _is_wts(l.message, wts_kw)]

    if not wts_lines:
        return _empty_seller_json(result, cov, config)

    # Daily counts: {date: total_count}
    daily_counts = defaultdict(int)
    for line in wts_lines:
        daily_counts[line.day] += 1

    # Per-seller stats
    seller_days    = defaultdict(set)   # player → set of days active
    seller_counts  = defaultdict(int)   # player → total mentions
    seller_msgs    = defaultdict(list)  # player → list of messages
    seller_items   = defaultdict(list)  # player → parsed items

    for line in wts_lines:
        seller_days[line.player].add(line.day)
        seller_counts[line.player] += 1
        seller_msgs[line.player].append(line.message)
        
        # Advanced Parsing
        price = parser_utils.normalize_price(line.message)
        ql, qty = parser_utils.extract_ql_and_qty(line.message)
        rarity = parser_utils.extract_rarity(line.message)
        item_id = parser_utils.resolve_item_identity(line.message, config)
        
        if item_id["id"] != "unknown":
            seller_items[line.player].append({
                "id": item_id["id"],
                "name": item_id["name"],
                "price": price,
                "qty": qty,
                "ql": ql,
                "rarity": rarity,
                "date": line.day.isoformat()
            })

    # Coverage per seller (% of corpus-covered days they appeared in)
    covered_days = set(cov.days_found)
    total_covered = max(len(covered_days), 1)

    sellers = []
    for player, count in seller_counts.items():
        if count < min_mentions:
            continue
        seller_cov = round(len(seller_days[player] & covered_days) / total_covered, 4)
        top_item   = _top_item(seller_msgs[player], categories)
        sellers.append({
            "name":     player,
            "count":    count,
            "coverage": seller_cov,
            "top_item": top_item,
            "parsed_items": seller_items[player]
        })

    sellers.sort(key=lambda s: s["count"], reverse=True)
    top_sellers = sellers[:top_n]

    # Category breakdown
    cat_counts = defaultdict(int)
    for line in wts_lines:
        cat = _categorize(line.message, categories)
        cat_counts[cat] += 1

    total_wts = sum(cat_counts.values()) or 1
    by_category = [
        {"category": cat, "count": count, "pct": round(count / total_wts, 4)}
        for cat, count in sorted(cat_counts.items(), key=lambda x: -x[1])
    ]

    # Summary stats
    unique_sellers   = len([s for s in sellers])  # already filtered by min_mentions
    total_listings   = sum(seller_counts.values())
    top_cat          = by_category[0]["category"] if by_category else "Unknown"
    top_cat_pct      = by_category[0]["pct"]      if by_category else 0.0
    peak_day, peak_mult = _peak_day(daily_counts, cov.days_found)

    # Build daily_activity array (all days in period, with gaps)
    from datetime import timedelta
    daily_activity = []
    if result.period_start and result.period_end:
        d = result.period_start
        day_num = 1
        while d <= result.period_end:
            is_gap = d not in covered_days
            daily_activity.append({
                "day":   day_num,
                "date":  d.isoformat(),
                "count": None if is_gap else daily_counts.get(d, 0),
                "gap":   is_gap
            })
            d += timedelta(days=1)
            day_num += 1

    obs_cfg = config.get("observatory", {})
    from datetime import datetime
    today = datetime.now().strftime("%Y-%m-%d")
    path  = result.file_path

    return {
        "lens":         "seller_activity",
        "corpus":       str(path).split("\\")[-1].split("/")[-1],
        "coverage":     round(cov.coverage_pct, 4),
        "generated_at": today,
        "confidence":   "partial" if cov.coverage_pct < 0.8 else "high",
        "gaps":         [f"{g['start']}/{g['end']}" for g in cov.gaps],
        "summary": {
            "unique_sellers":       unique_sellers,
            "total_listings":       total_listings,
            "top_category":         top_cat,
            "top_category_pct":     top_cat_pct,
            "peak_day":             peak_day,
            "peak_day_multiplier":  peak_mult
        },
        "daily_activity": daily_activity,
        "top_sellers":    top_sellers,
        "by_category":    by_category
    }


# ─── Buyer Activity Lens ─────────────────────────────────────────────────────

def process_buyer_lens(result: ParseResult, cov: CoverageResult, config: dict) -> dict:
    """
    Buyer Activity Lens.
    Counts WTB mentions per player and per category.
    """
    lens_cfg = config.get("lenses", {}).get("buyer_activity", {})
    cleaning = config.get("cleaning", {})
    categories = config.get("categories", {})

    wtb_kw   = [k.lower() for k in cleaning.get("wtb_keywords", ["wtb", "buying", "looking for"])]
    top_n    = lens_cfg.get("top_buyers_count", 10)
    min_mentions = lens_cfg.get("min_mentions", 3)

    wtb_lines = [l for l in result.lines if _is_wtb(l.message, wtb_kw)]

    buyer_counts = defaultdict(int)
    buyer_days   = defaultdict(set)
    buyer_msgs   = defaultdict(list)
    buyer_items  = defaultdict(list)

    for line in wtb_lines:
        buyer_counts[line.player] += 1
        buyer_days[line.player].add(line.day)
        buyer_msgs[line.player].append(line.message)

        # Advanced Parsing
        price = parser_utils.normalize_price(line.message)
        ql, qty = parser_utils.extract_ql_and_qty(line.message)
        rarity = parser_utils.extract_rarity(line.message)
        item_id = parser_utils.resolve_item_identity(line.message, config)
        
        if item_id["id"] != "unknown":
            buyer_items[line.player].append({
                "id": item_id["id"],
                "name": item_id["name"],
                "price": price,
                "qty": qty,
                "ql": ql,
                "rarity": rarity,
                "date": line.day.isoformat()
            })

    covered_days  = set(cov.days_found)
    total_covered = max(len(covered_days), 1)

    buyers = []
    for player, count in buyer_counts.items():
        if count < min_mentions:
            continue
        buyer_cov = round(len(buyer_days[player] & covered_days) / total_covered, 4)
        top_item  = _top_item(buyer_msgs[player], categories)
        buyers.append({
            "name":     player,
            "count":    count,
            "coverage": buyer_cov,
            "top_item": top_item,
            "parsed_items": buyer_items[player]
        })

    buyers.sort(key=lambda b: b["count"], reverse=True)

    cat_counts = defaultdict(int)
    for line in wtb_lines:
        cat_counts[_categorize(line.message, categories)] += 1

    total_wtb   = sum(cat_counts.values()) or 1
    by_category = [
        {"category": cat, "count": count, "pct": round(count / total_wtb, 4)}
        for cat, count in sorted(cat_counts.items(), key=lambda x: -x[1])
    ]

    from datetime import datetime
    today = datetime.now().strftime("%Y-%m-%d")

    return {
        "lens":         "buyer_activity",
        "corpus":       str(result.file_path).split("\\")[-1].split("/")[-1],
        "coverage":     round(cov.coverage_pct, 4),
        "generated_at": today,
        "confidence":   "partial" if cov.coverage_pct < 0.8 else "high",
        "gaps":         [f"{g['start']}/{g['end']}" for g in cov.gaps],
        "summary": {
            "unique_buyers":    len(buyers),
            "total_signals":    sum(buyer_counts.values()),
            "top_category":     by_category[0]["category"] if by_category else "Unknown",
            "top_category_pct": by_category[0]["pct"]      if by_category else 0.0
        },
        "top_buyers":   buyers[:top_n],
        "by_category":  by_category
    }


# ─── Helpers ─────────────────────────────────────────────────────────────────

def _is_wts(message: str, keywords: list) -> bool:
    msg = message.lower()
    for kw in keywords:
        if re.search(rf"\b{re.escape(kw.lower())}\b", msg):
            return True
    return False


def _is_wtb(message: str, keywords: list) -> bool:
    msg = message.lower()
    for kw in keywords:
        if re.search(rf"\b{re.escape(kw.lower())}\b", msg):
            return True
    return False


def _categorize(message: str, categories: dict) -> str:
    msg = message.lower()
    for cat, keywords in categories.items():
        if any(kw.lower() in msg for kw in keywords):
            return cat
    return "Other"


def _top_item(messages: list, categories: dict) -> str:
    """Find the single most common item keyword mentioned by this player."""
    counts = defaultdict(int)
    for msg in messages:
        ml = msg.lower()
        for cat, keywords in categories.items():
            for kw in keywords:
                if kw.lower() in ml:
                    counts[kw] += 1
    if not counts:
        return "Unknown"
    return max(counts, key=counts.get).capitalize()


def _peak_day(daily_counts: dict, days_found: list) -> tuple:
    """
    Compute the day-of-week with the highest average activity.
    Returns (day_name, multiplier_vs_weekday_avg).
    """
    dow_totals = defaultdict(int)
    dow_days   = defaultdict(int)

    for d, count in daily_counts.items():
        if d in set(days_found):
            wd = d.strftime("%A")
            dow_totals[wd] += count
            dow_days[wd]   += 1

    if not dow_totals:
        return ("Saturday", 1.0)

    dow_avgs = {
        wd: dow_totals[wd] / dow_days[wd]
        for wd in dow_totals
    }

    peak = max(dow_avgs, key=dow_avgs.get)

    weekday_names = {"Monday","Tuesday","Wednesday","Thursday","Friday"}
    weekday_vals  = [v for k, v in dow_avgs.items() if k in weekday_names]
    weekday_avg   = (sum(weekday_vals) / len(weekday_vals)) if weekday_vals else 1
    multiplier    = round(dow_avgs[peak] / weekday_avg, 1) if weekday_avg > 0 else 1.0

    return (peak, multiplier)


def _empty_seller_json(result: ParseResult, cov: CoverageResult, config: dict) -> dict:
    from datetime import datetime
    return {
        "lens":         "seller_activity",
        "corpus":       str(result.file_path).split("\\")[-1].split("/")[-1],
        "coverage":     round(cov.coverage_pct, 4),
        "generated_at": datetime.now().strftime("%Y-%m-%d"),
        "confidence":   "none",
        "gaps":         [],
        "summary": {
            "unique_sellers": 0, "total_listings": 0,
            "top_category": "None", "top_category_pct": 0.0,
            "peak_day": "Unknown", "peak_day_multiplier": 1.0
        },
        "daily_activity": [],
        "top_sellers":    [],
        "by_category":    []
    }
