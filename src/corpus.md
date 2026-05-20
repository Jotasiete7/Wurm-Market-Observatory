---
title: Corpus Explorer
toc: false
---

```js
import { html } from "npm:htl";
import { t, LanguageSelector, lang } from "./components/i18n.js";

const dataPartitions = {
  NFI: {
    "2025": FileAttachment("data/nfi-corpus-meta-2025.json"),
    "2026-ytd": FileAttachment("data/nfi-corpus-meta-2026-ytd.json")
  },
  SFI: {
    "2025": FileAttachment("data/sfi-corpus-meta-2025.json"),
    "2026-ytd": FileAttachment("data/sfi-corpus-meta-2026-ytd.json")
  }
};
```

```js
const serverView = Inputs.select(["NFI", "SFI"], {value: "NFI"});
const serverVal  = Generators.input(serverView);

const periodView = Inputs.select(["2025", "2026-ytd"], {
  format: x => x === "2025" ? "2025 (Jan–Dec)" : "2026 (YTD)",
  value: "2025"
});
const periodVal = Generators.input(periodView);
```

```js
const activeServer = serverVal === "SFI" ? "SFI" : "NFI";
const activePeriod = periodVal === "2026-ytd" ? "2026-ytd" : "2025";
const activePartition = dataPartitions[activeServer][activePeriod];
const meta = await activePartition.json();
const langVal = lang.value || "pt";
```

```js
display(html`<div class="obs-page">

<div class="obs-hero">
  <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:1.5rem">
    <div class="obs-hero-eyebrow">${t("explorer_title")}</div>
    <div style="display:flex; gap:8px; align-items:center;">
      ${serverView}
      ${periodView}
      ${LanguageSelector()}
    </div>
  </div>
  <h1 class="obs-hero-title">${langVal === "pt" ? "A matéria-prima" : "The raw material"}</h1>
  <p class="obs-hero-sub">
    ${langVal === "pt"
      ? "Cada análise neste observatório deriva de corpora restaurados do Arquivo Histórico. Esta página mostra o que foi carregado e o que está faltando."
      : "Every analysis in this observatory derives from restored corpora from the Historical Archive. This page shows what has been loaded and what is missing."}
  </p>
</div>

<div class="obs-section" style="margin-top:3rem">
  <div class="obs-label">${langVal === "pt" ? "Corpora Carregados (" + serverVal + ")" : "Loaded Corpora (" + serverVal + ")"}</div>
  <div style="display:flex; flex-direction:column; gap:8px; margin-top:1rem">
    ${meta.all_corpora.filter(c => c.coverage > 0).map(c => html`
      <div class="obs-card" style="display:flex; align-items:center; gap:1.5rem; padding:0.75rem 1rem">
        <div style="min-width:90px; font-size:0.75rem; color:var(--ink)">${c.month}</div>
        <div style="flex:1; background:var(--border); border-radius:2px; height:4px; overflow:hidden">
          <div style="width:${Math.round(c.coverage * 100)}%; height:100%; background:var(--amber)"></div>
        </div>
        <div style="min-width:40px; text-align:right; font-size:0.75rem; color:var(--amber)">${Math.round(c.coverage * 100)}%</div>
      </div>
    `)}
  </div>
</div>

<div class="obs-section" style="margin-top:3rem">
  <div class="obs-label">${langVal === "pt" ? "Períodos Ausentes" : "Missing Periods"}</div>
  <div style="display:flex; flex-direction:column; gap:8px; margin-top:1rem">
    ${meta.all_corpora.filter(c => c.coverage === 0).length === 0
      ? html`<p style="color:var(--ink-3); font-size:0.8rem">${langVal === "pt" ? "Nenhum gap detectado." : "No gaps detected."}</p>`
      : meta.all_corpora.filter(c => c.coverage === 0).map(c => html`
        <div class="obs-card" style="display:flex; align-items:center; gap:1.5rem; padding:0.75rem 1rem; opacity:0.5">
          <div style="min-width:90px; font-size:0.75rem; color:var(--ink-3)">${c.month}</div>
          <div style="flex:1; height:4px; background:var(--hatch); border-radius:2px"></div>
          <div style="font-size:0.7rem; color:var(--ink-4)">${langVal === "pt" ? "sem dados" : "no data"}</div>
        </div>
      `)
    }
  </div>
</div>

<div class="obs-section" style="margin-top:3rem">
  <div class="method-note">
    <strong>${langVal === "pt" ? "O que é um corpus restaurado?" : "What is a restored corpus?"}</strong><br>
    <p style="font-size:0.8rem; color:var(--ink-2); line-height:1.7; margin-top:0.5rem">
      ${langVal === "pt"
        ? "Corpora são logs do canal de trade extraídos do Arquivo Histórico. 'Restaurado' significa que o log foi limpo de artefatos e duplicatas. A cobertura reflete quantos dias têm pelo menos uma entrada válida."
        : "Corpora are trade channel logs from the Historical Archive. 'Restored' means the log has been cleaned of encoding artifacts and duplicates. Coverage reflects how many days have at least one valid log entry."}
    </p>
  </div>
</div>

</div>`);
```
