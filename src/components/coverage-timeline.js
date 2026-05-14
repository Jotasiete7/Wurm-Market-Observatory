import { html } from "npm:htl";

export function CoverageTimeline(corpora) {
  return html`
    <div>
      <div class="timeline-track">
        ${corpora.map(c => {
          const pct = Math.round(c.coverage * 100);
          let bg;
          if (c.coverage === 0) {
            bg = `repeating-linear-gradient(90deg, var(--gap) 0, var(--gap) 2px, transparent 2px, transparent 6px)`;
          } else {
            const alpha = (0.25 + c.coverage * 0.75).toFixed(2);
            bg = `rgba(176, 125, 42, ${alpha})`;
          }
          const tip = c.coverage === 0
            ? `${c.month} — no data`
            : `${c.month} · ${pct}% coverage`;
          return html`
            <div class="timeline-seg" style="background:${bg};border:0.5px solid var(--border)">
              <div class="timeline-seg-tooltip">${tip}</div>
            </div>
          `;
        })}
      </div>
      <div class="timeline-axis">
        ${corpora.map(c => html`<span>${c.month.slice(0, 3)}</span>`)}
      </div>
    </div>
  `;
}
