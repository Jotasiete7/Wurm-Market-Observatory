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

<div style="padding: 1.5rem 0; border-bottom: 0.5px solid var(--border); margin-bottom: 2rem;">
<div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.5rem">
<div>
<a href="/" style="font-size:0.7rem;color:var(--amber);text-decoration:none;">${t("back")}</a>
</div>
<div style="display:flex; gap:8px; align-items:center;">
${ServerSelector()}
${LanguageSelector()}
</div>
</div>

# ${t("seller_title")}

</div>

<div class="obs-card" style="margin-bottom:1.5rem">
<div class="stat-card-val">${Math.round(data.coverage * 100)}%</div>
<div class="corpus-stat-label">${t("coverage")} — ${corpus.period} (${server.value})</div>
</div>

<div class="obs-grid-4" style="display:grid; grid-template-columns: repeat(4, 1fr); gap:1rem; margin-bottom:1.5rem">
<div class="stat-card">
<div class="stat-card-label">${t("unique_sellers")}</div>
<div class="stat-card-val">${data.summary.unique_sellers}</div>
</div>
<div class="stat-card">
<div class="stat-card-label">${t("total_listings")}</div>
<div class="stat-card-val">${data.summary.total_listings}</div>
</div>
</div>

<div class="obs-section">
<div class="obs-label">${t("daily_activity")}</div>
```js
display(Plot.plot({
  width: 680,
  height: 80,
  style: { background: "transparent", color: "var(--ink)" },
  marks: [
    Plot.lineY(data.daily_activity, { x: "date", y: "count", stroke: "var(--amber)" })
  ]
}));
```
</div>

<div class="obs-section">
<div class="obs-label">${t("source_corpus")}</div>
${CorpusHealthCard(corpus)}
</div>

</div>
