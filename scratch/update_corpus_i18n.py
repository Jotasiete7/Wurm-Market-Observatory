import sys

content = r'''---
title: Corpus Explorer
toc: false
---

```js
import { html } from "npm:htl";
import { t, LanguageSelector, lang } from "./components/i18n.js";
const meta = await FileAttachment("data/corpus-meta.json").json();
```

<div class="obs-page">

  <div class="obs-hero" style="padding-bottom:1.5rem">
    <div style="display:flex; justify-content:space-between; align-items:flex-start;">
      <div class="obs-hero-eyebrow">${t("explorer_title")}</div>
      <div>${LanguageSelector()}</div>
    </div>
    <h1 class="obs-hero-title" style="font-size:1.8rem">
      ${lang.value === "pt" ? "A matéria-prima" : "The raw material"}
    </h1>
    <p class="obs-hero-sub">
      ${lang.value === "pt" 
        ? "Cada análise neste observatório deriva de corpora restaurados baixados do Arquivo Histórico. Esta página mostra o que foi carregado, o que está faltando e a contribuição de cada corpus."
        : "Every analysis in this observatory derives from restored corpora downloaded from the Historical Archive. This page shows what has been loaded, what is missing, and what each corpus contributes."
      }
    </p>
  </div>

  <div class="obs-section">
    <div class="obs-label">${lang.value === "pt" ? "Corpora Carregados" : "Loaded corpora"}</div>
```js
display(html`<div style="display:flex;flex-direction:column;gap:8px">
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
        <span class="lens-status ${c.coverage >= 0.65 ? 'active' : 'partial'}">${c.coverage >= 0.65 ? (lang.value === 'pt' ? 'bom' : 'good') : 'partial'}</span>
      </div>
    </div>
  `)}
</div>`)
```
  </div>

  <div class="obs-section">
    <div class="obs-label">${lang.value === "pt" ? "Períodos Ausentes" : "Missing periods"}</div>
```js
display(html`<div style="display:flex;flex-direction:column;gap:8px">
  ${meta.all_corpora.filter(c => c.coverage === 0).map(c => html`
    <div class="obs-card obs-card-sm" style="display:flex;align-items:center;gap:1.5rem;opacity:0.5">
      <div style="min-width:90px;font-size:0.75rem;color:var(--ink-3)">${c.month}</div>
      <div style="flex:1;height:5px;background:repeating-linear-gradient(90deg, var(--gap) 0, var(--gap) 2px, transparent 2px, transparent 6px);border-radius:2px"></div>
      <span class="lens-status unavail">${lang.value === 'pt' ? 'sem dados' : 'no data'}</span>
    </div>
  `)}
</div>`)
```
  </div>

  <div class="obs-section">
    <div class="method-note">
      <strong>${lang.value === "pt" ? "O que é um corpus restaurado?" : "What is a restored corpus?"}</strong><br>
      ${lang.value === "pt"
        ? "Corpora são logs do canal de trade extraídos do Wurm Online Historical Archive. 'Restaurado' significa que o log bruto foi limpo de artefatos de codificação e linhas duplicadas. A porcentagem de cobertura reflete quantos dias do período têm pelo menos uma entrada de log válida. Um dia com zero entradas é contado como um gap, independentemente da causa — queda do servidor, falta de upload ou falha de processamento."
        : "Corpora are trade channel logs extracted from the Wurm Online Historical Archive. 'Restored' means the raw log has been cleaned of encoding artifacts and duplicate lines. Coverage percentage reflects how many days of the period have at least one valid log entry. A day with zero entries is counted as a gap regardless of cause — server downtime, missing upload, or parsing failure."
      }
    </div>
  </div>

</div>
'''

with open('src/corpus.md', 'w', encoding='utf-8', newline='\r\n') as f:
    f.write(content)
print("corpus.md updated with i18n support")
