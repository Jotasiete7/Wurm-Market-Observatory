# Corpus Workbench

A local desktop tool for the **Wurm Market Observatory** pipeline.
Processes restored Wurm `.txt` log files into JSON datasets — no network, no database.

## How to run

From the `Wurm Market Observatory/` root folder:

```bash
py pipeline/gui.py
```

Or as a module:
```bash
py -m pipeline
```

## What it does

1. **Corpus tab** — select your restored `.txt` log file (downloaded from the Archive), click "Scan Corpus" to see coverage, gaps, and line counts.
2. **Settings tab** — configure WTS/WTB keywords, item categories, which lenses to generate, and the output path.
3. **Run tab** — click "Run Pipeline" to generate the JSON files.

## Output files

| File | Used by |
|---|---|
| `src/data/corpus-meta.json` | Homepage timeline, Corpus Explorer |
| `src/data/seller-activity.json` | Seller Activity lens |
| `src/data/buyer-activity.json` | Buyer Activity lens (if enabled) |

After running, refresh the Observatory dev server (`npm run dev`) and the site will show real data.

## Editing categories

Open `pipeline/config.json` and edit the `categories` section.
Each key is a category name, each value is a list of keywords matched case-insensitively.

## Requirements

- Python 3.10+ (you have 3.13 ✓)
- No extra dependencies — uses only Python standard library + tkinter (built-in)
