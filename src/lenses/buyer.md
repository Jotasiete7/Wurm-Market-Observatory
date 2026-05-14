---
title: Buyer Activity Lens
toc: false
---

```js
import * as Plot from "npm:@observablehq/plot";
import { CorpusHealthCard } from "../components/corpus-health.js";

const meta   = await FileAttachment("../data/corpus-meta.json").json();
const data   = await FileAttachment("../data/buyer-activity.json").json();
const corpus = meta.active;
```

<div class="obs-page">

  <!-- HEADER -->
  <div style="padding: 2rem 0 1.5rem; border-bottom: 0.5px solid var(--border); margin-bottom: 2rem;">
    <div style="margin-bottom: 0.5rem">
      <a href="/" style="font-size:0.7rem;color:var(--amber);text-decoration:none;letter-spacing:0.5px">← Observatory</a>
      <span style="font-size:0.7rem;color:var(--ink-4);margin:0 0.5rem">/</span>
      <span style="font-size:0.7rem;color:var(--ink-4);letter-spacing:0.5px">Lens</span>
    </div>
    <h1 style="font-family:var(--font-title);font-size:2rem;font-weight:400;margin-bottom:0.5rem">Buyer Activity</h1>
    <p style="font-size:0.75rem;color:var(--ink-3);max-width:480px;line-height:1.7">
      Demand signals, WTB (Want To Buy) patterns, and item search frequency.
    </p>
  </div>

  <!-- METHODOLOGY NOTE -->
  <div class="method-note" style="margin-bottom:1.5rem">
    <strong>Methodological note —</strong>
    This lens identifies buyers by parsing "WTB" and "Buying" signals. 
    It captures the <em>intent</em> to purchase, which is often more sporadic than selling activity.
    Note that many buyers prefer private messages (PMs) which are not captured in the public trade channel corpus.
    <strong>Coverage: ${Math.round(data.coverage * 100)}%.</strong>
  </div>

  <!-- STATS ROW -->
  <div class="obs-grid-4" style="margin-bottom:1.5rem">
    <div class="stat-card">
      <div class="stat-card-label">Unique buyers</div>
      <div class="stat-card-val">${data.summary.unique_buyers}</div>
      <div class="stat-card-sub">in covered periods</div>
    </div>
    <div class="stat-card">
      <div class="stat-card-label">WTB signals</div>
      <div class="stat-card-val">${data.summary.total_wtb_signals.toLocaleString()}</div>
      <div class="stat-card-sub">distinct search mentions</div>
    </div>
    <div class="stat-card">
      <div class="stat-card-label">Top category</div>
      <div class="stat-card-val" style="font-size:1.1rem;margin-top:4px">${data.summary.top_category}</div>
      <div class="stat-card-sub">${Math.round(data.summary.top_category_pct * 100)}% of demand</div>
    </div>
    <div class="stat-card">
      <div class="stat-card-label">Peak activity</div>
      <div class="stat-card-val" style="font-size:1.1rem;margin-top:4px">${data.summary.peak_day}</div>
      <div class="stat-card-sub">${data.summary.peak_day_multiplier}× baseline</div>
    </div>
  </div>

  <!-- ACTIVITY CHART -->
  <div class="chart-wrap" style="margin-bottom:1.25rem">
    <div class="chart-header">
      <div class="obs-label" style="margin-bottom:0">Daily buyer activity — ${corpus.period}</div>
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
      style: { fontFamily: "JetBrains Mono, monospace", fontSize: 10, background: "transparent", color: "#7a7568" },
      x: { label: null, tickFormat: d => `${d}`, ticks: 10 },
      y: { label: null, grid: true, gridColor: "#e4dfd4" },
      marks: [
        Plot.barY(gaps, {
          x: "day",
          y: 60,
          fill: "repeating-linear-gradient(90deg, #c4bfb2 0, #c4bfb2 2px, transparent 2px, transparent 6px)",
          opacity: 0.5,
          title: d => "No data — gap period"
        }),
        Plot.barY(observed, {
          x: "day",
          y: "count",
          fill: "#b07d2a",
          opacity: 0.75,
          rx: 1,
          title: d => `Day ${d.day}: ${d.count} WTB signals observed`
        }),
        Plot.ruleY([0], { stroke: "#ccc8bc", strokeWidth: 0.5 })
      ]
    })
    ```
  </div>

  <div class="obs-grid-2" style="margin-bottom:1.25rem;gap:1rem">
    <div class="chart-wrap">
      <div class="obs-label">Demand by category</div>
      ```js
      Plot.plot({
        width: 320,
        height: 180,
        marginLeft: 80,
        marginRight: 20,
        style: { fontFamily: "JetBrains Mono, monospace", fontSize: 10, background: "transparent", color: "#7a7568" },
        x: { label: null },
        y: { label: null },
        marks: [
          Plot.barX(data.by_category, {
            x: "count",
            y: "category",
            fill: "#b07d2a",
            opacity: d => 0.4 + d.pct * 1.4,
            rx: 1,
            sort: { y: "-x" },
            title: d => `${d.category}: ${d.count} (${Math.round(d.pct*100)}%)`
          }),
          Plot.ruleX([0], { stroke: "#ccc8bc", strokeWidth: 0.5 })
        ]
      })
      ```
    </div>

    <div class="chart-wrap">
      <div class="chart-header" style="margin-bottom:0.75rem">
        <div class="obs-label" style="margin-bottom:0">Top buyers by mention count</div>
      </div>
      <div>
        ```js
        const maxCount = data.top_buyers[0].count;
        html`<div>
          ${data.top_buyers.map((s, i) => html`
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
        </div>`
        ```
      </div>
    </div>
  </div>

  <!-- SOURCE -->
  <div class="obs-section">
    <div class="obs-label">Source corpus</div>
    ${CorpusHealthCard(corpus)}
  </div>

</div>
