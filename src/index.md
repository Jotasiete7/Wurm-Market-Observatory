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
    <div class="obs-label">Historical coverage — all corpora</div>
    ${CoverageTimeline(meta.all_corpora)}
  </div>

  <!-- LENSES -->
  <div class="obs-section">
    <div class="obs-label">Available lenses</div>
    <div class="obs-grid-lenses">
      ${LensCard({
        href: "/lenses/seller",
        icon: "ti-user-circle",
        name: "Seller Activity",
        insight: "287 unique sellers identified across 4 corpora",
        coverage: corpus.coverage,
        period: corpus.period,
        status: "active"
      })}
      ${LensCard({
        href: "/lenses/buyer",
        icon: "ti-search",
        name: "Buyer Activity",
        insight: "WTB signals across 12 item categories",
        coverage: corpus.coverage,
        period: corpus.period,
        status: "active"
      })}
      ${LensCard({
        href: "/lenses/density",
        icon: "ti-chart-area",
        name: "Trade Density",
        insight: "Activity peaks Fri–Sat evenings UTC",
        coverage: 0.43,
        period: "partial",
        status: "partial"
      })}
      ${LensCard({
        href: "#",
        icon: "ti-diamond",
        name: "Rare Item",
        insight: "19 legendary-tier items tracked",
        coverage: corpus.coverage,
        period: corpus.period,
        status: "active"
      })}
      ${LensCard({
        href: "#",
        icon: "ti-map-pin",
        name: "Regional Activity",
        insight: "Requires multi-server corpus — not yet available",
        coverage: null,
        period: null,
        status: "unavail"
      })}
    </div>
  </div>

</div>
