import { html } from "npm:htl";

const HEIGHTS = [32, 27, 30, 25, 32, 26, 31, 28, 32, 27, 30, 29, 32, 26, 28];

export function CoverageTimeline(corpora) {
  return html`
    <div>
      <div class="timeline-track">
        ${corpora.map((c, i) => {
          const pct = Math.round(c.coverage * 100);
          const h = HEIGHTS[i % HEIGHTS.length];
          const isGap = c.coverage === 0;
          const alpha = isGap ? 0 : (0.2 + c.coverage * 0.8).toFixed(2);
          const tip = isGap
            ? `${c.month} — no data`
            : `${c.month} · ${pct}% coverage`;
          return html`
            <div
              class="timeline-seg ${isGap ? 'gap-seg' : ''}"
              style="
                height: ${h}px;
                ${!isGap ? `background: rgba(var(--amber-rgb), ${alpha});` : ''}
                align-self: flex-end;
              "
            >
              <div class="timeline-seg-tooltip">${tip}</div>
            </div>
          `;
        })}
      </div>
      <div class="timeline-axis">
        ${corpora.map(c => html`<span>${c.month.slice(0, 3)}</span>`)}
      </div>
      <div class="cov-legend" style="margin-top:6px">
        <div class="cov-legend-item">
          <div class="cov-swatch covered"></div>
          <span>high coverage</span>
        </div>
        <div class="cov-legend-item">
          <div class="cov-swatch" style="background:rgba(176,125,42,0.35);border:0.5px solid var(--border)"></div>
          <span>partial</span>
        </div>
        <div class="cov-legend-item">
          <div class="cov-swatch gap"></div>
          <span>absent — unknown territory</span>
        </div>
      </div>
    </div>
  `;
}
