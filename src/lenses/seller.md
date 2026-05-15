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

const meta   = server.value === "NFI" ? nfi_meta : sfi_meta;
const data   = server.value === "NFI" ? nfi_data : sfi_data;
const corpus = meta.active;
const maxCount = data.top_sellers[0] ? data.top_sellers[0].count : 1;
const serverName = server.value || "NFI";
const langVal = lang.value || "pt";
```

```js
display(html`<div class="obs-page">

<div style="padding: 2rem 0; border-bottom: 0.5px solid var(--border); margin-bottom: 2rem;">
  <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:1rem">
    <a href="/" style="font-size:0.65rem; color:var(--amber); text-decoration:none; text-transform:uppercase; letter-spacing:1px">${t("back")}</a>
    <div style="display:flex; gap:8px; align-items:center;">
      ${ServerSelector()}
      ${LanguageSelector()}
    </div>
  </div>
  <div class="obs-hero-eyebrow">${t("lens_v")}</div>
  <h1 class="obs-hero-title">${t("seller_title")}</h1>
  <p class="obs-hero-sub">${langVal === "pt" ? "Quem vende e o que vendem no corpus de " + serverName : "Who sells and what they sell on " + serverName}</p>
</div>

<div class="method-note" style="margin-bottom:2rem">
  ${t("methodology_note")}
</div>

<div class="obs-grid-4" style="margin-bottom:2rem">
  <div class="stat-card">
    <div class="stat-card-label">${t("unique_sellers")}</div>
    <div class="stat-card-val">${data.summary.unique_sellers}</div>
  </div>
  <div class="stat-card">
    <div class="stat-card-label">${t("total_listings")}</div>
    <div class="stat-card-val">${data.summary.total_listings.toLocaleString()}</div>
  </div>
  <div class="stat-card">
    <div class="stat-card-label">${t("top_category")}</div>
    <div class="stat-card-val" style="font-size:1rem; text-transform:uppercase">${data.summary.top_category}</div>
  </div>
  <div class="stat-card">
    <div class="stat-card-label">${t("coverage")}</div>
    <div class="stat-card-val">${Math.round(data.coverage * 100)}%</div>
  </div>
</div>

</div>`);
```

```js
display(Plot.plot({
  width: 860,
  height: 110,
  style: { background: "transparent", color: "var(--ink-3)", fontFamily: "var(--font-mono)", fontSize: 10 },
  marks: [
    Plot.areaY(data.daily_activity, { x: "date", y: "count", fill: "var(--amber)", fillOpacity: 0.12 }),
    Plot.lineY(data.daily_activity, { x: "date", y: "count", stroke: "var(--amber)", strokeWidth: 1.5 }),
    Plot.ruleX(data.daily_activity.filter(d => d.is_gap), { x: "date", stroke: "var(--gap)", strokeWidth: 2, strokeDasharray: "4,2" })
  ]
}));
```

```js
display(html`<div class="obs-page" style="padding-top:1rem">
<div class="obs-section">
  <div class="obs-label">${t("source_corpus")}</div>
  ${CorpusHealthCard(corpus)}
</div>
</div>`);
```
