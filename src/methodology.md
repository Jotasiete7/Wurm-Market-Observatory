---
title: Methodology
toc: false
---

```js
import { html } from "npm:htl";
import { t, LanguageSelector, lang } from "./components/i18n.js";

const langVal = lang.value || "pt";
```

```js
display(html`<div class="obs-page">

<div class="obs-hero">
  <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:1.5rem">
    <div class="obs-hero-eyebrow">${t("methodology_title")}</div>
    ${LanguageSelector()}
  </div>
  <h1 class="obs-hero-title">${langVal === "pt" ? "O que isso é — e o que não é" : "What this is — and what it isn't"}</h1>
</div>

<div class="obs-section" style="margin-top:3rem">
  <h2 style="font-family:var(--font-title); font-weight:400; color:var(--ink); margin-bottom:1rem">${langVal === "pt" ? "Os dois projetos" : "The two projects"}</h2>
  <p style="font-size:0.9rem; color:var(--ink-2); line-height:1.8">
    ${langVal === "pt"
      ? "O Wurm Market Observatory é o segundo de dois projetos relacionados. O Arquivo Histórico preserva os logs brutos do canal de trade — ele não interpreta, é uma infraestrutura de custódia. Este Observatório lê os corpora exportados e gera análises interpretativas."
      : "The Wurm Market Observatory is the second of two related projects. The Historical Archive preserves raw trade channel logs — it does not interpret, it is a custodial infrastructure. This Observatory reads exported corpora and generates interpretive analyses."}
  </p>
</div>

<div class="obs-section" style="margin-top:2.5rem">
  <h2 style="font-family:var(--font-title); font-weight:400; color:var(--ink); margin-bottom:1rem">${langVal === "pt" ? "O que são lentes?" : "What are lenses?"}</h2>
  <p style="font-size:0.9rem; color:var(--ink-2); line-height:1.8">
    ${langVal === "pt"
      ? "As análises são chamadas de lentes — deliberadamente. Uma lente é uma forma de olhar, não uma forma de saber. Cada lente tem seu próprio parser, sua própria metodologia e suas próprias limitações. Nenhuma é autoritativa. Todas são parciais."
      : "Analyses are called lenses — deliberately. A lens is a way of looking, not a way of knowing. Each lens has its own parser, its own methodology, its own limitations. None is authoritative. All are partial."}
  </p>
</div>

<div class="obs-section" style="margin-top:3rem">
  <div class="method-note">
    <strong>${langVal === "pt" ? "Uma nota sobre honestidade epistêmica —" : "A note on epistemic honesty —"}</strong>
    <p style="font-size:0.8rem; color:var(--ink-2); line-height:1.7; margin-top:0.5rem">
      ${langVal === "pt"
        ? "O canal de trade é um chat público, não um mercado formal. Vendedores postam, compradores respondem, os negócios acontecem fora do canal. Este observatório observa a superfície da atividade econômica, não a atividade em si."
        : "The trade channel is a public chat, not a formal marketplace. Sellers post, buyers respond, deals happen off-channel. This observatory observes the surface of economic activity, not the activity itself."}
    </p>
  </div>
</div>

</div>`);
```
