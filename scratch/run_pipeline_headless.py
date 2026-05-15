import sys
import json
from pathlib import Path
from datetime import datetime

# Setup paths
PIPELINE_DIR = Path("pipeline")
sys.path.insert(0, str(PIPELINE_DIR))

import core
import lenses as lens_mod

def run():
    print("--- Running Headless Pipeline ---")
    
    # Load config
    with open(PIPELINE_DIR / "config.json", "r", encoding="utf-8") as f:
        config = json.load(f)
        
    # Find the corpus file
    corpus_path = Path("pipeline/WurmArchive_NFI_Restored_12m.txt")
        
    print(f"Using corpus: {corpus_path}")
    
    # Parse
    result = core.parse_file(corpus_path, config)
    coverage = core.compute_coverage(result)
    
    # Output dir
    out_dir = Path("src/data")
    out_dir.mkdir(parents=True, exist_ok=True)
    
    srv_prefix = config.get("observatory", {}).get("server", "NFI").lower() + "-"
    print(f"Output prefix: {srv_prefix}")
    
    # 1. corpus-meta.json
    print(f"Generating {srv_prefix}corpus-meta.json...")
    meta = core.build_corpus_meta(result, coverage, config)
    with open(out_dir / f"{srv_prefix}corpus-meta.json", "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=2, ensure_ascii=False)
        
    # 2. seller-activity.json
    print(f"Generating {srv_prefix}seller-activity.json...")
    seller_data = lens_mod.process_seller_lens(result, coverage, config)
    with open(out_dir / f"{srv_prefix}seller-activity.json", "w", encoding="utf-8") as f:
        json.dump(seller_data, f, indent=2, ensure_ascii=False)
        
    # 3. buyer-activity.json
    print(f"Generating {srv_prefix}buyer-activity.json...")
    buyer_data = lens_mod.process_buyer_lens(result, coverage, config)
    with open(out_dir / f"{srv_prefix}buyer-activity.json", "w", encoding="utf-8") as f:
        json.dump(buyer_data, f, indent=2, ensure_ascii=False)
        
    print("Pipeline complete. Files saved in src/data")

if __name__ == "__main__":
    run()
