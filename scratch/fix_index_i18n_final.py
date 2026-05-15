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
import { t, LanguageSelector, lang } from "./components/i18n.js";

const meta   = await FileAttachment("data/corpus-meta.json").json();
const corpus = meta.active;
const seller = await FileAttachment("data/seller-activity.json").json();
const buyer  = await FileAttachment("data/buyer-activity.json").json();
```

<div class="obs-page">

<div class="obs-hero">
<div style="display:flex; justify-content:space-between; align-items:flex-start;">
<div class="obs-hero-eyebrow">Wurm Market Observatory</div>
<div>${LanguageSelector()}</div>
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
◆ derived data — source: historical archive — not canonical
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
  ? html`Aumento observado nas listagens de armas no final de novembro — concentração em longswords e armaduras de placa. A categoria <strong>${seller.summary.top_category}</strong> representa ${Math.round(seller.summary.top_category_pct * 100)}% de todas as menções.`
  : html`Observed surge in weapon listings during late November — concentration in longswords and plate armour. <strong>${seller.summary.top_category}</strong> category accounts for ${Math.round(seller.summary.top_category_pct * 100)}% of all mentions.`
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
  ? html`Atividade aos sábados é consistentemente <strong>${seller.summary.peak_day_multiplier}×</strong> maior que a média dos dias úteis. O padrão se mantém em todos os corpora.`
  : html`Saturday activity consistently <strong>${seller.summary.peak_day_multiplier}×</strong> weekday volume across all covered periods. Pattern holds across corpora.`
}
</div>
<div class="obs-meta">${lang.value === 'pt' ? 'densidade_trade' : 'trade_density'} · multi-corpus · partial</div>
</div>
</div>
<div class="obs-item">
<div class="obs-dot"></div>
<div>
<div class="obs-text">
${lang.value === "pt"
  ? html`Menções a itens raros como espelhos permanecem extremamente esparsas — menos de 3 aparições por mês coberto.`
  : html`Rare mirror mentions remain extremely sparse — fewer than 3 appearances per covered month.`
}
</div>
<div class="obs-meta">rare_item · ${corpus.period} · low confidence</div>
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
${LensCard({
  href: "#",
  icon: "ti-chart-area",
  name: lang.value === "pt" ? "Densidade de Trade" : "Trade Density",
  insight: lang.value === "pt" ? "Picos de atividade Sex-Sáb noites UTC" : "Activity peaks Fri-Sat evenings UTC",
  coverage: 0.43,
  period: "partial",
  status: "partial",
  version: "v0.1"
})}
</div>
</div>

</div>
'''

with open('src/index.md', 'w', encoding='utf-8', newline='\r\n') as f:
    f.write(content)
print("index.md updated with full bilingual support")
