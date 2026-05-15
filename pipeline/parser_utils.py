import re

def normalize_price(price_str: str) -> float:
    """
    Normalizes a price string into a numeric Copper value.
    Example: '1s 50c' -> 150.0
    """
    if not price_str:
        return 0.0
        
    s = str(price_str).lower().strip()
    if not s or s in ('nan', 'none'):
        return 0.0

    s = s.replace(',', '.')
    
    # Direct numeric check
    if re.match(r'^-?\d+(\.\d+)?$', s):
        try:
            return float(s)
        except ValueError:
            return 0.0

    total_copper = 0.0
    regex = re.compile(r'([\d.]+)\s*([gsci])')
    found_match = False
    
    for match in regex.finditer(s):
        found_match = True
        try:
            val = float(match.group(1))
            unit = match.group(2)
            
            if unit == 'g': total_copper += val * 10000.0
            elif unit == 's': total_copper += val * 100.0
            elif unit == 'c': total_copper += val
            elif unit == 'i': total_copper += val / 100.0
        except ValueError:
            continue
            
    if found_match:
        return total_copper
        
    return 0.0

def extract_ql_and_qty(raw_text: str):
    """
    Extracts QL and Quantity from the raw message text.
    """
    ql = 50.0
    qty = 1
    
    # QL parsing
    ql_match = re.search(r'QL:\s*(\d+(\.\d+)?)', raw_text, re.IGNORECASE)
    if ql_match:
        try:
            ql = float(ql_match.group(1))
        except ValueError:
            pass
    else:
        ql_match = re.search(r'\b(\d+(\.\d+)?)\s*ql\b', raw_text, re.IGNORECASE)
        if ql_match:
            try:
                ql = float(ql_match.group(1))
            except ValueError:
                pass
                
    # Quantity parsing
    qty_match = re.search(r'\b(\d+)\s*x\b', raw_text, re.IGNORECASE)
    if qty_match:
        try:
            qty = int(qty_match.group(1))
        except ValueError:
            pass
    else:
        qty_match = re.search(r'\bx\s*(\d+)\b', raw_text, re.IGNORECASE)
        if qty_match:
            try:
                qty = int(qty_match.group(1))
            except ValueError:
                pass
                
    return ql, qty

def extract_rarity(raw_text: str) -> str:
    """Extract rarity from text."""
    lower = raw_text.lower()
    if 'fantastic' in lower: return 'Fantastic'
    if 'supreme' in lower: return 'Supreme'
    if 'rare' in lower: return 'Rare'
    return 'Common'

def resolve_item_identity(raw_text: str, config: dict) -> dict:
    """
    Cleans raw text to find the canonical item name.
    """
    cleaning_cfg = config.get("cleaning", {})
    aliases = cleaning_cfg.get("aliases", {})
    noise_terms = set(cleaning_cfg.get("ignored_terms", []))
    noise_prefixes = set(cleaning_cfg.get("ignored_prefixes", []))
    service_terms = set(cleaning_cfg.get("service_terms", []))
    semantic_items = config.get("semantic_items", {})
    
    # 1. Initial Name Extraction (Extract from brackets if available)
    raw_name = raw_text
    match = re.search(r'\[(.*?)\]', raw_text)
    if match:
        raw_name = match.group(1)
        
    cleaned = raw_name.lower().strip()
    
    # 2. Strip Commercial Prefixes (WTS, WTB, etc.)
    prefixes = config.get("cleaning", {}).get("wts_keywords", []) + \
               config.get("cleaning", {}).get("wtb_keywords", []) + \
               ["wtb", "wts", "buying", "selling", "want", "to", "buy", "sell"]
    
    for pref in prefixes:
        cleaned = re.sub(rf"^\b{re.escape(pref.lower())}\b", "", cleaned).strip()

    # If the message contains service terms, flag as unknown
    words = cleaned.split()
    if any(w in service_terms for w in words):
        return {"id": "unknown", "name": "Unknown (Service)"}
        
    # Basic Cleaning
    cleaned = re.sub(r'\[.*?\]', '', cleaned)
    cleaned = re.sub(r'\b(ql|dmg|wt)[:\s]*[\d.]+', '', cleaned)
    cleaned = re.sub(r'\b\d+(\.\d+)?\s*ql\b', '', cleaned)
    cleaned = re.sub(r'\bx?\s*\d+\s*x?\b', '', cleaned)  # remove quantities
    
    words = re.split(r'[\s-]+', cleaned)
    filtered_words = []
    
    for w in words:
        if not w: continue
        if re.match(r'^\d+(\.\d+)?$', w): continue
        if w in noise_terms: continue
        if w in noise_prefixes: continue
        if w in service_terms: continue
        filtered_words.append(w)
        
    joined = " ".join(filtered_words).strip()
    
    if joined in aliases:
        joined = aliases[joined]
        
    final_name = joined
    
    for key, c in semantic_items.items():
        if key.replace('_', ' ') in joined:
            if c.get("collapseMaterials", False):
                final_name = c.get("displayName", key).lower()
                
    # Specific sleep powder check
    if 'sleep powder' in joined:
        final_name = 'sleep powder'
        
    id_str = re.sub(r'[^a-z0-9]+', '_', final_name).strip('_')
    
    if not id_str:
        return {"id": "unknown", "name": "Unknown"}
        
    return {"id": id_str, "name": final_name.title()}
