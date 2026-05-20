---
title: Observatory
toc: false
---

```js
import { html } from "npm:htl";
import { CorpusHealthCard } from "./components/corpus-health.js";
import { CoverageTimeline }  from "./components/coverage-timeline.js";
import { LensCard }          from "./components/lens-card.js";
import { t, LanguageSelector, lang } from "./components/i18n.js";

// BLOCO 1: Carregamento estático
const nfi_meta   = await FileAttachment("data/nfi-corpus-meta.json").json();
const sfi_meta   = await FileAttachment("data/sfi-corpus-meta.json").json();
const nfi_seller = await FileAttachment("data/nfi-seller-activity.json").json();
const sfi_seller = await FileAttachment("data/sfi-seller-activity.json").json();
const nfi_buyer  = await FileAttachment("data/nfi-buyer-activity.json").json();
const sfi_buyer  = await FileAttachment("data/sfi-buyer-activity.json").json();
```

```js
// BLOCO 2: Seletor nativo reativo
const serverView = Inputs.select(["NFI", "SFI"], {value: "NFI"});
const serverVal  = Generators.input(serverView);
```

```js
// BLOCO 3: Seleção reativa
const meta   = serverVal === "NFI" ? nfi_meta   : sfi_meta;
const corpus = meta.active;
const seller = serverVal === "NFI" ? nfi_seller : sfi_seller;
const buyer  = serverVal === "NFI" ? nfi_buyer  : sfi_buyer;
const langVal = lang.value || "pt";
```

```js
display(html`<div class="obs-page">

<div class="obs-hero">
  <div style="display:flex; justify-content:space-between; align-items:flex-start;">
    <div class="obs-hero-eyebrow">Wurm Market Observatory</div>
    <div style="display:flex; gap:8px; align-items:center;">
      ${serverView}
      ${LanguageSelector()}
    </div>
  </div>
  <h1 class="obs-hero-title">${t("hero_title")}</h1>
  <p class="obs-hero-sub">${t("hero_sub")}</p>
  <div class="derived-badge">${t("hero_badge")}</div>
</div>

<div class="obs-section">
  <div class="obs-label">${langVal === "pt" ? "Cronologia Reconstruída" : "Reconstructed Chronology"}</div>
  ${CoverageTimeline(meta.all_corpora)}
</div>

<div class="obs-dashboard-layout">
  
  <!-- Coluna Principal (Esquerda - 2/3 da largura útil) -->
  <div style="display:flex; flex-direction:column; gap:2rem;">
    
    <div class="obs-section" style="margin-top:0">
      <div class="obs-label">${t("source_corpus")}</div>
      ${CorpusHealthCard(corpus)}
    </div>
    
    <div class="obs-section" style="margin-top:0">
      <div class="obs-label">${t("available_lenses")}</div>
      <div class="obs-grid-lenses">
        ${LensCard({ href: "/lenses/seller", name: t("seller_title"), insight: seller.summary.unique_sellers + " " + t("unique_sellers"), coverage: corpus.coverage, period: corpus.period, status: "active", version: "v0.1" })}
        ${LensCard({ href: "/lenses/buyer",  name: t("buyer_title"),  insight: buyer.summary.unique_buyers  + " " + t("unique_buyers"),  coverage: corpus.coverage, period: corpus.period, status: "active", version: "v0.1" })}
      </div>
    </div>
    
  </div>
  
  <!-- Coluna Lateral de Status e Logs (Direita - 1/3 da largura útil) -->
  <div style="display:flex; flex-direction:column; gap:2rem;">
    
    <div class="obs-section" style="margin-top:0">
      <div class="obs-label">${t("recent_obs")}</div>
      <div class="obs-card" style="padding:1.25rem;">
        <div class="obs-items">
          <div class="obs-item" style="padding-top:0">
            <div class="obs-dot"></div>
            <div>
              <div class="obs-text">${t("obs_surge", { cat: seller.summary.top_category, pct: Math.round(seller.summary.top_category_pct * 100) })}</div>
              <div class="obs-meta">${langVal === "pt" ? "atividade_vendedor" : "seller_activity"} · ${corpus.period}</div>
            </div>
          </div>
          <div class="obs-item" style="padding-bottom:0; border-bottom:none">
            <div class="obs-dot"></div>
            <div>
              <div class="obs-text">${t("obs_weekend")}</div>
              <div class="obs-meta">${langVal === "pt" ? "densidade_trade" : "trade_density"} · multi-corpus</div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="obs-section" style="margin-top:0">
      <div class="obs-label">${langVal === "pt" ? "Status da Estação" : "Station Status"}</div>
      <div class="obs-stats-sidebar">
        <div class="obs-stats-sidebar-title">OBSERVATORY METRICS</div>
        <div class="obs-stats-sidebar-row">
          <span class="obs-stats-sidebar-label">${langVal === "pt" ? "Servidor Ativo" : "Active Server"}</span>
          <span class="obs-stats-sidebar-value" style="color: var(--amber); font-weight:500;">${serverVal}</span>
        </div>
        <div class="obs-stats-sidebar-row">
          <span class="obs-stats-sidebar-label">${langVal === "pt" ? "Gaps Conhecidos" : "Known Gaps"}</span>
          <span class="obs-stats-sidebar-value" style="color: ${corpus.gaps.length > 0 ? 'var(--amber)' : 'var(--ink-3)'}">${corpus.gaps.length}</span>
        </div>
        <div class="obs-stats-sidebar-row">
          <span class="obs-stats-sidebar-label">${langVal === "pt" ? "Cobertura Temporal" : "Timeframe Covered"}</span>
          <span class="obs-stats-sidebar-value">${corpus.period}</span>
        </div>
        <div class="obs-stats-sidebar-row">
          <span class="obs-stats-sidebar-label">${langVal === "pt" ? "Total de Linhas" : "Total Log Lines"}</span>
          <span class="obs-stats-sidebar-value">${corpus.log_lines.toLocaleString()}</span>
        </div>
      </div>
    </div>
    
  </div>

</div>`);
```
