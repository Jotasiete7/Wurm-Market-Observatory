---
title: Methodology
toc: false
---

```js
import { html } from "npm:htl";
import { t, LanguageSelector, lang } from "./components/i18n.js";
```

<div class="obs-page">

<div class="obs-hero" style="padding-bottom:1.5rem">
<div style="display:flex; justify-content:space-between; align-items:flex-start;">
<div class="obs-hero-eyebrow">${t("methodology_title")}</div>
<div>${LanguageSelector()}</div>
</div>
```js
display(html`<h1 class="obs-hero-title" style="font-size:1.8rem">
${lang.value === "pt" ? "O que isso é — e o que não é" : "What this is — and what it isn't"}
</h1>`)
```
</div>

<div class="obs-section">
```js
display(html`<h2>${lang.value === "pt" ? "Os dois projetos" : "The two projects"}</h2>`)
```
<p>
${lang.value === "pt"
? "O Wurm Market Observatory é o segundo de dois projetos relacionados, porém independentes."
: "The Wurm Market Observatory is the second of two related but independent projects."
}
</p>
<p>
<strong>${lang.value === "pt" ? "Projeto 1 — Arquivo Histórico" : "Project 1 — Historical Archive"}</strong>
${lang.value === "pt"
? "preserva os logs brutos do canal de trade do Wurm Online. Ele armazena os arquivos .txt originais e mostra a cobertura temporal. Ele não interpreta; é uma infraestrutura de custódia."
: "preserves raw trade channel logs from Wurm Online. It stores original .txt files, deduplicates uploads, and shows temporal coverage. It does not interpret. It is a custodial infrastructure."
}
</p>
<p>
<strong>${lang.value === "pt" ? "Projeto 2 — Este Observatório" : "Project 2 — This Observatory"}</strong>
${lang.value === "pt"
? "lê os corpora exportados do Arquivo e gera análises interpretativas. Ele nunca modifica os dados originais. Cada número aqui é derivado — não original."
: "reads restored corpora exported from the Archive and generates interpretive analyses. It never modifies the source data. Every number here is derived — not original."
}
</p>
</div>

<div class="obs-section">
```js
display(html`<h2>${lang.value === "pt" ? "O que são lentes?" : "What are lenses?"}</h2>`)
```
<p>
${lang.value === "pt"
? "As análises neste observatório são chamadas de lentes — deliberadamente. Uma lente é uma forma de olhar, não uma forma de saber. Cada lente tem seu próprio parser, sua própria metodologia e suas próprias limitações. Nenhuma é autoritativa. Todas são parciais."
: "Analyses in this observatory are called *lenses* — deliberately. A lens is a way of looking, not a way of knowing. Each lens has its own parser, its own methodology, its own limitations. None is authoritative. All are partial."
}
</p>
</div>

<div class="obs-section">
```js
display(html`<h2>${lang.value === "pt" ? "Cobertura e lacunas (gaps)" : "Coverage and gaps"}</h2>`)
```
<p>
${lang.value === "pt"
? "Nenhum corpus neste arquivo é completo. A cobertura é expressa como uma porcentagem de dias em um período que contêm pelo menos uma entrada de log válida. Gaps são períodos com zero entradas. As lacunas nunca são interpoladas. Quando um gráfico mostra uma região hachurada, significa: não sabemos o que aconteceu aqui. O gráfico não adivinha."
: "No corpus in this archive is complete. Coverage is expressed as a percentage of days in a period that contain at least one valid log entry. Gaps are periods with zero entries. Gaps are never interpolated. When a chart shows a hatched region, it means: *we do not know what happened here.* The chart does not guess."
}
</p>
</div>

<div class="obs-section">
<div class="method-note" style="margin-top:2rem">
<strong>${lang.value === "pt" ? "Uma nota sobre honestidade epistêmica —" : "A note on epistemic honesty —"}</strong><br>
${lang.value === "pt"
? "O canal de trade do Wurm Online é um chat público, não um mercado formal. Vendedores postam, compradores respondem, e os negócios acontecem fora do canal. Este observatório observa a superfície da atividade econômica, não a atividade em si. Trate cada número aqui como uma estimativa com margens de erro desconhecidas."
: "Wurm Online's trade channel is a public chat channel, not a formal marketplace. Sellers post, buyers respond, deals happen off-channel. This observatory observes the surface of economic activity, not the activity itself. Treat every number here as an estimate with unknown error bounds."
}
</div>
</div>

</div>
