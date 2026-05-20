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

// BLOCO 1: Carregamento de partições de dados
const dataPartitions = {
  NFI: {
    "2025": {
      meta: FileAttachment("data/nfi-corpus-meta-2025.json"),
      seller: FileAttachment("data/nfi-seller-activity-2025.json"),
      buyer: FileAttachment("data/nfi-buyer-activity-2025.json")
    },
    "2026-ytd": {
      meta: FileAttachment("data/nfi-corpus-meta-2026-ytd.json"),
      seller: FileAttachment("data/nfi-seller-activity-2026-ytd.json"),
      buyer: FileAttachment("data/nfi-buyer-activity-2026-ytd.json")
    }
  },
  SFI: {
    "2025": {
      meta: FileAttachment("data/sfi-corpus-meta-2025.json"),
      seller: FileAttachment("data/sfi-seller-activity-2025.json"),
      buyer: FileAttachment("data/sfi-buyer-activity-2025.json")
    },
    "2026-ytd": {
      meta: FileAttachment("data/sfi-corpus-meta-2026-ytd.json"),
      seller: FileAttachment("data/sfi-seller-activity-2026-ytd.json"),
      buyer: FileAttachment("data/sfi-buyer-activity-2026-ytd.json")
    }
  }
};
```

```js
// BLOCO 2: Seletor nativo reativo de servidor e período
const serverView = Inputs.select(["NFI", "SFI"], {value: "NFI"});
const serverVal  = Generators.input(serverView);

const periodView = Inputs.select([
  {label: "2025 (Jan–Dec)", value: "2025"},
  {label: "2026 (YTD)", value: "2026-ytd"}
], {value: "2025"});
const periodVal = Generators.input(periodView);
```

```js
// BLOCO 3: Seleção reativa de dados baseada nas escolhas
const activeServer = serverVal === "SFI" ? "SFI" : "NFI";
const activePeriod = periodVal === "2026-ytd" ? "2026-ytd" : "2025";
const activePartition = dataPartitions[activeServer][activePeriod];
const meta = await activePartition.meta.json();
const corpus = meta.active;
const seller = await activePartition.seller.json();
const buyer = await activePartition.buyer.json();
const langVal = lang.value || "pt";
```

```js
display(html`<div class="obs-page">

<div class="obs-hero">
  <div style="display:flex; justify-content:space-between; align-items:flex-start;">
    <div class="obs-hero-eyebrow">Wurm Market Observatory</div>
    <div style="display:flex; gap:8px; align-items:center;">
      ${serverView}
      ${periodView}
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
      <div class="obs-label">${langVal === "pt" ? "Crônicas do Observatório" : "Observatory Chronicles"}</div>
      <div class="obs-card" style="padding:1.25rem;">
        <div class="obs-items">
          <div class="obs-chronicle-item" style="padding-top:0">
            <span class="obs-chronicle-tag">${langVal === "pt" ? "Anomalia de Mercado" : "Market Anomaly"}</span>
            <div class="obs-chronicle-body">
              ${t("obs_surge", { cat: seller.summary.top_category, pct: Math.round(seller.summary.top_category_pct * 100) })}
            </div>
            <span class="obs-chronicle-meta">${langVal === "pt" ? "atividade_vendedor" : "seller_activity"} · ${corpus.period}</span>
          </div>
          <div class="obs-chronicle-item" style="padding-bottom:0; border-bottom:none">
            <span class="obs-chronicle-tag">${langVal === "pt" ? "Densidade de Trade" : "Trade Density"}</span>
            <div class="obs-chronicle-body">
              ${t("obs_weekend")}
            </div>
            <span class="obs-chronicle-meta">${langVal === "pt" ? "multi-corpus" : "multi-corpus"}</span>
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

```
