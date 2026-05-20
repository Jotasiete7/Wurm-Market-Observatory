---
title: Buyer Activity Lens
toc: false
---

```js
import * as Plot from "npm:@observablehq/plot";
import { html } from "npm:htl";
import { CorpusHealthCard } from "../components/corpus-health.js";
import { t, LanguageSelector, lang } from "../components/i18n.js";

// Carregamento de partições de dados
const dataPartitions = {
  NFI: {
    "2025": {
      meta: FileAttachment("../data/nfi-corpus-meta-2025.json"),
      data: FileAttachment("../data/nfi-buyer-activity-2025.json")
    },
    "2026-ytd": {
      meta: FileAttachment("../data/nfi-corpus-meta-2026-ytd.json"),
      data: FileAttachment("../data/nfi-buyer-activity-2026-ytd.json")
    }
  },
  SFI: {
    "2025": {
      meta: FileAttachment("../data/sfi-corpus-meta-2025.json"),
      data: FileAttachment("../data/sfi-buyer-activity-2025.json")
    },
    "2026-ytd": {
      meta: FileAttachment("../data/sfi-corpus-meta-2026-ytd.json"),
      data: FileAttachment("../data/sfi-buyer-activity-2026-ytd.json")
    }
  }
};
```

```js
// Seletor nativo reativo de servidor e período
const serverView = Inputs.select(["NFI", "SFI"], {value: "NFI"});
const serverVal  = Generators.input(serverView);

const periodView = Inputs.select([
  {label: "2025 (Jan–Dec)", value: "2025"},
  {label: "2026 (YTD)", value: "2026-ytd"}
], {value: "2025"});
const periodVal = Generators.input(periodView);
```

```js
// Bloco reativo — re-executa quando serverVal, periodVal ou lang mudam
const activeServer = serverVal === "SFI" ? "SFI" : "NFI";
const activePeriod = periodVal === "2026-ytd" ? "2026-ytd" : "2025";
const activePartition = dataPartitions[activeServer][activePeriod];
const meta     = await activePartition.meta.json();
const data     = await activePartition.data.json();
const corpus   = meta.active;
const maxCount = data.top_buyers[0] ? data.top_buyers[0].count : 1;
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
      ${periodView}
      ${LanguageSelector()}
    </div>
  </div>
  <h1 class="obs-hero-title">${t("buyer_title")}</h1>
  <p class="obs-hero-sub">${langVal === "pt" ? "Sinais de compra (WTB) no corpus de " + serverVal : "Buy signals (WTB) on " + serverVal}</p>
</div>

<div class="method-note" style="margin-bottom:1.5rem">
  <strong>${t("methodology_note")}</strong>
  <strong>${t("coverage")}: ${Math.round(data.coverage * 100)}%.</strong>
</div>

<div class="obs-grid-4" style="margin-bottom:1.5rem">
  <div class="stat-card">
    <div class="stat-card-label">${t("unique_buyers")}</div>
    <div class="stat-card-val">${data.summary.unique_buyers}</div>
  </div>
  <div class="stat-card">
    <div class="stat-card-label">${t("signals")}</div>
    <div class="stat-card-val">${data.summary.total_signals.toLocaleString()}</div>
  </div>
  <div class="stat-card">
    <div class="stat-card-label">${t("top_category")}</div>
    <div class="stat-card-val">${data.summary.top_category}</div>
  </div>
  <div class="stat-card">
    <div class="stat-card-label">${t("confidence")}</div>
    <div class="stat-card-val" style="font-size:0.85rem; text-transform:uppercase">${data.confidence}</div>
  </div>
</div>

</div>`);
```

```js
display(html`<div class="obs-page" style="padding-top:0">
<div class="obs-grid-2" style="margin-bottom:1.25rem; gap:1rem">
  <div class="chart-wrap">
    <div class="obs-label">${langVal === "pt" ? "Demanda por Categoria" : "Demand by Category"}</div>
    ${Plot.plot({
      width: 320, height: 220, marginLeft: 82,
      style: { fontFamily: "var(--font-mono)", fontSize: 10, background: "transparent", color: "var(--ink-3)" },
      marks: [
        Plot.barX(data.by_category, { x: "count", y: "category", fill: "#c47a3a", sort: { y: "-x" } }),
        Plot.ruleX([0], { stroke: "var(--border)" })
      ]
    })}
  </div>
  <div class="chart-wrap">
    <div class="obs-label" style="margin-bottom:0.75rem">${t("rank")} / ${t("mentions")}</div>
    ${html`<div>${data.top_buyers.slice(0,12).map((s,i) => html`<div class="rank-row">
      <span class="rank-n">${i+1}</span>
      <span class="rank-name">${s.name}</span>
      <div class="rank-bar-cell">
        <div class="rank-bar" style="background:#c47a3a; width:${Math.round(s.count/maxCount*100)}px"></div>
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
