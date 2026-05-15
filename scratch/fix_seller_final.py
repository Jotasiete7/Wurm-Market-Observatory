import sys

content = r'''---
title: Seller Activity Lens
toc: false
---

```js
import * as Plot from "npm:@observablehq/plot";
import { html } from "npm:htl";
import { CorpusHealthCard } from "../components/corpus-health.js";

const meta = await FileAttachment("../data/corpus-meta.json").json();
const data = await FileAttachment("../data/seller-activity.json").json();
const corpus = meta.active;

const observed = data.daily_activity.filter(function(row) { return !row.gap; });
const gaps = data.daily_activity.filter(function(row) { return row.gap; });
const maxCount = data.top_sellers[0] ? data.top_sellers[0].count : 1;
```

<div class="obs-page">

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

  <div class="method-note" style="margin-bottom:1.5rem">
    <strong>Methodological note —</strong>
    This lens counts seller mentions in the trade channel.
    <strong>Coverage: ${Math.round(data.coverage * 100)}%.</strong>
  </div>

  <div class="obs-card obs-card-sm" style="display:flex;align-items:center;gap:1.5rem;margin-bottom:1.5rem">
    <div style="font-size:2rem;color:var(--amber);min-width:56px;font-family:var(--font-mono);font-weight:300">
      ${Math.round(data.coverage * 100)}%
    </div>
    <div style="flex:1">
      <div class="corpus-stat-label" style="margin-bottom:4px">Corpus coverage — ${corpus.period}</div>
      <div class="cov-bar-track">
        <div class="cov-bar-fill" style="width:${Math.round(data.coverage*100)}%"></div>
      </div>
      <div style="font-size:0.65rem;color:var(--ink-4);margin-top:4px">
        ${corpus.gaps.map(function(g) { return html`<span style="color:#c47a3a;margin-right:0.5rem">▲ ${g.label}</span>`; })}
      </div>
    </div>
  </div>

  <div class="obs-grid-4" style="margin-bottom:1.5rem">
    <div class="stat-card">
      <div class="stat-card-label">Unique sellers</div>
      <div class="stat-card-val">${data.summary.unique_sellers}</div>
    </div>
    <div class="stat-card">
      <div class="stat-card-label">Total listings</div>
      <div class="stat-card-val">${data.summary.total_listings.toLocaleString()}</div>
    </div>
    <div class="stat-card">
      <div class="stat-card-label">Top category</div>
      <div class="stat-card-val">${data.summary.top_category}</div>
    </div>
    <div class="stat-card">
      <div class="stat-card-label">Peak day</div>
      <div class="stat-card-val">${data.summary.peak_day}</div>
    </div>
  </div>

  <div class="chart-wrap" style="margin-bottom:1.25rem">
    <div class="chart-header">
      <div class="obs-label" style="margin-bottom:0">Daily seller activity — ${corpus.period}</div>
      <span class="cov-badge warn">⚠ ${Math.round(data.coverage * 100)}% coverage</span>
    </div>

```js
display(Plot.plot({
  width: 740,
  height: 200,
  marginLeft: 40,
  marginRight: 10,
  style: { fontFamily: "var(--font-mono)", fontSize: 10, background: "transparent", color: "var(--ink-3)" },
  x: { label: null, ticks: 10 },
  y: { label: null, grid: true, gridColor: "var(--border)" },
  marks: [
    Plot.barY(gaps, { x: "day", y: 320, fill: "var(--gap)", opacity: 0.6 }),
    Plot.barY(observed, { x: "day", y: "count", fill: "var(--amber)", opacity: 0.72 }),
    Plot.ruleY([0], { stroke: "var(--border-strong)", strokeWidth: 0.5 })
  ]
}));
```

  </div>

  <div class="obs-grid-2" style="margin-bottom:1.25rem;gap:1rem">
    <div class="chart-wrap">
      <div class="obs-label">Listings by category</div>

```js
display(Plot.plot({
  width: 320,
  height: 200,
  marginLeft: 82,
  style: { fontFamily: "var(--font-mono)", fontSize: 10, background: "transparent", color: "var(--ink-3)" },
  marks: [
    Plot.barX(data.by_category, { x: "count", y: "category", fill: "var(--amber)", sort: { y: "-x" } }),
    Plot.ruleX([0], { stroke: "var(--border)" })
  ]
}));
```

    </div>
    <div class="chart-wrap">
      <div class="obs-label" style="margin-bottom:0.75rem">Top sellers by count</div>

```js
display(html`<div>
  ${data.top_sellers.map(function(s, i) { 
    return html`<div class="rank-row">
      <span class="rank-n">${i + 1}</span>
      <span class="rank-name">${s.name}</span>
      <div class="rank-bar-cell">
        <div class="rank-bar" style="width:${Math.round(s.count / (maxCount || 1) * 100)}px"></div>
        <span class="rank-count">${s.count}</span>
      </div>
    </div>`;
  })}
</div>`);
```

    </div>
  </div>

  <div class="obs-section">
    <div class="obs-label">Source corpus</div>
    ${CorpusHealthCard(corpus)}
  </div>

</div>
'''

with open('src/lenses/seller.md', 'w', encoding='utf-8', newline='\r\n') as f:
    f.write(content)
