---
title: Observatory
toc: false
---

```js
import { CorpusHealthCard } from "./components/corpus-health.js";
import { CoverageTimeline }  from "./components/coverage-timeline.js";
import { LensCard }          from "./components/lens-card.js";

const meta   = await FileAttachment("data/corpus-meta.json").json();
const corpus = meta.active;
const seller = await FileAttachment("data/seller-activity.json").json();
```

<div class="obs-page">

  <div class="obs-hero">
    <div class="obs-hero-eyebrow">Wurm Market Observatory</div>
    <h1 class="obs-hero-title">An archaeological record of Wurm Online's economy</h1>
    <p class="obs-hero-sub">
      Interpretive lenses built from restored corpora. Coverage is partial.<br>
      Data represents <em>observed mentions</em>, not confirmed transactions.<br>
      Each lens is a reading — not a truth.
    </p>
    <div class="derived-badge">
      ◆ derived data — source: historical archive — not canonical
    </div>
  </div>

  <!-- CORPUS HEALTH -->
  <div class="obs-section">
    <div class="obs-label">Active corpus</div>
    ${CorpusHealthCard(corpus)}
  </div>

  <!-- TIMELINE -->
  <div class="obs-section">
    <div class="obs-label">Reconstructed chronology — all corpora</div>
    ${CoverageTimeline(meta.all_corpora)}
  </div>

  <!-- RECENT OBSERVATIONS -->
  <div class="obs-section">
    <div class="obs-label">Recent observations</div>

```js
html`<div class="obs-items">
  <div class="obs-item">
    <div class="obs-dot"></div>
    <div>
      <div class="obs-text">
        Observed surge in weapon listings during late November —
        concentration in longswords and plate armour.
        <strong>${seller.summary.top_category}</strong> category accounts for
        ${Math.round(seller.summary.top_category_pct * 100)}% of all mentions.
      </div>
      <div class="obs-meta">seller_activity · Nov 2024 · ${Math.round(seller.coverage * 100)}% cov</div>
    </div>
  </div>
  <div class="obs-item">
    <div class="obs-dot"></div>
    <div>
      <div class="obs-text">
        Saturday activity consistently <strong>${seller.summary.peak_day_multiplier}×</strong>
        weekday volume across all covered periods. Pattern holds across corpora.
      </div>
      <div class="obs-meta">trade_density · multi-corpus · partial</div>
    </div>
  </div>
  <div class="obs-item">
    <div class="obs-dot"></div>
    <div>
      <div class="obs-text">
        Rare mirror mentions remain extremely sparse — fewer than 3 appearances per covered month.
        Possibly underrepresented due to private channels.
      </div>
      <div class="obs-meta">rare_item · Nov 2024 · 71% cov · low confidence</div>
    </div>
  </div>
  <div class="obs-item">
    <div class="obs-dot"></div>
    <div>
      <div class="obs-text">
        Trade visibility decreases sharply during early November gaps.
        Archival absence or genuine market lull — indeterminate from corpus alone.
      </div>
      <div class="obs-meta">field annotation · Nov 6–8 · unverifiable</div>
    </div>
  </div>
</div>`
```

  </div>

  <!-- LENSES -->
  <div class="obs-section">
    <div class="obs-label">Available lenses</div>
    <div class="obs-grid-lenses">
      ${LensCard({
        href: "/lenses/seller",
        icon: "ti-user-circle",
        name: "Seller Activity",
        insight: `${seller.summary.unique_sellers} unique sellers identified across 4 corpora`,
        coverage: corpus.coverage,
        period: corpus.period,
        status: "active",
        version: "v0.1"
      })}
      ${LensCard({
        href: "#",
        icon: "ti-search",
        name: "Buyer Activity",
        insight: "WTB signals across 12 item categories",
        coverage: corpus.coverage,
        period: corpus.period,
        status: "active",
        version: "v0.1"
      })}
      ${LensCard({
        href: "#",
        icon: "ti-chart-area",
        name: "Trade Density",
        insight: "Activity peaks Fri–Sat evenings UTC",
        coverage: 0.43,
        period: "partial",
        status: "partial",
        version: "v0.1"
      })}
      ${LensCard({
        href: "#",
        icon: "ti-diamond",
        name: "Rare Item",
        insight: "19 legendary-tier items tracked",
        coverage: corpus.coverage,
        period: corpus.period,
        status: "active",
        version: "v0.1"
      })}
      ${LensCard({
        href: "#",
        icon: "ti-map-pin",
        name: "Regional Activity",
        insight: "Territory not yet restored. Multi-server corpus required.",
        coverage: null,
        period: null,
        status: "uncharted"
      })}
    </div>
  </div>

</div>
