---
title: Seller Activity Lens
toc: false
---

```js
import * as Plot from "npm:@observablehq/plot";
import { html } from "npm:htl";
import { CorpusHealthCard } from "../components/corpus-health.js";

const meta   = await FileAttachment("../data/corpus-meta.json").json();
const data   = await FileAttachment("../data/seller-activity.json").json();
const corpus = meta.active;
```

<div class="obs-page">

  <!-- HEADER -->
  <div style="padding: 2rem 0 1.5rem; border-bottom: 0.5px solid var(--border); margin-bottom: 2rem;">
    <div style="margin-bottom: 0.5rem">
      <a href="/" style="font-size:0.7rem;color:var(--amber);text-decoration:none;letter-spacing:0.5px">← Observatory</a>
      <span style="font-size:0.7rem;color:var(--ink-4);margin:0 0.5rem">/</span>
      <span style="font-size:0.7rem;color:var(--ink-4);letter-spacing:0.5px">Lens · v0.1</span>
    </div>
    <h1 style="font-family:var(--font-title);font-size:2rem;font-weight:400;margin-bottom:0.5rem">Seller Activity</h1>
    <p style="font-size:0.75rem;color:var(--ink-3);max-width:480px;line-height:1.7">
      Who sells, what they sell, and when they appear in the trade channel corpus.
    </p>
  </div>

  <!-- METHODOLOGY NOTE -->
  <div class="method-note" style="margin-bottom:1.5rem">
    <strong>Methodological note —</strong>
    This lens counts seller <em>mentions</em> in the trade channel corpus, not confirmed transactions.
    A seller appearing 50 times may have listed one item repeatedly or completed many trades —
    the corpus does not distinguish. Price data reflects asked prices, not agreed prices.
    Periods marked with diagonal hatching contain no data and are <em>not interpolated</em>.
    <strong>Coverage: ${Math.round(data.coverage * 100)}%.</strong>
  </div>

  <!-- COVERAGE BLOCK -->
  <div class="obs-card obs-card-sm" style="display:flex;align-items:center;gap:1.5rem;margin-bottom:1.5rem">
    <div style="font-size:2rem;color:var(--amber);min-width:56px;font-family:var(--font-mono);font-weight:300">
      ${Math.round(data.coverage * 100)}%
    </div>
    <div style="flex:1">
      <div class="corpus-stat-label" style="margin-bottom:4px">Corpus coverage — ${corpus.period}</div>
      <div class="cov-bar-track">
        <div class="cov-bar-fill" style="width:${Math.round(data.coverage*100)}%"></div>
        <div class="cov-bar-gap" style="left:18%;width:11%;top:0;bottom:0;height:7px"></div>
        <div class="cov-bar-gap" style="left:43%;width:9%;top:0;bottom:0;height:7px"></div>
        <div class="cov-bar-gap" style="left:71%;width:29%;top:0;bottom:0;height:7px"></div>
      </div>
```js
html`<div style="font-size:0.65rem;color:var(--ink-4);margin-top:4px">
  Known gaps:
  ${corpus.gaps.map(g => html`<span style="color:#c47a3a;margin-right:0.5rem">▲ ${g.label}</span>`)}
</div>`
```
    </div>
  </div>

  <!-- STATS ROW -->
  <div class="obs-grid-4" style="margin-bottom:1.5rem">
    <div class="stat-card">
      <div class="stat-card-label">Unique sellers</div>
      <div class="stat-card-val">${data.summary.unique_sellers}</div>
      <div class="stat-card-sub">in covered periods</div>
    </div>
    <div class="stat-card">
      <div class="stat-card-label">Total listings</div>
      <div class="stat-card-val">${data.summary.total_listings.toLocaleString()}</div>
      <div class="stat-card-sub">mentions counted</div>
    </div>
    <div class="stat-card">
      <div class="stat-card-label">Top category</div>
      <div class="stat-card-val" style="font-size:1.1rem;margin-top:4px">${data.summary.top_category}</div>
      <div class="stat-card-sub">${Math.round(data.summary.top_category_pct * 100)}% of listings</div>
    </div>
    <div class="stat-card">
      <div class="stat-card-label">Peak day</div>
      <div class="stat-card-val" style="font-size:1.1rem;margin-top:4px">${data.summary.peak_day}</div>
      <div class="stat-card-sub">avg ${data.summary.peak_day_multiplier}× weekday vol</div>
    </div>
  </div>

  <!-- ACTIVITY CHART -->
  <div class="chart-wrap" style="margin-bottom:1.25rem">
    <div class="chart-header">
      <div class="obs-label" style="margin-bottom:0">Daily seller activity — ${corpus.period}</div>
      <span class="cov-badge warn">⚠ ${Math.round(data.coverage * 100)}% coverage</span>
    </div>

```js
const observed = data.daily_activity.filter(d => !d.gap);
const gaps     = data.daily_activity.filter(d => d.gap);

Plot.plot({
  width: 740,
  height: 200,
  marginLeft: 40,
  marginRight: 10,
  style: {
    fontFamily: "var(--font-mono)",
    fontSize: 10,
    background: "transparent",
    color: "var(--ink-3)"
  },
  x: { label: null, ticks: 10 },
  y: { label: null, grid: true, gridColor: "var(--border)" },
  marks: [
    Plot.barY(gaps, {
      x: "day",
      y: 320,
      fill: "var(--gap)",
      opacity: 0.6,
      rx: 1,
      title: () => "No data — gap period (not interpolated)"
    }),
    Plot.barY(observed, {
      x: "day",
      y: "count",
      fill: "var(--amber)",
      opacity: 0.72,
      rx: 1,
      title: d => `Day ${d.day}: ${d.count} listings observed`
    }),
    Plot.ruleY([0], { stroke: "var(--border-strong)", strokeWidth: 0.5 })
  ]
})
```

    <div class="cov-legend" style="margin-top:0.5rem">
      <div class="cov-legend-item"><div class="cov-swatch covered"></div><span>observed activity</span></div>
      <div class="cov-legend-item"><div class="cov-swatch gap"></div><span>no data (gap — not interpolated)</span></div>
    </div>

    <!-- FIELD ANNOTATIONS -->
    <div class="field-notes">
      <div class="fn-item">
        <span class="fn-tick">Nov 6–8</span>
        <span class="fn-text">Trade visibility drops sharply. <strong>Archival absence or genuine market lull</strong> — indeterminate from corpus alone.</span>
      </div>
      <div class="fn-item">
        <span class="fn-tick">Nov 20–21</span>
        <span class="fn-text">Observed surge in listings. <strong>Weekend effect confirmed.</strong> Weapon category disproportionately represented.</span>
      </div>
      <div class="fn-item">
        <span class="fn-tick">Nov 24–30</span>
        <span class="fn-text">Final week absent from corpus. <strong>Possible upload gap in archive.</strong> Late-month patterns unverifiable.</span>
      </div>
    </div>
  </div>

  <!-- CATEGORY + RANKING -->
  <div class="obs-grid-2" style="margin-bottom:1.25rem;gap:1rem">

    <div class="chart-wrap">
      <div class="obs-label">Listings by category</div>
```js
Plot.plot({
  width: 320,
  height: 200,
  marginLeft: 82,
  marginRight: 20,
  style: {
    fontFamily: "var(--font-mono)",
    fontSize: 10,
    background: "transparent",
    color: "var(--ink-3)"
  },
  x: { label: null },
  y: { label: null },
  marks: [
    Plot.barX(data.by_category, {
      x: "count",
      y: "category",
      fill: "var(--amber)",
      opacity: d => 0.35 + d.pct * 1.3,
      rx: 1,
      sort: { y: "-x" },
      title: d => `${d.category}: ${d.count} (${Math.round(d.pct*100)}%)`
    }),
    Plot.ruleX([0], { stroke: "var(--border)", strokeWidth: 0.5 })
  ]
})
```
    </div>

    <div class="chart-wrap">
      <div class="obs-label" style="margin-bottom:0.75rem">Top sellers by listing count</div>
```js
const maxCount = data.top_sellers[0].count;
html`<div>
  ${data.top_sellers.map((s, i) => html`
    <div class="rank-row">
      <span class="rank-n">${i + 1}</span>
      <span class="rank-name">${s.name}</span>
      <div class="rank-bar-cell">
        <div class="rank-bar" style="width:${Math.round(s.count / maxCount * 100)}px"></div>
        <span class="rank-count">${s.count}</span>
      </div>
      <span class="rank-cov">${Math.round(s.coverage * 100)}%</span>
    </div>
  `)}
  <p class="print-hint" style="margin-top:8px">
    % is per-seller corpus coverage. Low-coverage sellers may be undercounted.
  </p>
</div>`
```
    </div>

  </div>

  <!-- EXTRACTED ITEMS SHOWCASE (from TortaApp logic) -->
  <div class="obs-section" style="margin-bottom:1.5rem">
    <div class="obs-label">Top Extracted Items (Parsed via Semantic Engine)</div>
    <div class="method-note" style="margin-bottom:1rem">
      <strong>Deep extraction active —</strong>
      The pipeline now extracts specific item IDs, quantities, and copper values from raw strings.
    </div>


  </div>



  </div>

  <!-- EXTRACTED ITEMS SHOWCASE (from TortaApp logic) -->
  <div class="obs-section" style="margin-bottom:1.5rem">
    <div class="obs-label">Top Extracted Items (Parsed via Semantic Engine)</div>
    <div class="method-note" style="margin-bottom:1rem">
      <strong>Deep extraction active —</strong>
      The pipeline now extracts specific item IDs, quantities, and copper values from raw strings.
    </div>

```js
const allItems = data.top_sellers.flatMap(s => s.parsed_items || []);

// Group by name
const grouped = {};
for (const item of allItems) {
  if (!grouped[item.name]) {
    grouped[item.name] = { count: 0, totalQty: 0, sumPrice: 0, priceCount: 0 };
  }
  grouped[item.name].count += 1;
  grouped[item.name].totalQty += item.qty;
  if (item.price > 0) {
    grouped[item.name].sumPrice += item.price;
    grouped[item.name].priceCount += 1;
  }
}

const itemsSummary = Object.entries(grouped)
  .map(([name, stats]) => ({
    name,
    count: stats.count,
    totalQty: stats.totalQty,
    avgPrice: stats.priceCount > 0 ? stats.sumPrice / stats.priceCount : 0
  }))
  .sort((a, b) => b.count - a.count)
  .slice(0, 10);

display(html`
<div style="background:var(--bg-card); border:1px solid var(--border); padding:1rem; border-radius:4px;">
  <div style="display:flex; border-bottom:1px solid var(--border); padding-bottom:8px; margin-bottom:8px; font-family:var(--font-mono); font-size:0.75rem; color:var(--ink-4);">
    <div style="flex:2">Item (Canonical Name)</div>
    <div style="flex:1;text-align:right">Mentions</div>
    <div style="flex:1;text-align:right">Total Qty</div>
    <div style="flex:1;text-align:right">Avg Price (C)</div>
  </div>
  ${itemsSummary.map(d => html`
    <div style="display:flex; padding:4px 0; font-family:var(--font-mono); font-size:0.8rem; color:var(--ink-2); border-bottom:1px dotted var(--border-light);">
      <div style="flex:2; color:var(--amber);">${d.name}</div>
      <div style="flex:1;text-align:right">${d.count}</div>
      <div style="flex:1;text-align:right">${d.totalQty}</div>
      <div style="flex:1;text-align:right; color:var(--ink-3)">${d.avgPrice > 0 ? d.avgPrice.toFixed(0) : '-'}</div>
    </div>
  `)}
</div>
`);
```
  </div>

  <!-- EXTRACTED ITEMS SHOWCASE (from TortaApp logic) -->
  <div class="obs-section" style="margin-bottom:1.5rem">
    <div class="obs-label">Top Extracted Items (Parsed via Semantic Engine)</div>
    <div class="method-note" style="margin-bottom:1rem">
      <strong>Deep extraction active —</strong>
      The pipeline now extracts specific item IDs, quantities, and copper values from raw strings.
    </div>

```js
const allItems = data.top_sellers.flatMap(s => s.parsed_items || []);

// Group by name
const grouped = {};
for (const item of allItems) {
  if (!grouped[item.name]) {
    grouped[item.name] = { count: 0, totalQty: 0, sumPrice: 0, priceCount: 0 };
  }
  grouped[item.name].count += 1;
  grouped[item.name].totalQty += item.qty;
  if (item.price > 0) {
    grouped[item.name].sumPrice += item.price;
    grouped[item.name].priceCount += 1;
  }
}

const itemsSummary = Object.entries(grouped)
  .map(([name, stats]) => ({
    name,
    count: stats.count,
    totalQty: stats.totalQty,
    avgPrice: stats.priceCount > 0 ? stats.sumPrice / stats.priceCount : 0
  }))
  .sort((a, b) => b.count - a.count)
  .slice(0, 10);

display(html`
<div style="background:var(--bg-card); border:1px solid var(--border); padding:1rem; border-radius:4px;">
  <div style="display:flex; border-bottom:1px solid var(--border); padding-bottom:8px; margin-bottom:8px; font-family:var(--font-mono); font-size:0.75rem; color:var(--ink-4);">
    <div style="flex:2">Item (Canonical Name)</div>
    <div style="flex:1;text-align:right">Mentions</div>
    <div style="flex:1;text-align:right">Total Qty</div>
    <div style="flex:1;text-align:right">Avg Price (C)</div>
  </div>
  ${itemsSummary.map(d => html`
    <div style="display:flex; padding:4px 0; font-family:var(--font-mono); font-size:0.8rem; color:var(--ink-2); border-bottom:1px dotted var(--border-light);">
      <div style="flex:2; color:var(--amber);">${d.name}</div>
      <div style="flex:1;text-align:right">${d.count}</div>
      <div style="flex:1;text-align:right">${d.totalQty}</div>
      <div style="flex:1;text-align:right; color:var(--ink-3)">${d.avgPrice > 0 ? d.avgPrice.toFixed(0) : '-'}</div>
    </div>
  `)}
</div>
`);
```
  </div>

  <!-- SOURCE CORPUS -->
  <div class="obs-section">
    <div class="obs-label">Source corpus</div>
    ${CorpusHealthCard(corpus)}
  </div>

  <div style="margin-top:2rem;padding-top:1rem;border-top:0.5px solid var(--border)">
    <p class="print-hint">
      Lens version 0.1.0 · Generated from ${data.corpus} ·
      Regenerated when a new corpus is loaded into the pipeline.
    </p>
  </div>

</div>
