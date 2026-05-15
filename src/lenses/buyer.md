---
title: Buyer Activity Lens
toc: false
---

```js
import * as Plot from "npm:@observablehq/plot";
import { html } from "npm:htl";
import { CorpusHealthCard } from "../components/corpus-health.js";
import { t, LanguageSelector, ServerSelector, lang, server } from "../components/i18n.js";

const nfi_meta = await FileAttachment("../data/nfi-corpus-meta.json").json();
const sfi_meta = await FileAttachment("../data/sfi-corpus-meta.json").json();
const nfi_data = await FileAttachment("../data/nfi-buyer-activity.json").json();
const sfi_data = await FileAttachment("../data/sfi-buyer-activity.json").json();

const meta = server.value === "NFI" ? nfi_meta : sfi_meta;
const data = server.value === "NFI" ? nfi_data : sfi_data;
const corpus = meta.active;
```

<div class="obs-page">

<div style="padding: 2rem 0; border-bottom: 1px solid var(--border); margin-bottom: 3rem;">
<div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:1rem">
<div>
<a href="/" style="font-size:0.75rem; color:var(--amber); text-decoration:none; text-transform:uppercase; letter-spacing:1px">${t("back")}</a>
</div>
<div style="display:flex; gap:8px; align-items:center;">
${ServerSelector()}
${LanguageSelector()}
</div>
</div>

<h1 class="obs-hero-title">${t("buyer_title")}</h1>
<p class="obs-hero-sub">${lang.value === "pt" ? "Sinais de compra detectados no corpus de " + server.value : "Buy signals detected on " + server.value}</p>
</div>

<div class="obs-grid-4" style="display:grid; grid-template-columns: repeat(4, 1fr); gap:1.5rem; margin-bottom:2rem">
<div class="obs-card">
<div class="obs-label" style="margin-bottom:8px">${t("unique_buyers")}</div>
<div class="stat-card-val">${data.summary.unique_buyers}</div>
</div>
<div class="obs-card">
<div class="obs-label" style="margin-bottom:8px">${t("signals")}</div>
<div class="stat-card-val">${data.summary.total_signals.toLocaleString()}</div>
</div>
<div class="obs-card">
<div class="obs-label" style="margin-bottom:8px">${t("top_category")}</div>
<div class="stat-card-val" style="font-size:1.1rem; text-transform:uppercase">${data.summary.top_category}</div>
</div>
<div class="obs-card">
<div class="obs-label" style="margin-bottom:8px">${t("confidence")}</div>
<div class="stat-card-val" style="font-size:1rem; color:var(--success)">${data.confidence}</div>
</div>
</div>

<div class="obs-section" style="margin-top:4rem">
<div class="obs-label">${t("source_corpus")}</div>
${CorpusHealthCard(corpus)}
</div>

</div>
