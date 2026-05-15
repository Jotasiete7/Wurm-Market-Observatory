---
title: Observatory
toc: false
---

```js
import { html } from "npm:htl";
import { CorpusHealthCard } from "./components/corpus-health.js";
import { CoverageTimeline }  from "./components/coverage-timeline.js";
import { LensCard }          from "./components/lens-card.js";
import { t, LanguageSelector, ServerSelector, lang, server } from "./components/i18n.js";

const nfi_meta   = await FileAttachment("data/nfi-corpus-meta.json").json();
const sfi_meta   = await FileAttachment("data/sfi-corpus-meta.json").json();
const nfi_seller = await FileAttachment("data/nfi-seller-activity.json").json();
const sfi_seller = await FileAttachment("data/sfi-seller-activity.json").json();
const nfi_buyer  = await FileAttachment("data/nfi-buyer-activity.json").json();
const sfi_buyer  = await FileAttachment("data/sfi-buyer-activity.json").json();

const meta   = server.value === "NFI" ? nfi_meta : sfi_meta;
const corpus = meta.active;
const seller = server.value === "NFI" ? nfi_seller : sfi_seller;
const buyer  = server.value === "NFI" ? nfi_buyer  : sfi_buyer;
```

```js
display(html`<div class="obs-page">

<div class="obs-hero">
  <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:1.5rem">
    <div style="font-size:0.65rem; color:var(--ink-4); letter-spacing:2px; text-transform:uppercase">Wurm Market Observatory</div>
    <div style="display:flex; gap:8px; align-items:center;">
      ${ServerSelector()}
      ${LanguageSelector()}
    </div>
  </div>
  <h1 class="obs-hero-title">${t("hero_title")}</h1>
  <p class="obs-hero-sub">${t("hero_sub")}</p>
  <div style="margin-top:1.5rem; font-size:0.65rem; color:var(--ink-4); letter-spacing:1px">${t("hero_badge")}</div>
</div>

<div class="obs-section" style="margin-top:3rem">
  <div class="obs-label">${t("source_corpus")}</div>
  ${CorpusHealthCard(corpus)}
</div>

<div class="obs-section" style="margin-top:3rem">
  <div class="obs-label">${t("recent_obs")}</div>
  <div style="display:flex; flex-direction:column; gap:1.5rem; margin-top:1rem">
    <div style="display:flex; gap:1rem">
      <div style="width:6px; height:6px; border-radius:50%; background:var(--amber); margin-top:6px; flex-shrink:0"></div>
      <div>
        <div class="obs-text">${t("obs_surge", { cat: seller.summary.top_category, pct: Math.round(seller.summary.top_category_pct * 100) })}</div>
        <div class="obs-meta" style="margin-top:4px">${lang.value === 'pt' ? 'atividade_vendedor' : 'seller_activity'} · ${corpus.period} · ${Math.round(seller.coverage * 100)}% cov</div>
      </div>
    </div>
    <div style="display:flex; gap:1rem">
      <div style="width:6px; height:6px; border-radius:50%; background:var(--amber); margin-top:6px; flex-shrink:0"></div>
      <div>
        <div class="obs-text">${t("obs_weekend")}</div>
        <div class="obs-meta" style="margin-top:4px">${lang.value === 'pt' ? 'densidade_trade' : 'trade_density'} · multi-corpus · partial</div>
      </div>
    </div>
  </div>
</div>

<div class="obs-section" style="margin-top:3rem">
  <div class="obs-label">${t("available_lenses")}</div>
  <div style="display:grid; grid-template-columns:1fr 1fr; gap:1.5rem; margin-top:1rem">
    ${LensCard({ href: "/lenses/seller", name: t("seller_title"), insight: seller.summary.unique_sellers + " " + t("unique_sellers"), coverage: corpus.coverage, period: corpus.period, status: "active", version: "v0.1" })}
    ${LensCard({ href: "/lenses/buyer",  name: t("buyer_title"),  insight: buyer.summary.unique_buyers  + " " + t("unique_buyers"),  coverage: corpus.coverage, period: corpus.period, status: "active", version: "v0.1" })}
  </div>
</div>

</div>`);
```
