---
title: Seller Activity Lens
toc: false
---

```js
import * as Plot from "npm:@observablehq/plot";
import { html } from "npm:htl";
import { CorpusHealthCard } from "../components/corpus-health.js";
import { t, LanguageSelector, lang } from "../components/i18n.js";

// Carregamento estático (roda uma vez)
const nfi_meta = await FileAttachment("../data/nfi-corpus-meta.json").json();
const sfi_meta = await FileAttachment("../data/sfi-corpus-meta.json").json();
const nfi_data = await FileAttachment("../data/nfi-seller-activity.json").json();
const sfi_data = await FileAttachment("../data/sfi-seller-activity.json").json();
```

```js
// Seletor nativo reativo do Observable (garantido)
const serverView = Inputs.select(["NFI", "SFI"], {value: "NFI"});
const serverVal  = Generators.input(serverView);
```

```js
// Bloco reativo — re-executa quando serverVal ou lang mudam
const meta     = serverVal === "NFI" ? nfi_meta : sfi_meta;
const data     = serverVal === "NFI" ? nfi_data : sfi_data;
const corpus   = meta.active;
const maxCount = data.top_sellers[0] ? data.top_sellers[0].count : 1;
const observed = data.daily_activity.filter(d => !d.is_gap);
const gaps_arr = data.daily_activity.filter(d =>  d.is_gap);
const langVal  = lang.value || "pt";
```

```js
display(html`<div class="obs-page">

<div style="padding: 2rem 0 1.5rem; border-bottom: 0.5px solid var(--border); margin-bottom: 2rem;">
  <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.5rem">
    <div>
      <a href="/" style="font-size:0.7rem;color:var(--amber);text-decoration:none;letter-spacing:0.5px">${t("back")}</a>
      <span style="font-size:0.7rem;color:var(--ink-4);margin:0 0.5rem">/</span>
      <span style="font-size:0.7rem;color:var(--ink-4);letter-spacing:0.5px">${t("lens_v")}</span>
    </div>
    <div style="display:flex; gap:8px; align-items:center;">
      ${serverView}
      ${LanguageSelector()}
    </div>
  </div>
  <h1 class="obs-hero-title">${t("seller_title")}</h1>
  <p class="obs-hero-sub">${langVal === "pt" ? "Quem vende e o que vendem no corpus de " + serverVal : "Who sells and what they sell on " + serverVal}</p>
</div>

<div class="method-note" style="margin-bottom:1.5rem">
  <strong>${t("methodology_note")}</strong>
  <strong>${t("coverage")}: ${Math.round(data.coverage * 100)}%.</strong>
</div>

<div class="obs-grid-4" style="margin-bottom:1.5rem">
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
    <div class="stat-card-val">${data.summary.top_category}</div>
  </div>
  <div class="stat-card">
    <div class="stat-card-label">${t("peak_day")}</div>
    <div class="stat-card-val">${data.summary.peak_day}</div>
  </div>
</div>

</div>`);
```

```js
display(html`<div class="obs-page" style="padding-top:0">
<div class="chart-wrap" style="margin-bottom:1.25rem">
  <div class="chart-header">
    <div class="obs-label" style="margin-bottom:0">${t("daily_activity")} — ${corpus.period} (${serverVal})</div>
    <span class="cov-badge warn">⚠ ${Math.round(data.coverage * 100)}% coverage</span>
  </div>
  ${Plot.plot({
    width: 740, height: 180, marginLeft: 40, marginRight: 10,
    style: { fontFamily: "var(--font-mono)", fontSize: 10, background: "transparent", color: "var(--ink-3)" },
    x: { label: null, ticks: 10 },
    y: { label: null, grid: true },
    marks: [
      Plot.barY(gaps_arr,  { x: "date", y2: 300, fill: "var(--gap)", opacity: 0.5 }),
      Plot.areaY(observed, { x: "date", y: "count", fill: "var(--amber)", fillOpacity: 0.15 }),
      Plot.lineY(observed, { x: "date", y: "count", stroke: "var(--amber)", strokeWidth: 1.5 }),
      Plot.ruleY([0], { stroke: "var(--border)" })
    ]
  })}
</div>
</div>`);
```

```js
display(html`<div class="obs-page" style="padding-top:0">
<div class="obs-grid-2" style="margin-bottom:1.25rem; gap:1rem">
  <div class="chart-wrap">
    <div class="obs-label">${langVal === "pt" ? "Volume por Categoria" : "Listings by Category"}</div>
    ${Plot.plot({
      width: 320, height: 220, marginLeft: 82,
      style: { fontFamily: "var(--font-mono)", fontSize: 10, background: "transparent", color: "var(--ink-3)" },
      marks: [
        Plot.barX(data.by_category, { x: "count", y: "category", fill: "var(--amber)", sort: { y: "-x" } }),
        Plot.ruleX([0], { stroke: "var(--border)" })
      ]
    })}
  </div>
  <div class="chart-wrap">
    <div class="obs-label" style="margin-bottom:0.75rem">${langVal === "pt" ? "Top Vendedores" : "Top Sellers"}</div>
    ${html`<div>${data.top_sellers.slice(0,12).map((s,i) => html`<div class="rank-row">
      <span class="rank-n">${i+1}</span>
      <span class="rank-name">${s.name}</span>
      <div class="rank-bar-cell">
        <div class="rank-bar" style="width:${Math.round(s.count/maxCount*100)}px"></div>
        <span class="rank-count">${s.count}</span>
      </div>
    </div>`)}</div>`}
  </div>
</div>
</div>`);
```

```js
display(html`<div class="obs-page" style="padding-top:0">
<div class="obs-section">
  <div class="obs-label">${t("source_corpus")}</div>
  ${CorpusHealthCard(corpus)}
</div>
</div>`);
```
