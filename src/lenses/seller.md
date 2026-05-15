---
title: Seller Activity Lens
toc: false
---

```js
import * as Plot from "npm:@observablehq/plot";
import { html } from "npm:htl";
import { CorpusHealthCard } from "../components/corpus-health.js";
import { t, LanguageSelector, ServerSelector, lang, server } from "../components/i18n.js";

const nfi_meta = await FileAttachment("../data/nfi-corpus-meta.json").json();
const sfi_meta = await FileAttachment("../data/sfi-corpus-meta.json").json();
const nfi_data = await FileAttachment("../data/nfi-seller-activity.json").json();
const sfi_data = await FileAttachment("../data/sfi-seller-activity.json").json();

const meta = server.value === "NFI" ? nfi_meta : sfi_meta;
const data = server.value === "NFI" ? nfi_data : sfi_data;
const corpus = meta.active;
const maxCount = data.top_sellers[0] ? data.top_sellers[0].count : 1;
```

<div class="obs-page">

<div style="padding: 2rem 0; border-bottom: 1px solid var(--border); margin-bottom: 3rem;">
<div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:1rem">
<div>
<a href="/" style="font-size:0.75rem; color:var(--amber); text-decoration:none; text-transform:uppercase; letter-spacing:1px">${t("back")}</a>
</div>
<div style="display:flex; gap:8px; align-items:center;">
${ServerSelector()}
${LanguageSelector()}
</div>
</div>

<h1 class="obs-hero-title">${t("seller_title")}</h1>
<p class="obs-hero-sub">${lang.value === "pt" ? "Quem vende e o que vendem no corpus de " + server.value : "Who sells and what they sell on " + server.value}</p>
</div>

<div class="obs-grid-4" style="display:grid; grid-template-columns: repeat(4, 1fr); gap:1.5rem; margin-bottom:2rem">
<div class="obs-card">
<div class="obs-label" style="margin-bottom:8px">${t("unique_sellers")}</div>
<div class="stat-card-val">${data.summary.unique_sellers}</div>
</div>
<div class="obs-card">
<div class="obs-label" style="margin-bottom:8px">${t("total_listings")}</div>
<div class="stat-card-val">${data.summary.total_listings.toLocaleString()}</div>
</div>
<div class="obs-card">
<div class="obs-label" style="margin-bottom:8px">${t("top_category")}</div>
<div class="stat-card-val" style="font-size:1.1rem; text-transform:uppercase">${data.summary.top_category}</div>
</div>
<div class="obs-card">
<div class="obs-label" style="margin-bottom:8px">${t("coverage")}</div>
<div class="stat-card-val">${Math.round(data.coverage * 100)}%</div>
</div>
</div>

<div class="obs-section">
<div class="obs-label">${t("daily_activity")}</div>

```js
display(Plot.plot({
  width: 860,
  height: 120,
  style: { background: "transparent", color: "var(--ink-3)", fontFamily: "var(--font-mono)", fontSize: 10 },
  marks: [
    Plot.areaY(data.daily_activity, { x: "date", y: "count", fill: "var(--amber)", fillOpacity: 0.1 }),
    Plot.lineY(data.daily_activity, { x: "date", y: "count", stroke: "var(--amber)", strokeWidth: 1.5 })
  ]
}));
```
</div>

<div class="obs-section" style="margin-top:4rem">
<div class="obs-label">${t("source_corpus")}</div>
${CorpusHealthCard(corpus)}
</div>

</div>
