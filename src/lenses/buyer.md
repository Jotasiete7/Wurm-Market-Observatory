---
title: Buyer Activity Lens
toc: false
---

```js
import * as Plot from "npm:@observablehq/plot";
import { html } from "npm:htl";
import { CorpusHealthCard } from "../components/corpus-health.js";
import { t, LanguageSelector, ServerSelector, lang, server } from "../components/i18n.js";

// Carregamento estático
const nfi_meta = await FileAttachment("../data/nfi-corpus-meta.json").json();
const sfi_meta = await FileAttachment("../data/sfi-corpus-meta.json").json();
const nfi_data = await FileAttachment("../data/nfi-buyer-activity.json").json();
const sfi_data = await FileAttachment("../data/sfi-buyer-activity.json").json();

// Seleção
const meta = server.value === "NFI" ? nfi_meta : sfi_meta;
const data = server.value === "NFI" ? nfi_data : sfi_data;
const corpus = meta.active;

const maxCount = data.top_buyers[0] ? data.top_buyers[0].count : 1;
```

<div class="obs-page">

<div style="padding: 2rem 0 1.5rem; border-bottom: 0.5px solid var(--border); margin-bottom: 2rem;">
<div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.5rem">
<div>
<a href="/" style="font-size:0.7rem;color:var(--amber);text-decoration:none;letter-spacing:0.5px">${t("back")}</a>
<span style="font-size:0.7rem;color:var(--ink-4);margin:0 0.5rem">/</span>
<span style="font-size:0.7rem;color:var(--ink-4);letter-spacing:0.5px">${t("lens_v")}</span>
</div>
<div style="display:flex; gap:8px; align-items:center;">
  ${ServerSelector()}
  ${LanguageSelector()}
</div>
</div>
```js
display(html`<h1 style="font-family:var(--font-title);font-size:2rem;font-weight:400;margin-bottom:0.5rem">${t("buyer_title")}</h1>`)
```
<p style="font-size:0.75rem;color:var(--ink-3);max-width:480px;line-height:1.7">
${lang.value === "pt" 
  ? `Análise da demanda e sinais de compra (WTB) detectados no canal de trade de ${server.value}.`
  : `Analysis of demand and buy signals (WTB) detected in the ${server.value} trade channel.`}
</p>
</div>

<div class="method-note" style="margin-bottom:1.5rem">
<strong>${t("methodology_note")}</strong>
<strong>${t("coverage")}: ${Math.round(data.coverage * 100)}%.</strong>
</div>

<div class="obs-card obs-card-sm" style="display:flex;align-items:center;gap:1.5rem;margin-bottom:1.5rem">
<div style="font-size:2rem;color:var(--amber);min-width:56px;font-family:var(--font-mono);font-weight:300">
${Math.round(data.coverage * 100)}%
</div>
<div style="flex:1">
<div class="corpus-stat-label" style="margin-bottom:4px">${t("coverage")} — ${corpus.period} (${server.value})</div>
<div class="cov-bar-track">
<div class="cov-bar-fill" style="width:${Math.round(data.coverage*100)}%"></div>
</div>
</div>
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
<div class="stat-card-val" style="font-size:0.8rem;text-transform:uppercase;color:var(--success)">${data.confidence}</div>
</div>
</div>

<div class="obs-grid-2" style="margin-bottom:1.25rem;gap:1rem">
<div class="chart-wrap">
<div class="obs-label">${lang.value === "pt" ? "Demanda por Categoria" : "Demand by Category"}</div>

```js
display(Plot.plot({
  width: 320,
  height: 200,
  marginLeft: 82,
  style: { fontFamily: "var(--font-mono)", fontSize: 10, background: "transparent", color: "var(--ink-3)" },
  marks: [
    Plot.barX(data.by_category, { x: "count", y: "category", fill: "#c47a3a", sort: { y: "-x" } }),
    Plot.ruleX([0], { stroke: "var(--border)" })
  ]
}));
```

</div>
<div class="chart-wrap">
<div class="obs-label" style="margin-bottom:0.75rem">${t("rank")} / ${t("mentions")}</div>

```js
display(html`<div>
  ${data.top_buyers.map(function(s, i) { 
    return html`<div class="rank-row">
      <span class="rank-n">${i + 1}</span>
      <span class="rank-name">${s.name}</span>
      <div class="rank-bar-cell">
        <div class="rank-bar" style="background:#c47a3a; width:${Math.round(s.count / (maxCount || 1) * 100)}px"></div>
        <span class="rank-count">${s.count}</span>
      </div>
    </div>`;
  })}
</div>`);
```

</div>
</div>

<div class="obs-section" style="margin-bottom:1.5rem">
<div class="obs-label">${t("items_title")}</div>

```js
const allItems = data.top_buyers.flatMap(function(s) { return s.parsed_items || []; });
const grouped = {};
for (const item of allItems) {
  if (!grouped[item.name]) grouped[item.name] = { count: 0, totalQty: 0 };
  grouped[item.name].count += 1;
  grouped[item.name].totalQty += item.qty;
}
const itemsSummary = Object.entries(grouped)
  .map(function([name, stats]) { return { name: name, count: stats.count, totalQty: stats.totalQty }; })
  .sort(function(a, b) { return b.count - a.count; })
  .slice(0, 10);

display(html`
<div style="background:var(--bg-card); border:1px solid var(--border); padding:1rem; border-radius:4px;">
  <div style="display:flex; border-bottom:1px solid var(--border); padding-bottom:8px; margin-bottom:8px; font-family:var(--font-mono); font-size:0.75rem; color:var(--ink-4);">
    <div style="flex:2">${t("item_name")}</div>
    <div style="flex:1;text-align:right">${t("mentions")}</div>
    <div style="flex:1;text-align:right">${t("total_qty")}</div>
  </div>
  ${itemsSummary.map(function(d) { return html`
    <div style="display:flex; padding:4px 0; font-family:var(--font-mono); font-size:0.8rem; color:var(--ink-2); border-bottom:1px dotted var(--border-light);">
      <div style="flex:2; color:#c47a3a;">${d.name}</div>
      <div style="flex:1;text-align:right">${d.count}</div>
      <div style="flex:1;text-align:right">${d.totalQty}</div>
    </div>`;
  })}
</div>
`);
```

</div>

<div class="obs-section">
<div class="obs-label">${t("source_corpus")}</div>
${CorpusHealthCard(corpus)}
</div>

</div>
