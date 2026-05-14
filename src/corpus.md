---
title: Corpus Explorer
toc: false
---

```js
const meta = await FileAttachment("data/corpus-meta.json").json();
```

<div class="obs-page">

  <div class="obs-hero" style="padding-bottom:1.5rem">
    <div class="obs-hero-eyebrow">Corpus Explorer</div>
    <h1 class="obs-hero-title" style="font-size:1.8rem">The raw material</h1>
    <p class="obs-hero-sub">
      Every analysis in this observatory derives from restored corpora downloaded from the
      Historical Archive. This page shows what has been loaded, what is missing, and
      what each corpus contributes.
    </p>
  </div>

  <div class="obs-section">
    <div class="obs-label">Loaded corpora</div>
    ```js
    html`<div style="display:flex;flex-direction:column;gap:8px">
      ${meta.all_corpora.filter(c => c.coverage > 0).map(c => html`
        <div class="obs-card obs-card-sm" style="display:flex;align-items:center;gap:1.5rem">
          <div style="min-width:90px;font-size:0.75rem;color:var(--ink)">${c.month}</div>
          <div style="flex:1">
            <div class="cov-bar-track" style="height:5px">
              <div class="cov-bar-fill" style="width:${Math.round(c.coverage*100)}%"></div>
            </div>
          </div>
          <div style="min-width:36px;text-align:right;font-size:0.75rem;color:var(--amber)">${Math.round(c.coverage*100)}%</div>
          <div style="min-width:36px;text-align:right">
            <span class="lens-status ${c.coverage >= 0.65 ? 'active' : 'partial'}">${c.coverage >= 0.65 ? 'good' : 'partial'}</span>
          </div>
        </div>
      `)}
    </div>`
    ```
  </div>

  <div class="obs-section">
    <div class="obs-label">Missing periods</div>
    ```js
    html`<div style="display:flex;flex-direction:column;gap:8px">
      ${meta.all_corpora.filter(c => c.coverage === 0).map(c => html`
        <div class="obs-card obs-card-sm" style="display:flex;align-items:center;gap:1.5rem;opacity:0.5">
          <div style="min-width:90px;font-size:0.75rem;color:var(--ink-3)">${c.month}</div>
          <div style="flex:1;height:5px;background:repeating-linear-gradient(90deg, var(--gap) 0, var(--gap) 2px, transparent 2px, transparent 6px);border-radius:2px"></div>
          <span class="lens-status unavail">no data</span>
        </div>
      `)}
    </div>`
    ```
  </div>

  <div class="obs-section">
    <div class="method-note">
      <strong>What is a restored corpus?</strong><br>
      Corpora are trade channel logs extracted from the Wurm Online Historical Archive.
      "Restored" means the raw log has been cleaned of encoding artifacts and duplicate lines.
      Coverage percentage reflects how many days of the period have at least one valid log entry.
      A day with zero entries is counted as a gap regardless of cause — server downtime,
      missing upload, or parsing failure.
    </div>
  </div>

</div>
