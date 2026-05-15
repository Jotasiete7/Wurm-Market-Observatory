# Wurm Market Observatory

> **An archaeological record of Wurm Online's economy.**

The Wurm Market Observatory is a data publication platform that analyzes historical trade channel logs from the game Wurm Online. It serves as an interpretive layer built upon the [Wurm Historical Archive](https://github.com/Jotasiete7/wurm-archive).

## 🏛️ Project Philosophy

This project is guided by the metaphor of **archaeology**. We treat trade logs not as a live data stream, but as "site samples" or "restored corpora" from a specific temporal period.

### 1. Epistemic Honesty
We prioritize showing what we *don't* know as much as what we do.
- **Lacunae (Gaps)**: Periods with missing log data are never interpolated or "guessed." They are explicitly marked with diagonal hatching to represent archival absence.
- **Derived Data**: Every chart and stat is a "reading" of a corpus. We don't claim to show "the market," but rather "what was observed in the available logs."

### 2. Methodological Transparency
Every lens (analytical view) used in the observatory is documented. We distinguish between "Seller Activity" (counts of mentions) and actual "Transactions" (which are off-channel and unverifiable).

---

## 🏗️ Architecture: Why no Database?

A core technical decision of the Observatory is that it **does not read directly from a live database.** Instead, it consumes pre-computed **JSON Corpora**.

### Why this approach?

1.  **Reproducibility**: By analyzing a static JSON export (a corpus), we ensure that the analysis is reproducible. A lens applied to the same corpus will always yield the same result, regardless of how the source database grows.
2.  **Performance & Portability**: Being 100% static means the site is incredibly fast, has zero backend overhead, and can be hosted anywhere (currently Cloudflare Pages).
3.  **Security by Decoupling**: The source database and the ingestion pipeline remain private and protected. Only the derived, anonymized analytical data is exposed to the public frontend.
4.  **The "Site Sample" Metaphor**: Just as an archaeologist analyzes a specific dig site, the Observatory analyzes a specific corpus. This decoupling allows us to version our datasets alongside our code.

### The Pipeline
1.  **Ingestion**: Raw logs are uploaded to the Historical Archive.
2.  **Restoration**: Logs are cleaned, deduplicated, and time-synchronized.
3.  **Extraction**: Python scripts process the cleaned logs into structured JSON datasets.
4.  **Observation**: This project (Observable Framework) reads those JSONs and renders the UI.

---

## 🛠️ Tech Stack

- **[Observable Framework](https://observablehq.com/framework/)**: A static site generator designed specifically for data-rich applications.
- **[Observable Plot](https://observablehq.com/plot/)**: A concise, expressive JS library for exploratory data visualization.
- **[htl](https://github.com/observablehq/htl)**: For safe, expressive HTML templating within JavaScript.
- **Vanilla CSS**: A custom design system built to evoke the feeling of a scholarly, institutional archive (Playfair Display, JetBrains Mono, creamy parchment tones).
- **Tabler Icons**: For lightweight, consistent iconography.

---

## 📂 Project Organization

```text
src/
├── index.md           # Homepage (Overview & Recent Observations)
├── corpus.md          # Corpus Explorer (Health & Coverage metrics)
├── methodology.md     # Project philosophy & data caveats
├── components/        # Reusable UI components (LensCard, Timeline, etc.)
├── data/              # Pre-computed JSON corpora
├── lenses/            # Specific analytical pages (Seller Activity, etc.)
└── style/             # Design system and typography
```

---

## 🚀 Getting Started

To run the observatory locally:

1.  **Clone the repo**:
    ```bash
    git clone https://github.com/Jotasiete7/Wurm-Market-Observatory.git
    cd Wurm-Market-Observatory
    ```

2.  **Install dependencies**:
    ```bash
    npm install
    ```

3.  **Run the dev server**:
    ```bash
    npm run dev
    ```
    Visit `http://localhost:3000` to see the results.

---

## 📜 Disclaimer
The Wurm Market Observatory is a fan-made research project. It is not affiliated with Code Club AB or the Wurm Online development team. Data is derived from public trade channels and should be considered an estimate for historical research purposes only.
