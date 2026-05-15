import sys

content = r'''---
title: Observatory
toc: false
---

```js
import { html } from "npm:htl";
import { CorpusHealthCard } from "./components/corpus-health.js";
import { CoverageTimeline }  from "./components/coverage-timeline.js";
import { LensCard }          from "./components/lens-card.js";
import { t, LanguageSelector, ServerSelector, lang, server } from "./components/i18n.js";

// Carregamento ESTÁTICO (mais seguro para o framework)
const nfi_meta = await FileAttachment("data/nfi-corpus-meta.json").json();
const sfi_meta = await FileAttachment("data/sfi-corpus-meta.json").json();

const nfi_seller = await FileAttachment("data/nfi-seller-activity.json").json();
const sfi_seller = await FileAttachment("data/sfi-seller-activity.json").json();

const nfi_buyer = await FileAttachment("data/nfi-buyer-activity.json").json();
const sfi_buyer = await FileAttachment("data/sfi-buyer-activity.json").json();

// Seleção reativa
const meta   = server.value === "NFI" ? nfi_meta : sfi_meta;
const corpus = meta.active;
const seller = server.value === "NFI" ? nfi_seller : sfi_seller;
const buyer  = server.value === "NFI" ? nfi_buyer : sfi_buyer;
```

<div class="obs-page">

<div class="obs-hero">
<div style="display:flex; justify-content:space-between; align-items:flex-start;">
<div class="obs-hero-eyebrow">Wurm Market Observatory</div>
<div style="display:flex; gap:8px; align-items:center;">
  ${ServerSelector()}
  ${LanguageSelector()}
</div>
</div>
<h1 class="obs-hero-title">
${lang.value === "pt" ? "Um registro arqueológico da economia do Wurm Online" : "An archaeological record of Wurm Online's economy"}
</h1>
<p class="obs-hero-sub">
${lang.value === "pt" 
  ? html`Lentes interpretativas construídas a partir de corpora restaurados. A cobertura é parcial.<br>Os dados representam <em>menções observadas</em>, não transações confirmadas.<br>Cada lente é uma leitura — não uma verdade.`
  : html`Interpretive lenses built from restored corpora. Coverage is partial.<br>Data represents <em>observed mentions</em>, not confirmed transactions.<br>Each lens is a reading — not a truth.`
}
</p>
<div class="derived-badge">
◆ derived data — server: ${server.value} — source: historical archive
</div>
</div>

<div class="obs-section">
<div class="obs-label">${t("source_corpus")}</div>
${CorpusHealthCard(corpus)}
</div>

<div class="obs-section">
<div class="obs-label">${lang.value === "pt" ? "Cronologia Reconstruída — todos os corpora" : "Reconstructed chronology — all corpora"}</div>
${CoverageTimeline(meta.all_corpora)}
</div>

<div class="obs-section">
<div class="obs-label">${lang.value === "pt" ? "Observações recentes" : "Recent observations"}</div>

```js
display(html`<div class="obs-items">
<div class="obs-item">
<div class="obs-dot"></div>
<div>
<div class="obs-text">
${lang.value === "pt" 
  ? html`Aumento observado nas listagens de armas no final de novembro em <strong>${server.value}</strong>. A categoria <strong>${seller.summary.top_category}</strong> representa ${Math.round(seller.summary.top_category_pct * 100)}% de todas as menções.`
  : html`Observed surge in weapon listings during late November on <strong>${server.value}</strong>. <strong>${seller.summary.top_category}</strong> category accounts for ${Math.round(seller.summary.top_category_pct * 100)}% of all mentions.`
}
</div>
<div class="obs-meta">${lang.value === 'pt' ? 'atividade_vendedor' : 'seller_activity'} · ${corpus.period} · ${Math.round(seller.coverage * 100)}% cov</div>
</div>
</div>
<div class="obs-item">
<div class="obs-dot"></div>
<div>
<div class="obs-text">
${lang.value === "pt"
  ? html`Atividade aos sábados em ${server.value} é <strong>${seller.summary.peak_day_multiplier}×</strong> maior que a média dos dias úteis.`
  : html`Saturday activity on ${server.value} is <strong>${seller.summary.peak_day_multiplier}×</strong> weekday volume.`
}
</div>
<div class="obs-meta">${lang.value === 'pt' ? 'densidade_trade' : 'trade_density'} · multi-corpus · partial</div>
</div>
</div>
</div>`);
```

</div>

<div class="obs-section">
<div class="obs-label">${lang.value === "pt" ? "Lentes Disponíveis" : "Available Lenses"}</div>
<div class="obs-grid-lenses">
${LensCard({
  href: "/lenses/seller",
  icon: "ti-user-circle",
  name: t("seller_title"),
  insight: `${seller.summary.unique_sellers} ${t("unique_sellers")}`,
  coverage: corpus.coverage,
  period: corpus.period,
  status: "active",
  version: "v0.1"
})}
${LensCard({
  href: "/lenses/buyer",
  icon: "ti-search",
  name: t("buyer_title"),
  insight: `${buyer.summary.unique_buyers} ${t("unique_buyers")}`,
  coverage: corpus.coverage,
  period: corpus.period,
  status: "active",
  version: "v0.1"
})}
</div>
</div>

</div>
'''

with open('src/index.md', 'w', encoding='utf-8', newline='\r\n') as f:
    f.write(content)
print("index.md fixed with static FileAttachment loading")
