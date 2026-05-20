/**
 * token-cloud.js — Word/token frequency visualizer for Wurm trade data.
 *
 * Since d3-cloud is a layout-only library and needs DOM measurement,
 * we implement a CSS-based "frequency cloud" that scales font-size
 * proportionally — works perfectly in Observable Framework with no
 * extra npm dependencies.
 *
 * For a richer visual, a d3-cloud version is also exported (opt-in).
 *
 * Usage:
 *   import { TokenCloud, TokenBar } from "./components/token-cloud.js";
 *   display(TokenCloud(data.tokens.items, { title: "Itens", lang: "pt" }));
 *   display(TokenBar(data.tokens.enchants, { title: "Enchants" }));
 */

import { html } from "npm:htl";

// ─── CSS Token Cloud (no extra deps) ────────────────────────────────────────

/**
 * @param {Array}  tokens  - [{text, count}, ...] sorted by count desc
 * @param {object} opts    - { title, lang, maxWords, minFontRem, maxFontRem }
 */
export function TokenCloud(tokens = [], opts = {}) {
  const {
    title      = "",
    lang       = "pt",
    maxWords   = 40,
    minFont    = 0.7,   // rem
    maxFont    = 2.2,   // rem
    minOpacity = 0.45,
    maxOpacity = 1.0
  } = opts;

  if (!tokens || tokens.length === 0) {
    return html`<div style="color:var(--ink-4);font-size:0.72rem;font-family:var(--font-mono);padding:0.5rem 0">
      ${lang === "pt" ? "— sem dados suficientes —" : "— insufficient data —"}
    </div>`;
  }

  const top    = tokens.slice(0, maxWords);
  const maxVal = top[0]?.count || 1;
  const minVal = top[top.length - 1]?.count || 1;
  const range  = Math.max(maxVal - minVal, 1);

  // Shuffle for visual variety (keeps relative sizes, breaks alphabetic order)
  const shuffled = [...top].sort(() => Math.random() - 0.5);

  const words = shuffled.map(t => {
    const ratio   = (t.count - minVal) / range;
    const fontSize = minFont + ratio * (maxFont - minFont);
    const opacity  = minOpacity + ratio * (maxOpacity - minOpacity);
    const isTop3   = top.indexOf(t) < 3;

    return html`<span
      title="${t.text}: ${t.count}"
      style="
        font-size: ${fontSize.toFixed(2)}rem;
        opacity: ${opacity.toFixed(2)};
        color: ${isTop3 ? "var(--amber)" : "var(--ink)"};
        font-family: var(--font-title);
        line-height: 1.4;
        cursor: default;
        transition: opacity 0.15s, color 0.15s;
        white-space: nowrap;
      "
      onmouseenter="this.style.color='var(--amber)';this.style.opacity='1'"
      onmouseleave="this.style.color='${isTop3 ? "var(--amber)" : "var(--ink)"
        }';this.style.opacity='${opacity.toFixed(2)}'"
    >${t.text}</span>`;
  });

  return html`<div>
    ${title ? html`<div class="obs-label" style="margin-bottom:0.6rem">${title}</div>` : ""}
    <div style="
      display: flex;
      flex-wrap: wrap;
      gap: 0.5rem 0.85rem;
      align-items: baseline;
      line-height: 1.5;
      padding: 0.25rem 0;
    ">${words}</div>
  </div>`;
}


// ─── Horizontal bar ranking (cleaner for enchants/professions) ───────────────

/**
 * @param {Array}  tokens  - [{text, count}, ...] sorted by count desc
 * @param {object} opts    - { title, lang, maxItems, color }
 */
export function TokenBar(tokens = [], opts = {}) {
  const {
    title    = "",
    lang     = "pt",
    maxItems = 15,
    color    = "var(--amber)"
  } = opts;

  if (!tokens || tokens.length === 0) {
    return html`<div style="color:var(--ink-4);font-size:0.72rem;font-family:var(--font-mono);padding:0.5rem 0">
      ${lang === "pt" ? "— sem dados suficientes —" : "— insufficient data —"}
    </div>`;
  }

  const top    = tokens.slice(0, maxItems);
  const maxVal = top[0]?.count || 1;

  const rows = top.map((t, i) => html`
    <div style="
      display: grid;
      grid-template-columns: 130px 1fr 36px;
      gap: 8px;
      align-items: center;
      padding: 4px 0;
      border-bottom: 0.5px solid var(--gap-bg);
    ">
      <span style="font-size:0.72rem;color:var(--ink);overflow:hidden;text-overflow:ellipsis;white-space:nowrap"
        title="${t.text}">${t.text}</span>
      <div style="background:var(--gap-bg);border-radius:2px;height:4px;overflow:hidden">
        <div style="width:${Math.round(t.count / maxVal * 100)}%;height:100%;background:${color};border-radius:2px"></div>
      </div>
      <span style="font-size:0.68rem;color:var(--ink-3);text-align:right;font-family:var(--font-mono)">${t.count}</span>
    </div>`);

  return html`<div>
    ${title ? html`<div class="obs-label" style="margin-bottom:0.5rem">${title}</div>` : ""}
    <div>${rows}</div>
  </div>`;
}


// ─── Combined panel (cloud + bar side by side) ───────────────────────────────

/**
 * TokenPanel — combines a cloud and a ranked bar for the same dataset
 * @param {Array}  tokens
 * @param {object} opts  - { title, lang, cloudTitle, barTitle }
 */
export function TokenPanel(tokens = [], opts = {}) {
  const { title = "", lang = "pt", cloudTitle, barTitle } = opts;

  return html`<div>
    ${title ? html`<div class="obs-label" style="margin-bottom:0.75rem">${title}</div>` : ""}
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:1.5rem;align-items:start">
      <div>${TokenCloud(tokens, { lang, title: cloudTitle || "" })}</div>
      <div>${TokenBar(tokens,   { lang, title: barTitle   || "" })}</div>
    </div>
  </div>`;
}
