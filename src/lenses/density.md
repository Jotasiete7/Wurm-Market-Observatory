---
title: Trade Density Lens
toc: false
---

```js
import * as Plot from "npm:@observablehq/plot";
import { CorpusHealthCard } from "../components/corpus-health.js";

const meta   = await FileAttachment("../data/corpus-meta.json").json();
const data   = await FileAttachment("../data/trade-density.json").json();
const corpus = meta.active;

const days = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];
```

<div class="obs-page">

  <!-- HEADER -->
  <div style="padding: 2rem 0 1.5rem; border-bottom: 0.5px solid var(--border); margin-bottom: 2rem;">
    <div style="margin-bottom: 0.5rem">
      <a href="/" style="font-size:0.7rem;color:var(--amber);text-decoration:none;letter-spacing:0.5px">← Observatory</a>
      <span style="font-size:0.7rem;color:var(--ink-4);margin:0 0.5rem">/</span>
      <span style="font-size:0.7rem;color:var(--ink-4);letter-spacing:0.5px">Lens</span>
    </div>
    <h1 style="font-family:var(--font-title);font-size:2rem;font-weight:400;margin-bottom:0.5rem">Trade Density</h1>
    <p style="font-size:0.75rem;color:var(--ink-3);max-width:480px;line-height:1.7">
      Temporal activity maps showing when the market is most active across the week.
    </p>
  </div>

  <!-- METHODOLOGY NOTE -->
  <div class="method-note" style="margin-bottom:1.5rem">
    <strong>Methodological note —</strong>
    Density is calculated by counting all unique mentions (Buy/Sell/Trade) per hour block.
    All times are normalized to UTC. 
    Note that "quiet" periods in the heatmap may be due to regional data gaps or server maintenance,
    not necessarily a lack of player activity.
    <strong>Coverage: ${Math.round(data.coverage * 100)}%.</strong>
  </div>

  <!-- HEATMAP CHART -->
  <div class="chart-wrap" style="margin-bottom:1.25rem">
    <div class="chart-header">
      <div class="obs-label" style="margin-bottom:0">Activity Heatmap (Day vs Hour UTC)</div>
      <span class="cov-badge">active corpus</span>
    </div>

    ```js
    Plot.plot({
      width: 740,
      height: 280,
      padding: 0.05,
      style: { fontFamily: "JetBrains Mono, monospace", fontSize: 10, background: "transparent", color: "#7a7568" },
      x: { label: "Hour of Day (UTC)", tickFormat: d => `${d}h`, domain: d3.range(24) },
      y: { label: null, tickFormat: d => days[d], domain: d3.range(7) },
      color: { scheme: "YlOrBr", label: "Mentions", legend: true },
      marks: [
        Plot.cell(data.heatmap, {
          x: "hour",
          y: "day",
          fill: "count",
          inset: 0.5,
          rx: 1,
          title: d => `${days[d.day]} ${d.hour}h: ${d.count} mentions`
        })
      ]
    })
    ```
  </div>

  <div class="obs-grid-2">
    <div class="obs-card">
      <div class="obs-label">Weekly Peak</div>
      <p style="font-size:1.1rem;color:var(--ink)">Friday through Saturday evenings</p>
      <p style="font-size:0.7rem;color:var(--ink-3);margin-top:0.5rem">
        Activity starts climbing at 16:00 UTC on Fridays, peaking around 21:00 UTC on Saturdays.
      </p>
    </div>
    <div class="obs-card">
      <div class="obs-label">The "Dead Zone"</div>
      <p style="font-size:1.1rem;color:var(--ink)">06:00 – 10:00 UTC daily</p>
      <p style="font-size:0.7rem;color:var(--ink-3);margin-top:0.5rem">
        Consistently low activity period across all observed corpora, aligning with early morning in Europe and late night in the Americas.
      </p>
    </div>
  </div>

  <!-- SOURCE -->
  <div class="obs-section">
    <div class="obs-label">Source corpus</div>
    ${CorpusHealthCard(corpus)}
  </div>

</div>
