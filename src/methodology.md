---
title: Methodology
toc: false
---

```js
import { html } from "npm:htl";
import { t, LanguageSelector, lang } from "./components/i18n.js";
```

```js
display(html`<div class="obs-page">

<div class="obs-hero">
  <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:1.5rem">
    <div style="font-size:0.65rem; color:var(--amber); letter-spacing:2px; text-transform:uppercase">${t("methodology_title")}</div>
    ${LanguageSelector()}
  </div>
  <h1 class="obs-hero-title">${lang.value === "pt" ? "O que isso é — e o que não é" : "What this is — and what it isn't"}</h1>
</div>

<div class="obs-section" style="margin-top:3rem">
  <h2 style="font-family:var(--font-title); font-weight:400; color:var(--ink); margin-bottom:1rem">${lang.value === "pt" ? "Os dois projetos" : "The two projects"}</h2>
  <p style="font-size:0.9rem; color:var(--ink-2); line-height:1.8">
    ${lang.value === "pt"
      ? "O Wurm Market Observatory é o segundo de dois projetos relacionados. O Arquivo Histórico preserva os logs brutos do canal de trade — ele não interpreta, é uma infraestrutura de custódia. Este Observatório lê os corpora exportados e gera análises interpretativas. Ele nunca modifica os dados originais. Cada número aqui é derivado — não original."
      : "The Wurm Market Observatory is the second of two related projects. The Historical Archive preserves raw trade channel logs — it does not interpret, it is a custodial infrastructure. This Observatory reads exported corpora and generates interpretive analyses. It never modifies the source data. Every number here is derived — not original."}
  </p>
</div>

<div class="obs-section" style="margin-top:2.5rem">
  <h2 style="font-family:var(--font-title); font-weight:400; color:var(--ink); margin-bottom:1rem">${lang.value === "pt" ? "O que são lentes?" : "What are lenses?"}</h2>
  <p style="font-size:0.9rem; color:var(--ink-2); line-height:1.8">
    ${lang.value === "pt"
      ? "As análises são chamadas de lentes — deliberadamente. Uma lente é uma forma de olhar, não uma forma de saber. Cada lente tem seu próprio parser, sua própria metodologia e suas próprias limitações. Nenhuma é autoritativa. Todas são parciais."
      : "Analyses are called lenses — deliberately. A lens is a way of looking, not a way of knowing. Each lens has its own parser, its own methodology, its own limitations. None is authoritative. All are partial."}
  </p>
</div>

<div class="obs-section" style="margin-top:2.5rem">
  <h2 style="font-family:var(--font-title); font-weight:400; color:var(--ink); margin-bottom:1rem">${lang.value === "pt" ? "Cobertura e lacunas" : "Coverage and gaps"}</h2>
  <p style="font-size:0.9rem; color:var(--ink-2); line-height:1.8">
    ${lang.value === "pt"
      ? "Nenhum corpus é completo. Gaps são períodos com zero entradas e nunca são interpolados. Quando um gráfico mostra uma região tracejada significa: não sabemos o que aconteceu aqui."
      : "No corpus is complete. Gaps are periods with zero entries and are never interpolated. When a chart shows a hatched region it means: we do not know what happened here."}
  </p>
</div>

<div class="obs-section" style="margin-top:3rem">
  <div class="obs-card" style="border-left: 2px solid var(--amber)">
    <strong style="font-size:0.8rem; color:var(--ink)">${lang.value === "pt" ? "Uma nota sobre honestidade epistêmica —" : "A note on epistemic honesty —"}</strong>
    <p style="font-size:0.8rem; color:var(--ink-2); line-height:1.7; margin-top:0.5rem">
      ${lang.value === "pt"
        ? "O canal de trade é um chat público, não um mercado formal. Vendedores postam, compradores respondem, os negócios acontecem fora do canal. Este observatório observa a superfície da atividade econômica, não a atividade em si. Trate cada número como uma estimativa com margens de erro desconhecidas."
        : "The trade channel is a public chat, not a formal marketplace. Sellers post, buyers respond, deals happen off-channel. This observatory observes the surface of economic activity, not the activity itself. Treat every number as an estimate with unknown error bounds."}
    </p>
  </div>
</div>

</div>`);
```
